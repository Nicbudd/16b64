import sys

fileIn = sys.argv[1]
fileOut = sys.argv[2]

bfCode = ""
b16 = "54O00X"

with open(fileIn) as file:
    for line in file:
        bfCode += line

for char in bfCode:
    if char == "+":
        b16 += "52ON a 14NAl M"
    elif char == "-":
        b16 += "54O a 14NAl M"
    elif char == "<":
        b16 += "z 54O e (00X i)"
    elif char == ">":
        b16 += "y 54O e (00X i)"
    elif char == ".":
        b16 += "D C"
    elif char == ",":
        b16 += "I 14NAl M"
    elif char == "[":
        b16 += "00Xed("
    elif char == "]":
        b16 += "00Xed)"

with open(fileOut, "w") as file:
    file.write(b16)