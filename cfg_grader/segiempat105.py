# NIM		 		: 16519105
# Nama 				: Fadli Naufal Rahman
# Tanggal 			: 4 Maret 2020
# Topik praktikum 	: Phython
# Deskripsi 		: Segi Empat

N=int(input())
C1=input()
C2=input()

if (N<=0 or C1==C2) :
	print ("Masukan tidak valid")
for i in range (1,N+1):
	for j in range (1,N+1):
		if (i==1 or j==1 or i==N or j==N):
			print (C1, end = "")
		else :
			print (C2, end = "")
	print()
		

