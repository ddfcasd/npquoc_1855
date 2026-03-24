import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        try:
            url = "http://127.0.0.1:5000/api/rsa/generate_keys"
            response = requests.get(url)
            if response.status_code == 200:
                QMessageBox.information(self, "Info", response.json().get("message", "OK"))
            else:
                QMessageBox.warning(self, "Error", "Generate Keys failed")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_encrypt(self):
        try:
            url = "http://127.0.0.1:5000/api/rsa/encrypt"
            payload = {
                "message": self.ui.txt_plainText.toPlainText(),
                "key_type": "public"
            }

            response = requests.post(url, json=payload)

            # DEBUG 🔥
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipherText.setPlainText(data.get("encrypted_message", ""))
            else:
                QMessageBox.warning(self, "Error", response.text)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_decrypt(self):
        try:
            url = "http://127.0.0.1:5000/api/rsa/decrypt"
            payload = {
                "ciphertext": self.ui.txt_cipherText.toPlainText(),
                "key_type": "private"
            }

            response = requests.post(url, json=payload)

            print("DECRYPT:", response.text)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plainText.setPlainText(data.get("decrypted_message", ""))
            else:
                QMessageBox.warning(self, "Error", "Decrypt failed")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_sign(self):
        try:
            url = "http://127.0.0.1:5000/api/rsa/sign"
            payload = {
                "message": self.ui.txt_information.toPlainText()
            }

            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_signature.setPlainText(data.get("signature", ""))
            else:
                QMessageBox.warning(self, "Error", "Sign failed")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def call_api_verify(self):
        try:
            url = "http://127.0.0.1:5000/api/rsa/verify"
            payload = {
                "message": self.ui.txt_information.toPlainText(),
                "signature": self.ui.txt_signature.toPlainText()
            }

            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                result = data.get("is_verified") or data.get("verified") or data.get("valid")

                if result:
                    QMessageBox.information(self, "Verify", "Verified Successfully")
                else:
                    QMessageBox.warning(self, "Verify", "Verification Failed")

            else:
                QMessageBox.warning(self, "Error", "Verify failed")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())