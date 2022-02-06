import random
import subprocess

char1 = '*'
char2 = '#'
path = "segiempat/"

# Input file
# values = random.sample(range(1,50), 45)

# for i in range(45):
#     filename = path + "input" + str(i+1) + ".txt" 
#     inputfile = open(filename, 'w')
#     inputfile.write("{}\n{}\n{}\n".format(values[i],char1,char2))
#     inputfile.close()

# Output file
for i in range(50):
    inputfile = path + "input" + str(i+1) + ".txt"
    infile = open(inputfile, 'r')
    command = ['python3', 'segiempatcontoh.py']
    output = subprocess.check_output(command, input=infile.read().encode(), timeout=2)
    outputfile = path + "output" + str(i+1) + ".txt"
    outfile = open(outputfile, 'w')
    outfile.write(str(output.decode()))
    infile.close()
    outfile.close()
