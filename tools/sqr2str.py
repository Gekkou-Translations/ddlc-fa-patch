#!/usr/bin/env python3
import argparse
import sys
import math
from PIL import Image

program_name = "sqr2str"
program_version = "1.0"

def decodeSqr(inFile):
    with Image.open(inFile) as sqr:
        px = sqr.load()

    sqrSize = sqr.size
    sqrBin = ''
    sqrStr = ''
    spc = 0

    for i in range(sqrSize[0]):
        for j in range(sqrSize[1]):
            if spc == 8:
                sqrBin += ' '
                spc = 0

            spc += 1

            if px[j, i] == (0, 0, 0, 255):
                sqrBin += '0'
            else:
                sqrBin += '1'

    for i in sqrBin.split(' '):
        sqrStr += chr(int(i, base=2))

    return sqrStr

def encodeSqr(inFile, outFile):
    with open(inFile, "r") as file:
        inStr = file.read()

    inStr = ''.join(f"{ord(i):08b}" for i in inStr)
    sqrSize = math.ceil(len(inStr)**0.5)

    with Image.new("1", [sqrSize, sqrSize]) as sqr:
        px = sqr.load()

        for i in range(len(inStr)):
            px[i%sqrSize, int(i/sqrSize)] = int(inStr[i])

        sqr.save(outFile)

def main():
    parser = argparse.ArgumentParser(
        description = "Convert a Binary square image to ASCII"
    )
    parser.add_argument(
        "-e",
        "--encode",
        action="store_true",
        dest="encode_sqr",
        default=False,
        help = "Encode an ASCII file to a Binary square image"
    )
    parser.add_argument(
        "input_file",
        help = "Input file"
    )
    parser.add_argument(
        "output_file",
        help = "Output file (Optional for decoding)",
        nargs = "?",
        default = "-"
    )
    args = parser.parse_args()

    if args.encode_sqr:
        output = encodeSqr(args.input_file, args.output_file)
    else:
        output = decodeSqr(args.input_file)
        if args.output_file == "-":
            print(output)
        else:
            with open(args.output_file, "w") as file:
                file.write(output)

    return 0

if __name__ == "__main__":
    sys.exit(main())
