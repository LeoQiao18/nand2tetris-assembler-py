import sys
from os.path import basename, splitext
from parser import Parser


def root_fname(f):
    return splitext(basename(f.name))[0]


if __name__ == "__main__":
    asm_name = sys.argv[1]

    psr = Parser(asm_name)

    # open and read .asm file
    with open(asm_name) as asm:
        bin_fname = root_fname(asm) + ".hack"

        # create and write to .hack file
        with open(bin_fname, "w") as hack:
            current_line = asm.readline()

            # keep compiling until EOF in .asm file
            while current_line != "":
                binary = compile_cmd(current_line) + "\n"
                hack.write(binary)

    print("Assembly process completed")
