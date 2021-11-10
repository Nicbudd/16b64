# interpreter for 16b64

# constants
# based on SHA-256 Hash of "16b64"
# 1c7214bcfc267e37b53f4fda20fe445ab76a25e582c06551b0e6c30483f36adc

import sys

v0 = 0x1c72
v1 = 0x14bc
v2 = 0xfc26
v3 = 0x7e37
v4 = 0xb53f
v5 = 0x4fda
v6 = 0x20fe
v7 = 0x445a
v8 = 0xb76a
v9 = 0x25e5

literals = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9]


# shift functionality
def shift(num, amount, dir):

    #Get hex part of number
    num = hex(int(num)).split('x')[-1]


    str = (bin(int(num, 16))[2:]).zfill(16)

    amount = amount % 16

    if (dir == 'r'):
        str = (str[16 - int(amount):] + str[0: 16 - int(amount)])

    else:
        str = (str[int(amount):] + str[0: int(amount)])

    return int(str, 2)


# main running function
def interpret(code):
    if code == None or code == "":
        return "Interpreter Error: No code to run."

    #print(code)

    loopstack = []
    stack = []
    flag = False

    returnString = ""

    # cycle through each instruction
    for i in range(len(code)):

        char = code[i]

        if char in ["0","1","2","3","4","5","6","7","8","9"]:
            stack.append(literals[int(char)])

        elif char == "A":
            x = stack.pop()
            y = stack.pop()
            stack.append(x&y)

        elif char == "C":
            x = stack.pop()
            y = x >> 8
            x %= 256
            returnString += chr(y) + chr(x)

        elif char == "D":
            stack.append(stack[-1])

        elif char == "L":
            x = stack.pop()
            y = stack.pop()
            stack.append(shift(y, x, "l"))

        elif char == "N":
            x = stack.pop()
            stack.append(x^0xffff)

        elif char == "O":
            x = stack.pop()
            y = stack.pop()
            stack.append(x|y)

        elif char == "R":
            x = stack.pop()
            y = stack.pop()
            stack.append(shift(y, x, "r"))

        elif char == "S":
            x = stack.pop()
            y = stack.pop()
            stack.append(x)
            stack.append(y)

        elif char == "U":
            x = stack.pop()
            returnString += chr(x)

        elif char == "X":
            x = stack.pop()
            y = stack.pop()
            stack.append(x^y)

        elif char == "a":
            x = stack.pop()
            y = stack.pop()
            sum = x+y

            if sum > 0xffff:
                sum -= 0x10000
                flag = True
            else:
                flag = False
            stack.append(sum)

        elif char == "b":
            x = stack[-1]

            if x % 2 == 0:
                flag = False
            else:
                flag = True

        elif char == "c":
            x = stack[-1]
            y = stack[-2]

            flag = x < y

        elif char == "d":
            x = stack.pop()

        elif char == "e":
            x = stack[-1]
            y = stack[-2]

            flag = x == y

        elif char == "g":
            x = stack[-1]
            y = stack[-2]

            flag = x > y

        elif char == "i":

            flag = not flag

        elif char == "l": #only if you're a little bitch
            x = stack.pop()
            stack.append(shift(x, 1, "l"))

        elif char == "r": #only if you're a little bitch
            x = stack.pop()
            stack.append(shift(x, 1, "r"))

        elif char == "(":
            loopstack.append(i)

        elif char == ")":
            if flag:
                i = loopstack.pop()

        else:
            return f"Unknown Char: {char}"


        list = ""
        for var in stack:
            list += format(int(var), "#018b") + ", "


    return returnString

def run():
    if sys.argv[1] == "-c":
        sys.stdout.write(interpret(sys.argv[2]) + "\n")
    else:
        for line in sys.argv[1]:
            sys.stdout.write(interpret(line) + "\n")


if __name__ == "__main__":
    run()
