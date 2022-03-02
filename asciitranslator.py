constants = [""] * 2**16

with open("16b64constants.txt") as fp:
    for line in fp:
        cList = line[9:].strip().split(", ")
        constants[int(line[2:6], 16)] = cList[0]

print(constants[:1000])
