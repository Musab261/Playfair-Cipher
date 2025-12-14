import tkinter as tk
from tkinter import scrolledtext
import random

alphabets = "abcdefghiklmnopqrstuvwxyz"   

def generate_random_key(length=10):
    return ''.join(random.sample(alphabets, length))

def create_key_matrix(key):
    key = key.lower().replace("j", "i")
    matrix = []
    used = []

    for ch in key:
        if ch in alphabets and ch not in used:
            used.append(ch)

    for ch in alphabets:
        if ch not in used:
            used.append(ch)

    for i in range(0, 25, 5):
        matrix.append(used[i:i+5])

    return matrix

def find_position(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j

def prepare_text(text):
    text = text.lower().replace("j", "i").replace(" ", "")
    prepared = ""
    i = 0

    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "x"

        if a == b:
            prepared += a + "x"
            i += 1
        else:
            prepared += a + b
            i += 2

    if len(prepared) % 2 != 0:
        prepared += "x"

    return prepared

def encoding(plain_text, matrix):
    cipher_text = ""
    for i in range(0, len(plain_text), 2):
        a, b = plain_text[i], plain_text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            cipher_text += matrix[r1][(c1+1)%5]
            cipher_text += matrix[r2][(c2+1)%5]
        elif c1 == c2:
            cipher_text += matrix[(r1+1)%5][c1]
            cipher_text += matrix[(r2+1)%5][c2]
        else:
            cipher_text += matrix[r1][c2]
            cipher_text += matrix[r2][c1]

    return cipher_text

def decoding(cipher_text, matrix):
    plain_text = ""
    for i in range(0, len(cipher_text), 2):
        a, b = cipher_text[i], cipher_text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            plain_text += matrix[r1][(c1-1)%5]
            plain_text += matrix[r2][(c2-1)%5]
        elif c1 == c2:
            plain_text += matrix[(r1-1)%5][c1]
            plain_text += matrix[(r2-1)%5][c2]
        else:
            plain_text += matrix[r1][c2]
            plain_text += matrix[r2][c1]

    return plain_text

def encode_text():
    global key_matrix, encrypted_text, random_key

    plain_text = input_text.get("1.0", tk.END).strip()
    if not plain_text:
        return

    random_key = generate_random_key()

    key_matrix = create_key_matrix(random_key)
    prepared_text = prepare_text(plain_text)
    encrypted_text = encoding(prepared_text, key_matrix)

    encrypted_box.delete("1.0", tk.END)
    encrypted_box.insert(tk.END, encrypted_text)

def decode_text():
    if not encrypted_text:
        return

    decoded_text = decoding(encrypted_text, key_matrix)

    decoded_box.delete("1.0", tk.END)
    decoded_box.insert(tk.END, decoded_text)

root = tk.Tk()
root.title("Playfair Cipher (Random Key)")

tk.Label(root, text="Enter Text:").pack()
input_text = scrolledtext.ScrolledText(root, height=8, width=100)
input_text.pack()

encode_btn = tk.Button(root, text="Encode", command=encode_text)
encode_btn.pack()

tk.Label(root, text="Encrypted Text:").pack()
encrypted_box = scrolledtext.ScrolledText(root, height=8, width=100)
encrypted_box.pack()

decode_btn = tk.Button(root, text="Decode", command=decode_text)
decode_btn.pack()

tk.Label(root, text="Decoded Text:").pack()
decoded_box = scrolledtext.ScrolledText(root, height=8, width=100)
decoded_box.pack()

root.mainloop()