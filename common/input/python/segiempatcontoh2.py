n = int(input())
c1 = input()
c2 = input()

if((n > 0) and (c1 != c2) and (len(c1) == 1) and (len(c2) == 1)):
    if(n == 1):
        print(c1)
    elif(n == 2):
        print(c1+c1)
        print(c1+c1)
    else:
        print(c1*n)
        for i in range(0, n-2):
            print(c1, end='')
            print(c2*(n-2), end='')
            print(c1)
        print(c1*n)

else:
    print("Masukan tidak valid")