N = int(input())
C1 = str(input())
C2 = str(input())

if N<=0:
	print("Masukan tidak valid")
elif C1==C2:
	print("Masukan tidak valid")
else:
	for i in range(N):
			if i==0 or i == N-1:
				print(str(C1*N))
			else:
				print(str(C1 + C2*(N-2) + C1))