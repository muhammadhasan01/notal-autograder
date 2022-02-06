#NIM : 16519103
#Nama : Nur Mutmainnah Rahim
#Tanggal : 4 Maret 2020
#Topik praktikum: bentuk segiempat
#Deskripsi : membuat program yang hasilnya bentukan segiempat

#PROGRAM bentuk segiempat
#program yang menghasilkan bentuk segiempat

#KAMUS
#N: integer
#C1: char
#C2:char


#ALGORITMA
N= int(input(""))
C1=input('')
C2=input('')

if (N==1) and (C1!=C2) :
	print(C1)
elif (N>1) and (C1!=C2) :
	print(C1*N)
	for i in range (N-2):
		print(C1 , end ='' )
		print (C2*(N-2) , end='')
		print(C1)
	print(C1*N)
else:
	print("Masukan tidak valid")

	
