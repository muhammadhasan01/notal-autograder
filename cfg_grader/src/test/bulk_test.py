from os import listdir
# from tkinter import filedialog
from pycfg_ex import generate_cfg
from test import compare
from collapse_test import collapse
from cfg_grader.src.testcase.blackbox import blackbox
import xlsxwriter

class Result:
    def __init__(self, filename, examplefile, results):
        self.filename = filename
        self.examplefile = examplefile
        self.results = results

# class CompareResult:
#     def __init__(self, nim, whitescore, blackscore, whitediff, details):
#         self.nim = nim
#         self.whitescore = whitescore
#         self.blackscore = blackscore
#         self.diff = diff
#         self.details = details

# root = tk.Tk()
# root.withdraw()

filename = "segiempat.py"
testcasepath = "testcase/segiempat/"
# print(filename)
dir = "../4661 Praktikum 3 Shift 4 - 15.45-17.45"
# print(dir)
# filename = input("Enter filename: ")
# examplefile = input("Enter path to example file: ")
names = [f for f in listdir(dir)]
# print(names)

examplepath = "examples/segiempat/"
examplefiles = [f for f in listdir(examplepath)]
example_graphs = [collapse(generate_cfg(examplepath + examplefile)) for examplefile in examplefiles]
# results = []

workbook = xlsxwriter.Workbook('results/' + filename[:-3] + '.xlsx')
worksheet = workbook.add_worksheet()

for i in range(len(names)):
    nim = names[i].split()[0]
    test_file = dir +'/' + names[i] + '/' + filename
    try:
        whitescore = 0
        diff = ''
        details = ''
        test_graph = collapse(generate_cfg(test_file))
        for example_graph in example_graphs:
            temp_whitescore, temp_diff, temp_details = compare(example_graph, test_graph)
            if(temp_whitescore >= whitescore):
                whitescore = temp_whitescore
                diff = temp_diff
                details = temp_details
        
    except FileNotFoundError:
        whitescore = 0
        diff = '-'
        details = "File not found"

    except:
        whitescore = 0
        diff = '-'
        details = "Something went wrong"
    
    finally:
        blackscore = blackbox(testcasepath, test_file, 50)
        worksheet.write(i+1, 0, nim)
        worksheet.write(i+1, 1, whitescore)
        worksheet.write(i+1, 2, blackscore)
        worksheet.write(i+1, 3, diff)
        worksheet.write(i+1, 4, str(details))
        # result = {
        #     "nim" : nim,
        #     "whitescore" : whitescore,
        #     "blackscore" : blackscore,
        #     "diff" : diff,
        #     "details" : details
        # }
        # results.append(result)

    print(names[i])

# final_result = Result(filename, examplefile, results)

# with open('result.json', 'w') as output:
#     json.dump(final_result.__dict__, output, ensure_ascii=False, indent=4)

# output.close()

worksheet.write(0, 0, "NIM")
worksheet.write(0, 1, "Whitescore")
worksheet.write(0, 2, "Blackscore")
worksheet.write(0, 3, "Total Cost")
worksheet.write(0, 4, "Details")

# for i in range(len(results)):
#     result = results[i]
    

workbook.close()