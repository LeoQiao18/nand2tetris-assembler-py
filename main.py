import sys
from os.path import basename, splitext
from asm_parser import Parser
import code
from symbol_table import SymbolTable


def root_fname(f):
    return splitext(basename(f.name))[0]


def is_postive_int(s):
    try:
        i = int(s)
        return i > 0
    except ValueError:
        return False


if __name__ == "__main__":
    asm_fname = sys.argv[1]

    # Initialization
    psr = Parser(asm_fname)
    sym_table = SymbolTable()

    # First Pass: symbol table, hack line count
    line_count = 0
    while psr.has_more_commands():
        psr.advance()
        # L_COMMAND
        if psr.command_type() == "L_COMMAND":
            psr.parse_command()
            if not sym_table.contains(psr.symbol):
                sym_table.add_entry(psr.symbol, line_count + 1)

        # A_COMMAND and C_COMMAND
        else:
            line_count += 1

    # Second Pass: parsing, writing to .hack file
    psr.restart()

    # create .hack file to write
    with open(root_fname(psr.f) + ".hack", "w") as hack:
        while psr.has_more_commands():

            # preparations
            psr.advance()
            psr.parse_command()
            cmd_type = psr.command_type()

            # A_COMMAND
            if cmd_type == "A_COMMAND":
                hack_line = "0"
                # constant
                if is_postive_int(psr.symbol):
                    hack_line += bin(int(psr.symbol))[2:].zfill(15)
                # previously defined symbol
                elif sym_table.contains(psr.symbol):
                    hack_line += bin(sym_table.get_address(psr.symbol)
                                     )[2:].zfill(15)
                # new symbol
                else:
                    sym_table.add_entry(psr.symbol)
                    hack_line += bin(sym_table.get_address(psr.symbol)
                                     )[2:].zfill(15)
                # write to .hack file
                hack.write(hack_line + "\n")

            # C_COMMAND
            elif cmd_type == "C_COMMAND":
                # assemble C_COMMAND
                hack_line = "111" + \
                    code.dest(psr.dest) + code.comp(psr.comp) + \
                    code.jump(psr.jump)
                # write to .hack file
                hack.write(hack_line + "\n")

        # close the .asm file
        psr.end()

    # complete
    print("Assembly process complete!!!")
·
