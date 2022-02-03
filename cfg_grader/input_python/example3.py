x = 1
y = 1
if(x < 3):
    for i in range(2):
        x += 1
    z = x + y
    print("yes")
else:
    z = x - y
    print("no")
print(z)