from flask import Flask, render_template, request
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()
transposition_cipher = TranspositionCipher()

@app.route('/')
def home():
    return render_template('index.html')

# ================= VIGENERE =================
@app.route('/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    plain_text = request.form['plain_text']
    key = request.form['key']
    result = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return render_template('index.html', result=result, cipher_name='Vigenere Encrypt')

@app.route('/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    cipher_text = request.form['cipher_text']
    key = request.form['key']
    result = vigenere_cipher.vigenere_decrypt(cipher_text, key)
    return render_template('index.html', result=result, cipher_name='Vigenere Decrypt')

# ================= RAIL FENCE =================
@app.route('/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    plain_text = request.form['plain_text']
    key = int(request.form['key'])
    result = railfence_cipher.rail_fence_encrypt(plain_text, key)
    return render_template('index.html', result=result, cipher_name='Rail Fence Encrypt')

@app.route('/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    cipher_text = request.form['cipher_text']
    key = int(request.form['key'])
    result = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    return render_template('index.html', result=result, cipher_name='Rail Fence Decrypt')

# ================= PLAYFAIR =================
@app.route('/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    plain_text = request.form['plain_text']
    key = request.form['key']
    result = playfair_cipher.playfair_encrypt(plain_text, key)
    return render_template('index.html', result=result, cipher_name='Playfair Encrypt')

@app.route('/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    cipher_text = request.form['cipher_text']
    key = request.form['key']
    result = playfair_cipher.playfair_decrypt(cipher_text, key)
    return render_template('index.html', result=result, cipher_name='Playfair Decrypt')

# ================= TRANSPOSITION =================
@app.route('/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    plain_text = request.form['plain_text']
    key = int(request.form['key'])
    result = transposition_cipher.encrypt_message(key, plain_text)
    return render_template('index.html', result=result, cipher_name='Transposition Encrypt')

@app.route('/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    cipher_text = request.form['cipher_text']
    key = int(request.form['key'])
    result = transposition_cipher.decrypt_message(key, cipher_text)
    return render_template('index.html', result=result, cipher_name='Transposition Decrypt')

if __name__ == '__main__':
    app.run(debug=True)