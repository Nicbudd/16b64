# interpreter for 16b64

# constants
# based on SHA-256 Hash of "16b64"
# 1c7214bcfc267e37b53f4fda20fe445ab76a25e582c06551b0e6c30483f36adc

import sys
import re

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
def shift(num, amount, direction):

    # Please refactor this section this is bad omg

    # Get hex part of number in string
    num = hex(int(num)).split('x')[-1]
    # Get binary part of number
    str = (bin(int(num, 16))[2:]).zfill(16)

    # Shift amount mod 16 to remove redundant shifts
    amount = amount % 16

    # if shifting right
    if direction == 'r':
        # str = right side + left side
        str = (str[16 - int(amount):] + str[0: 16 - int(amount)])

    else:
        # str = right side + left side
        str = (str[int(amount):] + str[0: int(amount)])

    return int(str, 2)


# main running function
def interpret(code, debug=False):

    # input handling
    if code is None or code == "":
        return "Interpreter Error: No code to run."

    # remove comments
    code = code.split("\n")
    code = [re.search(r"^([^\#]*)\#?.*$", x).group(1) for x in code]

    # define variables used in execution
    stack = []
    loopStack = []  # list of pointers back to beginning of loop
    flag = False

    returnString = ""

    #print(code)

    for line in code:
        line = line.strip().replace(" ", "")

        # cycle through each instruction
        for i in range(len(line)):

            # single instruction is put in char
            char = line[i]

            if debug:
                sys.stdout.write(f"{char} {stack}\n")

            # add literals to the stack
            if char in ["0","1","2","3","4","5","6","7","8","9"]:
                stack.append(literals[int(char)])

            # FUNCTIONS
            # AND
            elif char == "A":
                x = stack.pop()
                y = stack.pop()
                stack.append(x&y)

            # ASCII PRINT
            elif char == "C":
                x = stack.pop()
                y = x >> 8
                x %= 256
                returnString += chr(y) + chr(x)

            # DUPLICATE
            elif char == "D":
                stack.append(stack[-1])

            # SHIFT LEFT BY AMOUNT
            elif char == "L":
                x = stack.pop()
                y = stack.pop()
                stack.append(shift(y, x, "l"))

            # NOT
            elif char == "N":
                x = stack.pop()
                stack.append(x^0xffff)

            # OR
            elif char == "O":
                x = stack.pop()
                y = stack.pop()
                stack.append(x|y)

            # Shift right by y
            elif char == "R":
                x = stack.pop()
                y = stack.pop()
                stack.append(shift(y, x, "r"))

            # Swap two stack pieces
            elif char == "S":
                x = stack.pop()
                y = stack.pop()
                stack.append(x)
                stack.append(y)

            # One word unicode code point
            elif char == "U":
                x = stack.pop()
                returnString += chr(x)

            # Two word unicode code point
            elif char == "V":
                x = stack.pop()
                y = stack.pop() << 16
                returnString += chr(y + x)

            # XOR
            elif char == "X":
                x = stack.pop()
                y = stack.pop()
                stack.append(x^y)

            # Add, set flag if overflow
            elif char == "a":
                x = stack.pop()
                y = stack.pop()
                sum = x+y

                flag = sum > 0xffff
                sum %= 2**16

                stack.append(sum)

            # Sets flag true if even, false if not
            elif char == "b":
                x = stack[-1]

                if x % 2 == 0:
                    flag = False
                else:
                    flag = True

            # Less than
            elif char == "c":
                x = stack[-1]
                y = stack[-2]

                flag = x < y

            # Delete
            elif char == "d":
                x = stack.pop()

            # Equal
            elif char == "e":
                x = stack[-1]
                y = stack[-2]

                flag = x == y

            # Greater than
            elif char == "g":
                x = stack[-1]
                y = stack[-2]

                flag = x > y

            # Invert flag
            elif char == "i":
                flag = not flag

            # Shift left
            elif char == "l": #only if you're a little bitch
                x = stack.pop()
                stack.append(shift(x, 1, "l"))

            # Shift right
            elif char == "r": #only if you're a little bitch
                x = stack.pop()
                stack.append(shift(x, 1, "r"))

            # Start loop
            elif char == "(":
                loopStack.append(i)

            # Loop if flag
            elif char == ")":
                if flag:
                    i = loopStack.pop()
                else:
                    loopStack.pop()

            # Otherwise there's a character we don't recognize, return error.
            else:
                return f"Interpreter Error: Unknown Char \"{char}\""

            # list = ""
            # for var in stack:
            #     list += format(int(var), "#018b") + ", "


    return returnString

def run():
    # Figure out what to do with the command line args

    flags = ""

    for x in sys.argv:
        if x[0] == "-":
            flags += x[1:]

    #print(flags)
    debug = "d" in flags

    # No arguments
    if len(sys.argv) <= 1:
        if sys.stdin is None:
            sys.stdout.write("No arguments given")
        else:
            sys.stdout.write(interpret(sys.stdin.readline(), debug))

    elif "." in sys.argv[-1]:
        with open(sys.argv[-1]) as file:
            program = ""

            for line in file:
                program += line

            sys.stdout.write(interpret(program, debug))

    else:
        sys.stdout.write(interpret(sys.argv[-1], debug))


if __name__ == "__main__":
    run()
