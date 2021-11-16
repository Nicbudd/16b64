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
def interpret(source, stdin, flags=""):

    debug = "d" in flags
    safe = "s" in flags

    # input handling
    if source is None or source == "":
        return "Interpreter Error: No code to run.\n"

    # remove comments
    source = source.split("\n")
    source = [re.search(r"^([^#]*)#?.*$", x).group(1) for x in source]

    code = "".join("".join(source).split())


    # define variables used in execution
    stack = []
    loopStack = []  # list of pointers back to beginning of loop
    flag = False
    skip = False
    parenthesis = 0
    returnString = ""
    loopIterations = 0
    #readPos = 1 # how far we are into reading stdin


    # cycle through each instruction
    # not a for loop as we might end up back where we started
    i = 0
    while i < len(code):

        # single instruction is put in char
        char = code[i]

        if debug:
            sys.stdout.write(f"{i:>3}: {char} {loopStack} {str(flag).ljust(5)} "
                             f"{str(skip).ljust(5)} {[f'0x{i:04x}' for i in stack]}\n")

        # Start loop if flag
        if char == "(":
            if not flag:
                skip = True

            if skip:
                parenthesis += 1
            else:
                loopStack.append(i)

        # Loop if flag
        elif char == ")":
            if skip:
                parenthesis -= 1
                if parenthesis == 0:
                    skip = False

            else:
                if safe and loopIterations > 10000:
                    return f"Interpreter Error: Too many loop repetitions.\n"
                elif flag:
                    loopIterations += 1
                    i = loopStack.pop() - 1
                else:
                    loopStack.pop()


        if not skip:

            # add literals to the stack
            if char in ["0","1","2","3","4","5","6","7","8","9"]:
                stack.append(literals[int(char)])

            # FUNCTIONS
            # AND
            elif char == "A":
                x = stack.pop()
                y = stack.pop()
                stack.append(x & y)

            # ASCII PRINT
            elif char == "C":
                x = stack.pop()
                y = x >> 8
                x %= 256
                returnString += chr(y) + chr(x)

            # DUPLICATE
            elif char == "D":
                stack.append(stack[-1])

            # FIND FROM STACK
            elif char == "F":
                x = stack.pop()
                try:
                    y = stack.pop(-x)
                except:
                    flag = False
                else:
                    flag = True
                    stack.append(y)

            # READ STDIN
            elif char == "H":
                h = ord(stdin.read(1))
                j = ord(stdin.read(1))
                k = ord(stdin.read(1))
                stack.append(h)
                stack.append((j << 8) + k)

            elif char == "I":
                h = ord(stdin.read(1))
                j = ord(stdin.read(1))
                stack.append((h << 8) + j)

            elif char == "J":
                h = ord(stdin.read(1))
                stack.append(h)

            # SHIFT LEFT BY AMOUNT
            elif char == "L":
                x = stack.pop()
                y = stack.pop()
                stack.append(shift(y, x, "l"))

            # MODULO
            elif char == "M":
                x = stack.pop()
                y = stack.pop()
                stack.append(y % x)

            # NOT
            elif char == "N":
                x = stack.pop()
                stack.append(x ^ 0xffff)

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

            # Find from stack: 4 bit
            elif char == "f":
                x = stack.pop() % 16
                try:
                    y = stack.pop(-x)
                except:
                    flag = False
                else:
                    flag = True
                    stack.append(y)


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

            # Move from bottom of stack to top of stack
            elif char == "y":
                stack.append(stack.pop(0))

            # Move to bottom of stack
            elif char == "z":
                stack.insert(0, stack.pop())



            # we recognize this character, but we're dealing with it above
            elif char in "()":
                pass
            # Otherwise there's a character we don't recognize, return error.
            else:
                return f"Interpreter Error: Unknown Char \"{char}\"\n"

        # list = ""
        # for var in stack:
        #     list += format(int(var), "#018b") + ", "

        i += 1

    return returnString

def run():
    # Figure out what to do with the command line args

    flags = ""
    for x in sys.argv:
        if x[0] == "-":
            flags += x[1:]

    #print(flags)

    # No arguments
    if len(sys.argv) <= 1:
        if sys.stdin is None:
            sys.stdout.write("No arguments given")
        else:
            sys.stdout.write(interpret(sys.stdin.readline(), None, flags=flags))

    elif "." in sys.argv[-1]:
        with open(sys.argv[-1]) as file:
            program = ""

            for line in file:
                program += line

            sys.stdout.write(interpret(program, sys.stdin, flags=flags))

    else:
        sys.stdout.write(interpret(sys.argv[-1], sys.stdin, flags=flags))


if __name__ == "__main__":
    run()
