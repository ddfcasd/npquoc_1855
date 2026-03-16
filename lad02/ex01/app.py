from flask import Flask, render_template, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__, template_folder="templates")
app.secret_key = "123456"


@app.route("/")
def home():
    return render_template("index.html")


# ===================== CAESAR =====================
@app.route("/caesar")
def caesar():
    return render_template("caesar.html")


@app.route("/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    try:
        text = request.form.get("inputPlainText", "").strip()
        key = int(request.form.get("inputKeyPlain", 0))

        caesar = CaesarCipher()
        encrypted_text = caesar.encrypt_text(text, key)

        return f"""
        <h3>Kết quả mã hóa Caesar</h3>
        text: {text}<br>
        key: {key}<br>
        encrypted text: {encrypted_text}
        """
    except Exception as e:
        return f"Lỗi Caesar Encrypt: {str(e)}"


@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    try:
        text = request.form.get("inputCipherText", "").strip()
        key = int(request.form.get("inputKeyCipher", 0))

        caesar = CaesarCipher()
        decrypted_text = caesar.decrypt_text(text, key)

        return f"""
        <h3>Kết quả giải mã Caesar</h3>
        text: {text}<br>
        key: {key}<br>
        decrypted text: {decrypted_text}
        """
    except Exception as e:
        return f"Lỗi Caesar Decrypt: {str(e)}"


# ===================== VIGENERE =====================
@app.route("/vigenere")
def vigenere():
    return render_template("vigenere.html")


@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    try:
        text = request.form.get("inputPlainText", "").strip()
        key = request.form.get("inputKeyPlain", "").strip()

        vigenere = VigenereCipher()
        encrypted_text = vigenere.encrypt_text(text, key)

        return f"""
        <h3>Kết quả mã hóa Vigenere</h3>
        text: {text}<br>
        key: {key}<br>
        encrypted text: {encrypted_text}
        """
    except Exception as e:
        return f"Lỗi Vigenere Encrypt: {str(e)}"


@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    try:
        text = request.form.get("inputCipherText", "").strip()
        key = request.form.get("inputKeyCipher", "").strip()

        vigenere = VigenereCipher()
        decrypted_text = vigenere.decrypt_text(text, key)

        return f"""
        <h3>Kết quả giải mã Vigenere</h3>
        text: {text}<br>
        key: {key}<br>
        decrypted text: {decrypted_text}
        """
    except Exception as e:
        return f"Lỗi Vigenere Decrypt: {str(e)}"


# ===================== PLAYFAIR =====================
@app.route("/playfair")
def playfair():
    return render_template("playfair.html")


@app.route("/api/playfair/creatematrix", methods=["POST"])
def playfair_creatematrix():
    try:
        data = request.get_json(silent=True) or {}
        key = data.get("key", "").strip()

        playfair_cipher = PlayFairCipher()
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)

        return jsonify({"playfair_matrix": playfair_matrix})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    try:
        text = request.form.get("inputPlainText", "").strip()
        key = request.form.get("inputKeyPlain", "").strip()

        playfair_cipher = PlayFairCipher()
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(text, playfair_matrix)

        return f"""
        <h3>Kết quả mã hóa Playfair</h3>
        text: {text}<br>
        key: {key}<br>
        encrypted text: {encrypted_text}
        """
    except Exception as e:
        return f"Lỗi Playfair Encrypt: {str(e)}"


@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    try:
        text = request.form.get("inputCipherText", "").strip()
        key = request.form.get("inputKeyCipher", "").strip()

        playfair_cipher = PlayFairCipher()
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(text, playfair_matrix)

        return f"""
        <h3>Kết quả giải mã Playfair</h3>
        text: {text}<br>
        key: {key}<br>
        decrypted text: {decrypted_text}
        """
    except Exception as e:
        return f"Lỗi Playfair Decrypt: {str(e)}"


# ===================== RAILFENCE =====================
@app.route("/railfence")
def railfence():
    return render_template("railfence.html")


@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    try:
        text = request.form.get("inputPlainText", "").strip()
        key = int(request.form.get("inputKeyPlain", 0))

        railfence = RailFenceCipher()
        encrypted_text = railfence.rail_fence_encrypt(text, key)

        return f"""
        <h3>Kết quả mã hóa Rail Fence</h3>
        text: {text}<br>
        key: {key}<br>
        encrypted text: {encrypted_text}
        """
    except Exception as e:
        return f"Lỗi RailFence Encrypt: {str(e)}"


@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    try:
        text = request.form.get("inputCipherText", "").strip()
        key = int(request.form.get("inputKeyCipher", 0))

        railfence = RailFenceCipher()
        decrypted_text = railfence.rail_fence_decrypt(text, key)

        return f"""
        <h3>Kết quả giải mã Rail Fence</h3>
        text: {text}<br>
        key: {key}<br>
        decrypted text: {decrypted_text}
        """
    except Exception as e:
        return f"Lỗi RailFence Decrypt: {str(e)}"


# ===================== TRANSPOSITION =====================
@app.route("/transposition")
def transposition():
    return render_template("transposition.html")


@app.route("/transposition/encrypt", methods=["POST"])
def transposition_encrypt():
    try:
        text = request.form.get("inputPlainText", "").strip()
        key = int(request.form.get("inputKeyPlain", 0))

        transposition = TranspositionCipher()
        encrypted_text = transposition.encrypt(text, key)

        return f"""
        <h3>Kết quả mã hóa Transposition</h3>
        text: {text}<br>
        key: {key}<br>
        encrypted text: {encrypted_text}
        """
    except Exception as e:
        return f"Lỗi Transposition Encrypt: {str(e)}"


@app.route("/transposition/decrypt", methods=["POST"])
def transposition_decrypt():
    try:
        text = request.form.get("inputCipherText", "").strip()
        key = int(request.form.get("inputKeyCipher", 0))

        transposition = TranspositionCipher()
        decrypted_text = transposition.decrypt(text, key)

        return f"""
        <h3>Kết quả giải mã Transposition</h3>
        text: {text}<br>
        key: {key}<br>
        decrypted text: {decrypted_text}
        """
    except Exception as e:
        return f"Lỗi Transposition Decrypt: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)