import os
import json
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, session, url_for
import hashlib

# --- Constantes SHA-256 ---
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Funcion rotate right corregida
def _rotate_right(num, shift, size=32):
    return (num >> shift) | ((num << (size-shift)) & (2**size-1))

def _sigma0(x):
    return _rotate_right(x, 7) ^ _rotate_right(x, 18) ^ (x >> 3)
def _sigma1(x):
    return _rotate_right(x, 17) ^ _rotate_right(x, 19) ^ (x >> 10)
def _capsigma0(x):
    return _rotate_right(x, 2) ^ _rotate_right(x, 13) ^ _rotate_right(x, 22)
def _capsigma1(x):
    return _rotate_right(x, 6) ^ _rotate_right(x, 11) ^ _rotate_right(x, 25)
def _ch(x,y,z):
    return (x & y) ^ (~x & z)
def _maj(x,y,z):
    return (x & y) ^ (x & z) ^ (y & z)

def generate_hash(message, step=False):
    """
    Retorna tupla (hash_bytes, rounds) donde rounds es lista de
    dicts {'round':i,'a':..,'b':..,...,'h':..} si step=True, o None.
    """
    # convertir a bytearray
    if isinstance(message, str):
        msg = bytearray(message, 'ascii')
    elif isinstance(message, (bytes, bytearray)):
        msg = bytearray(message)
    else:
        raise TypeError("Tipo no soportado para hashing")

    # --- Padding ---
    bit_len = len(msg) * 8
    msg.append(0x80)
    while (len(msg)*8 + 64) % 512 != 0:
        msg.append(0)
    msg += bit_len.to_bytes(8, 'big')

    # dividir en bloques de 64 bytes
    blocks = [msg[i:i+64] for i in range(0, len(msg), 64)]

    # valores iniciales
    h0, h1, h2, h3 = 0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a
    h4, h5, h6, h7 = 0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19

    rounds = [] if step else None

    for block in blocks:
        # preparar schedule
        W = [int.from_bytes(block[i*4:(i*4)+4], 'big') for i in range(16)]
        for t in range(16,64):
            val = (_sigma1(W[t-2]) + W[t-7] + _sigma0(W[t-15]) + W[t-16]) & 0xFFFFFFFF
            W.append(val)

        a,b,c,d,e,f,g,h = h0,h1,h2,h3,h4,h5,h6,h7

        # iterar rondas
        for t in range(64):
            T1 = (h + _capsigma1(e) + _ch(e,f,g) + K[t] + W[t]) & 0xFFFFFFFF
            T2 = (_capsigma0(a) + _maj(a,b,c)) & 0xFFFFFFFF
            h = g; g = f; f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c; c = b; b = a
            a = (T1 + T2) & 0xFFFFFFFF

            if step:
                rounds.append({
                    'round': t+1,
                    'a': hex(a), 'b': hex(b), 'c': hex(c), 'd': hex(d),
                    'e': hex(e), 'f': hex(f), 'g': hex(g), 'h': hex(h)
                })

        # actualizar hash intermedio
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    digest = b''.join(hv.to_bytes(4,'big') for hv in (h0,h1,h2,h3,h4,h5,h6,h7))
    return digest, rounds

# --- Configuración Flask ---
app = Flask(__name__)
app.secret_key = 'cambiá_esto_por_una_clave_segura'
UPLOAD_FOLDER = 'uploads'
HISTORY_FILE = 'history.json'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_history():
    if os.path.exists(HISTORY_FILE):
        return json.load(open(HISTORY_FILE,'r'))
    return {'entries': []}

def save_history(data):
    with open(HISTORY_FILE,'w') as f:
        json.dump(data, f, indent=2)

@app.route('/', methods=['GET','POST'])
def index():
    history = load_history()
    
    if request.method == 'POST':
        modo = request.form.get('mode')
        paso = request.form.get('step') == 'on'
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = {}

        if modo == 'text':
            txt = request.form.get('text','')
            raw, rounds = generate_hash(txt, paso)
            hs = raw.hex()
            history['entries'].append({'tipo':'Texto','input':txt,'hash':hs,'time':ts})
            result = {'hash':hs,'time':ts,'rounds':rounds}

        else:  # archivo
            f = request.files.get('file')
            if f and f.filename:
                ruta = os.path.join(UPLOAD_FOLDER, f.filename)
                f.save(ruta)
                contenido = open(ruta,'rb').read()
                raw, rounds = generate_hash(contenido, paso)
                hs = raw.hex()
                history['entries'].append({'tipo':'Archivo','input':f.filename,'hash':hs,'time':ts})
                result = {'hash':hs,'time':ts,'rounds':rounds,'file':f.filename}
            else:
                flash("No seleccionaste ningún archivo.")
                return redirect(url_for('index'))

        save_history(history)
        session['result'] = result
        return redirect(url_for('index'))

    result = session.pop('result', {})
    return render_template('index.html', result=result, history=history)

if __name__ == '__main__':
    app.run(debug=True)