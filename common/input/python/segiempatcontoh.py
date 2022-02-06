n = int(input())
c1 = input()
c2 = input()

if((n == 1) and (c1 != c2) and (len(c1) == 1) and (len(c2) == 1)):
    print(c1)
elif((n > 1) and (c1 != c2) and (len(c1) == 1) and (len(c2) == 1)):
    for i in range(n):
        if((i == 0) or (i == n-1)):
            for j in range(n-1):
                print(c1, end='')
            print(c1)
        else:
            print(c1, end='')
            for j in range(n-2):
                print(c2, end='')
            print(c1)
else:
    print("Masukan tidak valid")