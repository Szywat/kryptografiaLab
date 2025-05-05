# Autorem zadania jest Szymon Wątorowski

import sys

def prepare():
    with open("orig.txt", "r", encoding="utf-8") as f:
        text = f.read()
        text = ' '.join(text.splitlines())
        filtered_text = ''.join(char for char in text if char.isalpha() or char.isspace()).lower()
    lines = []
    for i in range(0, len(text), 64):
        line = filtered_text[i:i+64]
        if len(line) == 64:
            lines.append(line)
    with open("plain.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def encrypt():
    with open("plain.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    with open("key.txt", "r", encoding="utf-8") as f:
        key = f.read().strip()
    if len(key) < 64:
        print("Klucz nie ma 64 znaków")
        sys.exit(1)
    key_bytes = key.encode()
    crypto = []
    for line in lines:
        c = bytes([ord(ch) ^ key_bytes[i] for i, ch in enumerate(line)])
        crypto.append(c.hex())
    with open("crypto.txt", "w") as f:
        f.write("\n".join(crypto))

def xor_bytes(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, b2)])

def analyze():
    with open("crypto.txt", "r") as f:
        hex_lines = [bytes.fromhex(line.strip()) for line in f if line.strip()]
    n = len(hex_lines)
    length = len(hex_lines[0])
    possible_space_positions = [set() for _ in range(n)]

    space_counters = [[0] * length for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            xored = xor_bytes(hex_lines[i], hex_lines[j])
            for k in range(length):
                print(xored)
                if 65 <= xored[k] <= 90:  # A-Z
                    space_counters[i][k] += 1
                    space_counters[j][k] += 1

    possible_spaces = [set() for _ in range(n)]
    for i in range(n):
        for k in range(length):
            if space_counters[i][k] > 7:  # wartość zależna od liczby wiadomości
                possible_spaces[i].add(k)

    key = [None] * length
    for i in range(n):
        for k in possible_spaces[i]:
            key[k] = hex_lines[i][k] ^ 0x20  # bo spacja ⊕ c = k

    guesses = []
    for i in range(n):
        line = []
        for k in range(length):
            if key[k] is not None:
                char = chr(hex_lines[i][k] ^ key[k])
                if 97 <= ord(char) <= 122 or char == " ":
                    line.append(char)
                else:
                    line.append("_")
            else:
                line.append("_")
        guesses.append("".join(line))

    with open("decrypt.txt", "w", encoding="utf-8") as f:
        for g in guesses:
            f.write("".join(g) + "\n")

if len(sys.argv) < 2:
    print("Nie podano opcji [-p|-e|-k]")
    sys.exit(1)

if sys.argv[1] == "-p":
   prepare()
   print("Linie tekstu zostały wyrównane do 64 znaków i zapisane w pliku plain.txt")
elif sys.argv[1] == "-e":
    encrypt()
    print("Zaszyfrowano tekst")
elif sys.argv[1] == "-k":
    analyze()
    print("Przeprowadzono kryptoanalizę")
else:
    print("Podaj opcję [-p|-e|-k]")
    sys.exit(1)