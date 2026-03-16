class CaesarCipher:

    def encrypt_text(self, text, key):
        result = ""

        for char in text:
            if char.isalpha():

                shift = key % 26

                if char.isupper():
                    result += chr((ord(char) + shift - 65) % 26 + 65)
                else:
                    result += chr((ord(char) + shift - 97) % 26 + 97)

            else:
                result += char

        return result


    def decrypt_text(self, text, key):
        return self.encrypt_text(text, -key)