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
    psr = Parser(asm_fname)
    sym_table = SymbolTable()

    # First Pass: symbol table, hack line count
    line_count = 0
    while psr.has_more_commands():
        psr.advance()
        if psr.command_type() == "L_COMMAND":
            psr.parse_command()
            if not sym_table.contains(psr.symbol):
                sym_table.add_entry(psr.symbol)

    # Second Pass: parsing, writing to .hack file
