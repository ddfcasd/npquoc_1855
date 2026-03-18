from flask import Flask, render_template, request, jsonify
import os

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = "123456"


@app.route("/")
def home():
    return render_template("index.html")


# ===================== CAESAR WEB =====================
@app.route("/caesar")
def caesar():
    return render_template("caesar.html")


@app.route("/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form.get("inputPlainText", "")
    key = int(request.form.get("inputKeyPlain", 0))
    result = CaesarCipher().encrypt_text(text, key)
    return f"Encrypted: {result}"


@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form.get("inputCipherText", "")
    key = int(request.form.get("inputKeyCipher", 0))
    result = CaesarCipher().decrypt_text(text, key)
    return f"Decrypted: {result}"


# ===================== CAESAR API =====================
@app.route("/api/caesar/encrypt", methods=["POST"])
def api_caesar_encrypt():
    data = request.get_json(silent=True) or {}
    text = data.get("plain_text", "")
    key = int(data.get("key", 0))
    result = CaesarCipher().encrypt_text(text, key)
    return jsonify({"encrypted_text": result})


@app.route("/api/caesar/decrypt", methods=["POST"])
def api_caesar_decrypt():
    data = request.get_json(silent=True) or {}
    text = data.get("cipher_text", "")
    key = int(data.get("key", 0))
    result = CaesarCipher().decrypt_text(text, key)
    return jsonify({"decrypted_text": result})


# ===================== VIGENERE =====================
@app.route("/vigenere")
def vigenere():
    return render_template("vigenere.html")


@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")
    result = VigenereCipher().encrypt_text(text, key)
    return f"Encrypted: {result}"


@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")
    result = VigenereCipher().decrypt_text(text, key)
    return f"Decrypted: {result}"


# ===================== PLAYFAIR =====================
@app.route("/playfair")
def playfair():
    return render_template("playfair.html")


@app.route("/api/playfair/creatematrix", methods=["POST"])
def playfair_creatematrix():
    data = request.get_json(silent=True) or {}
    key = data.get("key", "")
    matrix = PlayFairCipher().create_playfair_matrix(key)
    return jsonify({"playfair_matrix": matrix})


# ===================== RAILFENCE =====================
@app.route("/railfence")
def railfence():
    return render_template("railfence.html")


# ===================== TRANSPOSITION =====================
@app.route("/transposition")
def transposition():
    return render_template("transposition.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)