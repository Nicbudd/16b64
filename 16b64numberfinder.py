# Currently broken

import i16b64

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

def lenSortFunc(e):
    return e['len']

def constOrderFunc(e):
    return e['const']


def main2():

    # object with constants
    constants = []

    # put object inside for each function
    for x in range(2 ** 16):
        constants.append({"const": x, "len": float('inf'), "seq": []})

    for x in literals:
        seq = str(literals.index(x))
        constants[x]["len"] = 1
        constants[x]["seq"].append(seq)

    for iteration in range(2):

        lenSortedConstants = sorted(constants, key=lenSortFunc)
        knownConstants = [c for c in lenSortedConstants if c["len"] < float('inf')]

        for const in knownConstants:

            for instr in "Nlr":
                seedSeq = const["seq"][0]

                if instr == "N" and seedSeq[-1] == "N":
                   pass

                else:
                    testSeq = seedSeq + instr
                    value = ord(i16b64.interpret(testSeq + "U"))

                    if constants[value]["len"] > len(testSeq):
                        constants[value] = {"const": value, "len": len(testSeq), "seq": [testSeq]}

                    elif constants[value]["len"] == len(testSeq) and testSeq not in constants[value]["seq"]:
                        constants[value]["seq"].append(testSeq)

        lenSortedConstants = sorted(constants, key=lenSortFunc)
        knownConstants = [c for c in lenSortedConstants if c["len"] < float('inf')]

        for x in knownConstants:
            for y in knownConstants[knownConstants.index(x):]:
                for instr in "ALORXa":
                    seedX = x["seq"][0]
                    seedY = y["seq"][0]

                    testSeq = seedX + seedY + instr
                    value = ord(i16b64.interpret(testSeq + "U"))

                    if constants[value]["len"] > len(testSeq):
                        constants[value] = {"const": value, "len": len(testSeq), "seq": [testSeq]}

                    elif constants[value]["len"] == len(testSeq) and testSeq not in constants[value]["seq"]:
                        constants[value]["seq"].append(testSeq)


    lenSortedConstants = sorted(constants, key=lenSortFunc)
    knownConstants = [c for c in lenSortedConstants if c["len"] < float('inf')]

    with open("16b64constants.txt", "w") as file:
        for x in range(len(constants)):
            file.write(f"{x:#06x} - {', '.join(constants[x]['seq'])}\n")

    print(f"{(len(knownConstants) / len(constants)) * 100:.4f}%")

#figure out the size of the stack after the calculations
def stacksize(code):
    size = 0
    for char in code:
        #0123456789ADILNORSXalr
        if char in "0123456789I":
            size -= 0
        elif char in "DNdlr":
            size -= 1
        elif char in "ALORSXa":
            size -= 2
        elif char in "CFUbcefgi":
            return f"Unused char in this number finder: {char}"
        else:
            return f"Unknown Char {char}"

        if size < 0:
            return "too small for stack"

        # 0123456789ADILNORSXadlr
        if char in "d":
            size += 0
        elif char in "0123456789AILNORXalr":
            size += 1
        elif char in "DS":
            size += 2

        if size == 0:
            return "nothing on stack"

    return size


    print(f"Constant: {c:#06x}, Code: {code}")

    return newConstants

def main():

    constants = []

    for x in range(2 ** 16):
        constants.append("")

    for x in range(len(literals)):
        constants[literals[x]] = [str(x)]

    # where the searching happens

    codeList = []

    for char in "0123456789":
        codeList += char

    for x in range(5):
        for code in range(len(codeList)):
            for char in "0123456789ADLNORSXadlr":
                codeList.append(codeList[code] + char)

    #print(codeList)

    for code in codeList:

        if stacksize(code) == 1:
            #print(code)

            c = ord(b16b64.run("", code + "U"))

            if constants[c] == "":
                constants[c] = [code]
            elif len(code) < len(constants[c][0]):
                constants[c] = [code]
            elif len(code) == len(constants[c][0]) and code not in constants[c]:
                constants[c].append(code)


    #print(codeList)

    file = open("16b64constants.txt", "w")

    for x in range(len(constants)):
        file.write(f"{x:#06x} - {', '.join(constants[x])}\n")


    file.close()

#l = []

#    for x in "penisballs":
#        l.append(f"{ord(x):02x}")
#
#    if len(l) % 2 == 1:
#        l.append("00")
#
#    for x in range(len(l) // 2):
#        print(l[x*2] + l[(x*2)+1])


if __name__ == "__main__":
    main2()