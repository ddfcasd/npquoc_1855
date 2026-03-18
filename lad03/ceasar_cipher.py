import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txt_plain_text.toPlainText(),
            "key": self.ui.txt_key.text()
        }
        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data["result"])
                QMessageBox.information(self, "OK", "Encrypted Successfully")
            else:
                print("Error:", response.text)

        except Exception as e:
            print("Error:", e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txt_cipher_text.toPlainText(),
            "key": self.ui.txt_key.text()
        }
        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["result"])
                QMessageBox.information(self, "OK", "Decrypted Successfully")
            else:
                print("Error:", response.text)

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())