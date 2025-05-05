# Autorem rozwiązania zadania jest Szymon Wątorowski

tablica = []
with open("hash.txt","r") as f:
    plik = f.readlines()
    for i in range(len(plik)):
        tablica.append(plik[i][:-4])

for i in range(len(tablica)):
    if i % 2 == 0:
        n1 = int(tablica[i], 16)
        n2 = int(tablica[i+1], 16)
        bit_diff = bin(n1 ^ n2).count('1')
        total_bits = len(tablica[i]) * 4
        for_procent = total_bits * 100
        procent = ((bit_diff / total_bits) * 100)
        print(f"Liczba różniących się bitów: {bit_diff} z {total_bits}, procentowo: {procent:.0f} %")
