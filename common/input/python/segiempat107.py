# Nama : Ezra Faiyaz Syahnatama
# NIM : 16519107

# Program jumlahderet
# membaca N (sebuah integer) berikut C1 dan C2 (dua buah karakter), dan kemudian menuliskan bentuk dengan syarat N>0 dan C1 tidak sama dengan C2.

# KAMUS
# N : Int
#C1, C2 : Char

# ALGORITMA
N=int(input())
C1=input()
C2=input()
if N>0 and C1!=C2:
	if N==1:
		print(C1)
	elif N==2:
		print(C1+C1)
		print(C1+C1)
	else:
		print(N*C1)
		for i in range(0,N-2):
			print(C1+((N-2)*C2)+C1)
		print(N*C1)
else:
	print("Masukan tidak valid")