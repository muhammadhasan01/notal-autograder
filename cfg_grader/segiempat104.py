#NIM				: 16519104
#Nama				: Aisyah Farras Aqila
#Tanggal			: 4 Maret 2020
#Topik praktikum	: Python
#Deskripsi			: Problem 6

N=int(input())
C1=input()
C2=input()
if(N>0 and str(C1)!=str(C2)):
	print(str(C1)*N)
	if(N>1):
		if(N>2):
			for i in range(N-2):
				print(str(C1), end = '')
				print(str(C2)*(N-2), end = '')
				print(str(C1))
		print(str(C1)*N)
else:
	print("Masukan tidak valid")
