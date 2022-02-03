# Nama : Muhammad Reza Nur Fauzi
# Nim  : 16519308

# Program GambarBTercermin
# Input: N : integer
# Output: Jika N > 0 dan ganjil, gambar B tercermin sesuai dengan N
#         Jika tidak, tampilkan pesan kesalahan: 

# KAMUS
# Variabel
#    N : int

def GambarBTercermin(N):
# I.S. N > 0 dan N ganjil
# F.S. Gambar B tercermin dengan lebar sebesar N sesuai spesifikasi soal
# Lengkapilah kamus lokal dan algoritma prosedur di bawah ini
    if N ==1:
        print('*')
    else:
        for i in range((N+1)//2,1,-1):
            print(((2*(((N+1)//2)-i)))*' ',end='')
            print(((2*i)-1)*'*',end='')
            print()
        for i in range(1,(N+1)//2):
            print(((2*(((N+1)//2)-i)))*' ',end='')
            print(((2*i)-1)*'*',end='')
            print()
        print('*'*N)
def IsValid(N):
# menghasilkan true jika N positif dan ganjil, false jika tidak
# Lengkapilah kamus lokal dan algoritma fungsi di bawah ini
    if N % 2 == 1 :
        return True
    else:
        return False

# ALGORITMA PROGRAM UTAMA
N = int(input())
if IsValid(N): # lengkapi dengan pemanggilan fungsi IsValid
    GambarBTercermin(N)  # lengkapi dengan pemanggilan prosedur GambarBTercermin
else: # N tidak positif atau N tidak ganjil
    print("Masukan tidak valid")