# Autorem tego zadania jest Szymon Wątorowski

import os
import sys
from sympy import mod_inverse

alfabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

# Funkcja pomocnicza do odczytywania pliku
def readFile(filename):
    try:
        with open(filename, "r") as file:
            return file.read().lower()
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {filename}.")
        sys.exit(1)

# Funkcja zapisująca do pliku
def writeFile(filename, content):
    try:
        with open(filename, "w") as file:
            file.write(content)
    except OSError as e:
        print(f"Wystąpił błąd podczas zapisywania: {e}")
        sys.exit(1)

# Szyfr Cezara (szyfrowanie i odszyfrowywanie)
def eCezar(k, x):
    result = []
    for char in x:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result.append(chr((ord(char) - offset + k) % 26 + offset))
        else:
            result.append(char)
    return "".join(result)

def dCezar(k, y):
    return eCezar(-k, y)

# Szyfr Afiniczny (szyfrowanie i odszyfrowywanie)
def eAfiniczny(a, b, x):
    result = []
    for char in x:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            i = ord(char) - offset
            result.append(chr((a * i + b) % 26 + offset))
        else:
            result.append(char)
    return "".join(result)

def dAfiniczny(a, b, y):
    if gcd(a, 26) != 1:
        print(f"Nie można znaleźć odwrotności dla a = {a} modulo 26, ponieważ NWD(a, 26) != 1.")
        sys.exit(1)

    a_inv = mod_inverse(a, 26)  # Obliczenie odwrotności a modulo 26
    if a_inv is None:
        print(f"Brak odwrotności dla 'a' w modulo 26.")
        sys.exit(1)

    result = []
    for char in y:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            i = ord(char) - offset
            result.append(chr((a_inv * (i - b)) % 26 + offset))
        else:
            result.append(char)
    return "".join(result)

# Kryptoanaliza z pomocą tekstu jawnego
def kryptoanalizaJawnym(x, y):
    with open("decrypt.txt", "w") as file:
        for k in range(1, 26):
            decrypted = dCezar(k, y)
            print(decrypted)
            if x in decrypted:
                writeFile("key-found.txt", str(k))
                file.write(decrypted)
                print(f"Klucz znaleziony: {k}")
                return
        print("Nie udało się znaleźć klucza za pomocą kryptoanalizy jawnego tekstu.")
        sys.exit(1)

# Kryptoanaliza bez pomocy tekstu jawnego (sprawdzanie wszystkich możliwych kluczy)
def kryptoanalizaBezJawnym(y):
    with open("decrypt.txt", "w") as file:
        for k in range(1, 26):
            decrypted = dCezar(k, y)
            file.write(f"\n{decrypted}\n\n")  # Zapisuje odszyfrowany tekst z kluczem w nagłówku
    print("Wszystkie możliwe odszyfrowane teksty zapisano w pliku 'decrypt.txt'.")


def kryptoanalizaAfinicznaBezJawnym(y):
    with open("decrypt.txt", "w") as file:
        for a in range(1, 26):
            if gcd(a, 26) == 1:
                for b in range(26):
                    decrypted = dAfiniczny(a, b, y)
                    file.write(f"{decrypted}\n\n")
        print("Wszystkie możliwe odszyfrowane teksty zapisano w plikach.")

# Funkcja obliczająca NWD (największy wspólny dzielnik)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Wykonanie akcji w zależności od argumentów
if len(sys.argv) < 3:
    sys.exit(1)

if sys.argv[1] == "-c":  # Szyfr Cezara
    if sys.argv[2] == "-e":
        print("Szyfrowanie Cezara")
        plaintext = readFile("plain.txt")
        key = int(readFile("key.txt").split()[0])  # Pierwsza liczba w kluczu
        encrypted = eCezar(key, plaintext)
        writeFile("crypto.txt", encrypted)

    elif sys.argv[2] == "-d":
        print("Odszyfrowywanie Cezara")
        ciphertext = readFile("crypto.txt")
        key = int(readFile("key.txt").split()[0])
        decrypted = dCezar(key, ciphertext)
        writeFile("decrypt.txt", decrypted)

    elif sys.argv[2] == "-j":
        print("Kryptoanaliza z tekstem jawnym")
        plaintext = readFile("extra.txt")
        ciphertext = readFile("crypto.txt")
        kryptoanalizaJawnym(plaintext, ciphertext)

    elif sys.argv[2] == "-k":
        print("Kryptoanaliza bez pomocy tekstu jawnego")
        ciphertext = readFile("crypto.txt")
        kryptoanalizaBezJawnym(ciphertext)

elif sys.argv[1] == "-a":  # Szyfr Afiniczny
    if sys.argv[2] == "-e":
        print("Szyfrowanie Afiniczne")
        plaintext = readFile("plain.txt")
        key = readFile("key.txt").split()
        a, b = int(key[0]), int(key[1])
        encrypted = eAfiniczny(a, b, plaintext)
        writeFile("crypto.txt", encrypted)

    elif sys.argv[2] == "-d":
        print("Odszyfrowywanie Afiniczne")
        ciphertext = readFile("crypto.txt")
        key = readFile("key.txt").split()
        a, b = int(key[0]), int(key[1])
        decrypted = dAfiniczny(a, b, ciphertext)
        writeFile("decrypt.txt", decrypted)

    elif sys.argv[2] == "-j":
        print("Kryptoanaliza z tekstem jawnym dla szyfru Afinicznego")
        plaintext = readFile("plain.txt")
        ciphertext = readFile("crypto.txt")
        kryptoanalizaJawnym(plaintext, ciphertext)

    elif sys.argv[2] == "-k":
        print("Kryptoanaliza bez pomocy tekstu jawnego dla szyfru Afinicznego")
        ciphertext = readFile("crypto.txt")
        kryptoanalizaAfinicznaBezJawnym(ciphertext)

else:
    sys.exit(1)
