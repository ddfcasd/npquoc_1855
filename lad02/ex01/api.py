from flask import Flask, render_template, request, jsonify
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher
from cipher.caesar import CaesarCipher

app = Flask(__name__)
caesar= CaesarCipher()

vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()
transposition_cipher = TranspositionCipher()


# ================= VIGENERE =================
@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    data = request.get_json()
    result = caesar.encrypt_text(data['plain_text'], int(data['key']))
    return jsonify({"result": result})


@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    data = request.get_json()
    result = caesar.decrypt_text(data['cipher_text'], int(data['key']))
    return jsonify({"result": result})


# ================= VIGENERE =================
@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.get_json()
    result = vigenere_cipher.vigenere_encrypt(data['plain_text'], data['key'])
    return jsonify({"result": result})


@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.get_json()
    result = vigenere_cipher.vigenere_decrypt(data['cipher_text'], data['key'])
    return jsonify({"result": result})


# ================= RAIL FENCE =================
@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.get_json()
    result = railfence_cipher.rail_fence_encrypt(data['plain_text'], int(data['key']))
    return jsonify({"result": result})


@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.get_json()
    result = railfence_cipher.rail_fence_decrypt(data['cipher_text'], int(data['key']))
    return jsonify({"result": result})


# ================= PLAYFAIR =================
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.get_json()
    result = playfair_cipher.playfair_encrypt(data['plain_text'], data['key'])
    return jsonify({"result": result})


@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.get_json()
    result = playfair_cipher.playfair_decrypt(data['cipher_text'], data['key'])
    return jsonify({"result": result})


# ================= TRANSPOSITION =================
@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    result = transposition_cipher.encrypt_message(int(data['key']), data['plain_text'])
    return jsonify({"result": result})


@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.get_json()
    result = transposition_cipher.decrypt_message(int(data['key']), data['cipher_text'])
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)