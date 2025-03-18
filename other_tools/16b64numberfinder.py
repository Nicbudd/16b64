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
            file.write(f"0x{x:04x} - {', '.join(constants[x]['seq'])}\n")


    print(f"{(len(knownConstants) / len(constants)) * 100:.4f}%")



if __name__ == "__main__":
    main2()
