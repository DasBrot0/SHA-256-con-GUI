import hashlib

# Texto de entrada
texto = "hola"

# Convertir el texto a bytes
texto_bytes = texto.encode('utf-8')

# Calcular el hash SHA-256
hash_objeto = hashlib.sha256(texto_bytes)

# Obtener el hash en formato hexadecimal
hash_hex = hash_objeto.hexdigest()

print("Texto:", texto)
print("Hash SHA-256:", hash_hex)