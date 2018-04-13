import sys
from os.path import basename, splitext
from parser import Parser
import code
from symbol_table import SymbolTable


def root_fname(f):
    return splitext(basename(f.name))[0]


if __name__ == "__main__":
    asm_fname = sys.argv[1]

    # Initialization

    # First Pass: symbol table, hack line count

    # Second Pass: parsing, writing to .hack file
