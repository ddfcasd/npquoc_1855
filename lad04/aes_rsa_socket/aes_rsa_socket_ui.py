import socket
import threading
import sys
from typing import List, Optional, Tuple

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ChatServer(QObject):
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self, host: str = "127.0.0.1", port: int = 12345):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.server_key = RSA.generate(2048)
        self.clients: List[Tuple[socket.socket, bytes]] = []
        self.lock = threading.Lock()
        self.accept_thread: Optional[threading.Thread] = None

    def update_config(self, host: str, port: int):
        self.host = host
        self.port = port

    def encrypt_message(self, key: bytes, message: str) -> bytes:
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode("utf-8"), AES.block_size))
        return cipher.iv + ciphertext

    def decrypt_message(self, key: bytes, encrypted_message: bytes) -> str:
        iv = encrypted_message[: AES.block_size]
        ciphertext = encrypted_message[AES.block_size :]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_message.decode("utf-8")

    def start_server(self):
        if self.running:
            self.log_signal.emit("Server đang chạy rồi.")
            return

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1)
            self.running = True
            self.accept_thread = threading.Thread(target=self.accept_loop, daemon=True)
            self.accept_thread.start()
            self.status_signal.emit("running")
            self.log_signal.emit(f"Server đang chạy tại {self.host}:{self.port}")
        except Exception as e:
            self.running = False
            self.status_signal.emit("stopped")
            self.log_signal.emit(f"Không thể khởi động server: {e}")
            self.close_server_socket()

    def close_server_socket(self):
        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except Exception:
                pass
            self.server_socket = None

    def stop_server(self):
        self.running = False
        with self.lock:
            for client_socket, _ in self.clients:
                try:
                    client_socket.close()
                except Exception:
                    pass
            self.clients.clear()
        self.close_server_socket()
        self.status_signal.emit("stopped")
        self.log_signal.emit("Server đã dừng.")

    def accept_loop(self):
        while self.running and self.server_socket is not None:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_socket, client_address), daemon=True
                )
                client_thread.start()
            except socket.timeout:
                continue
            except OSError:
                break
            except Exception as e:
                self.log_signal.emit(f"Lỗi accept client: {e}")
                break

    def handle_client(self, client_socket: socket.socket, client_address):
        aes_key = None
        try:
            self.log_signal.emit(f"Client kết nối: {client_address}")

            client_socket.send(self.server_key.publickey().export_key(format="PEM"))
            client_received_key = RSA.import_key(client_socket.recv(4096))

            aes_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(client_received_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            client_socket.send(encrypted_aes_key)

            with self.lock:
                self.clients.append((client_socket, aes_key))

            while self.running:
                encrypted_message = client_socket.recv(4096)
                if not encrypted_message:
                    break

                decrypted_message = self.decrypt_message(aes_key, encrypted_message)
                self.log_signal.emit(f"Nhận từ {client_address}: {decrypted_message}")

                if decrypted_message == "exit":
                    break

                with self.lock:
                    for client, key in list(self.clients):
                        if client != client_socket:
                            try:
                                encrypted = self.encrypt_message(key, decrypted_message)
                                client.send(encrypted)
                            except Exception:
                                pass
        except Exception as e:
            self.log_signal.emit(f"Lỗi client {client_address}: {e}")
        finally:
            if aes_key is not None:
                with self.lock:
                    if (client_socket, aes_key) in self.clients:
                        self.clients.remove((client_socket, aes_key))
            try:
                client_socket.close()
            except Exception:
                pass
            self.log_signal.emit(f"Ngắt kết nối: {client_address}")


class ChatClient(QObject):
    message_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    connection_signal = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.client_socket: Optional[socket.socket] = None
        self.client_key = None
        self.server_public_key = None
        self.aes_key = None
        self.receive_thread: Optional[threading.Thread] = None
        self.connected = False

    def encrypt_message(self, key: bytes, message: str) -> bytes:
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode("utf-8"), AES.block_size))
        return cipher.iv + ciphertext

    def decrypt_message(self, key: bytes, encrypted_message: bytes) -> str:
        iv = encrypted_message[: AES.block_size]
        ciphertext = encrypted_message[AES.block_size :]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_message.decode("utf-8")

    def connect_to_server(self, host: str, port: int):
        if self.connected:
            self.error_signal.emit("Client đã kết nối rồi.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))

            self.client_key = RSA.generate(2048)
            self.server_public_key = RSA.import_key(self.client_socket.recv(4096))
            self.client_socket.send(self.client_key.publickey().export_key(format="PEM"))

            encrypted_aes_key = self.client_socket.recv(4096)
            cipher_rsa = PKCS1_OAEP.new(self.client_key)
            self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)

            self.connected = True
            self.connection_signal.emit(True, f"Đã kết nối tới {host}:{port}")

            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
        except Exception as e:
            self.connected = False
            self.error_signal.emit(f"Không thể kết nối server: {e}")
            self.disconnect(send_exit=False)

    def receive_messages(self):
        while self.connected and self.client_socket is not None:
            try:
                encrypted_message = self.client_socket.recv(4096)
                if not encrypted_message:
                    break
                decrypted_message = self.decrypt_message(self.aes_key, encrypted_message)
                self.message_signal.emit(decrypted_message)
            except Exception:
                break

        if self.connected:
            self.disconnect(send_exit=False)
            self.connection_signal.emit(False, "Mất kết nối server.")

    def send_message(self, message: str):
        if not self.connected or self.client_socket is None or self.aes_key is None:
            self.error_signal.emit("Client chưa kết nối server.")
            return

        try:
            encrypted_message = self.encrypt_message(self.aes_key, message)
            self.client_socket.send(encrypted_message)
        except Exception as e:
            self.error_signal.emit(f"Không gửi được tin nhắn: {e}")
            self.disconnect(send_exit=False)

    def disconnect(self, send_exit: bool = True):
        if send_exit and self.connected and self.client_socket is not None and self.aes_key is not None:
            try:
                encrypted_message = self.encrypt_message(self.aes_key, "exit")
                self.client_socket.send(encrypted_message)
            except Exception:
                pass

        self.connected = False
        if self.client_socket is not None:
            try:
                self.client_socket.close()
            except Exception:
                pass
        self.client_socket = None
        self.aes_key = None
        self.connection_signal.emit(False, "Đã ngắt kết nối.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server = ChatServer()
        self.client = ChatClient()
        self.init_ui()
        self.bind_signals()

    def init_ui(self):
        self.setWindowTitle("AES-RSA SOCKET UI")
        self.resize(980, 620)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title = QLabel("AES-RSA SOCKET UI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        config_group = QGroupBox("Cấu hình kết nối")
        config_layout = QGridLayout(config_group)
        self.txt_host = QLineEdit("127.0.0.1")
        self.txt_port = QLineEdit("12345")
        self.txt_name = QLineEdit("client")
        config_layout.addWidget(QLabel("Host"), 0, 0)
        config_layout.addWidget(self.txt_host, 0, 1)
        config_layout.addWidget(QLabel("Port"), 0, 2)
        config_layout.addWidget(self.txt_port, 0, 3)
        config_layout.addWidget(QLabel("Tên hiển thị"), 0, 4)
        config_layout.addWidget(self.txt_name, 0, 5)
        main_layout.addWidget(config_group)

        body_layout = QHBoxLayout()
        main_layout.addLayout(body_layout)

        server_group = QGroupBox("Server")
        server_layout = QVBoxLayout(server_group)
        server_button_layout = QHBoxLayout()
        self.btn_start_server = QPushButton("Start Server")
        self.btn_stop_server = QPushButton("Stop Server")
        self.btn_stop_server.setEnabled(False)
        server_button_layout.addWidget(self.btn_start_server)
        server_button_layout.addWidget(self.btn_stop_server)
        self.txt_server_log = QTextEdit()
        self.txt_server_log.setReadOnly(True)
        server_layout.addLayout(server_button_layout)
        server_layout.addWidget(self.txt_server_log)
        body_layout.addWidget(server_group)

        client_group = QGroupBox("Client Chat")
        client_layout = QVBoxLayout(client_group)
        client_button_layout = QHBoxLayout()
        self.btn_connect = QPushButton("Connect")
        self.btn_disconnect = QPushButton("Disconnect")
        self.btn_disconnect.setEnabled(False)
        client_button_layout.addWidget(self.btn_connect)
        client_button_layout.addWidget(self.btn_disconnect)
        self.txt_chat = QTextEdit()
        self.txt_chat.setReadOnly(True)
        input_layout = QHBoxLayout()
        self.txt_message = QLineEdit()
        self.txt_message.setPlaceholderText("Nhập tin nhắn...")
        self.btn_send = QPushButton("Send")
        self.btn_send.setEnabled(False)
        input_layout.addWidget(self.txt_message)
        input_layout.addWidget(self.btn_send)
        client_layout.addLayout(client_button_layout)
        client_layout.addWidget(self.txt_chat)
        client_layout.addLayout(input_layout)
        body_layout.addWidget(client_group)

    def bind_signals(self):
        self.btn_start_server.clicked.connect(self.start_server)
        self.btn_stop_server.clicked.connect(self.server.stop_server)
        self.btn_connect.clicked.connect(self.connect_client)
        self.btn_disconnect.clicked.connect(self.disconnect_client)
        self.btn_send.clicked.connect(self.send_message)
        self.txt_message.returnPressed.connect(self.send_message)

        self.server.log_signal.connect(self.append_server_log)
        self.server.status_signal.connect(self.handle_server_status)

        self.client.message_signal.connect(self.append_incoming_message)
        self.client.error_signal.connect(self.show_error)
        self.client.connection_signal.connect(self.handle_client_connection)

    def get_host_port(self):
        host = self.txt_host.text().strip() or "127.0.0.1"
        try:
            port = int(self.txt_port.text().strip())
        except ValueError:
            raise ValueError("Port phải là số nguyên.")
        return host, port

    def start_server(self):
        try:
            host, port = self.get_host_port()
        except ValueError as e:
            self.show_error(str(e))
            return
        self.server.update_config(host, port)
        self.server.start_server()

    def connect_client(self):
        try:
            host, port = self.get_host_port()
        except ValueError as e:
            self.show_error(str(e))
            return
        self.client.connect_to_server(host, port)

    def disconnect_client(self):
        self.client.disconnect()

    def send_message(self):
        message = self.txt_message.text().strip()
        if not message:
            return

        display_name = self.txt_name.text().strip()
        outgoing_message = f"{display_name}: {message}" if display_name else message
        self.client.send_message(outgoing_message)
        self.txt_chat.append(f"Me: {message}")
        self.txt_message.clear()

    def append_server_log(self, text: str):
        self.txt_server_log.append(text)

    def append_incoming_message(self, text: str):
        self.txt_chat.append(text)

    def handle_server_status(self, status: str):
        is_running = status == "running"
        self.btn_start_server.setEnabled(not is_running)
        self.btn_stop_server.setEnabled(is_running)

    def handle_client_connection(self, connected: bool, text: str):
        self.txt_chat.append(text)
        self.btn_connect.setEnabled(not connected)
        self.btn_disconnect.setEnabled(connected)
        self.btn_send.setEnabled(connected)

    def show_error(self, text: str):
        QMessageBox.warning(self, "Thông báo", text)

    def closeEvent(self, event):
        try:
            self.client.disconnect(send_exit=False)
        except Exception:
            pass
        try:
            self.server.stop_server()
        except Exception:
            pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
