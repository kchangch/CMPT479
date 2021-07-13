from Crypto.Cipher import AES

key = b'you saw nothing!'
iv = b'CMPT 479 test iv'
msg = bytearray(b'Eat my fat ass')
roundup = int((len(msg)+1)/16) * 16 + 16

diff = roundup - len(msg)

while len(msg) < roundup:
    msg.append(diff)

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(bytes(msg))

f = open("ciphertext", "wb")
f.write(iv)
f.write(ciphertext)
f.close()
