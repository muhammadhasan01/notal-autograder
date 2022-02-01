#NIM : 16519103
#Nama : Nur Mutmainnah Rahim
#Tanggal : 4 Maret 2020
#Topik praktikum: jumlah deret
#Deskripsi : membuat program yang menjumlahkan  nilai ganjil sampai N

#PROGRAM JUMLAH DERET
#program yang menjumlahkan semua bilangan ganjil sampai N

#KAMUS
#N: integer


#ALGORITMA
N= int(input(""))
sum=0
i=1

for i in range (1,N+1,2):
	sum=sum + i
	i=0+i
	
print(sum)




