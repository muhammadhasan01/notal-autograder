import subprocess

def blackbox(testcasepath, codepath, testcasenum):
    
    # codepath = "../4661 Praktikum 3 Shift 4 - 15.45-17.45/16519118 Zarfa Naida Pratista/segiempat.py"
    # codepath = "../4661 Praktikum 3 Shift 4 - 15.45-17.45/16519103 Nur Mutmainnah Rahim/segiempat.py"
    error = False
    try:
        codefile = open(codepath, 'r')
        correct = 0
        for i in range(testcasenum):
            
            inputfile = testcasepath + "input" + str(i+1) + ".txt"
            infile = open(inputfile, 'r')
            command = ['python3', codepath]
            output = subprocess.check_output(command, input=infile.read().encode(), timeout=2)
            outputfile = testcasepath + "output" + str(i+1) + ".txt"
            outfile = open(outputfile, 'r')
            # print("Testcase " + str(i+1) + " : ", end='')
            
            if(outfile.read().rstrip() == output.decode().rstrip()):
                correct += 1
                # print("100")
                # print(outfile.read().rstrip())
                # print(output.decode().rstrip())
            # else:
                # print("0")

            infile.close()
            outfile.close()
        
    except:
        error = True
        # print("Testcase " + str(i+1) + " : Error")

    
    if(not(error)):
        codefile.close()
        return ((correct/testcasenum)*100)
    else:
        return 0