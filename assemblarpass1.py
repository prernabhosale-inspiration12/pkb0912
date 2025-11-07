import re
import os

# ---------- Data structures ----------
class TableEntry:
    def __init__(self, name, address=0):
        self.name = name
        self.address = address

class PoolTable:
    def __init__(self, first, total_literals):
        self.first = first
        self.total_literals = total_literals


# ---------- Utility search functions ----------
def search(token, lst):
    for i, item in enumerate(lst):
        if isinstance(item, TableEntry):
            if item.name.lower() == token.lower():
                return i
        elif isinstance(item, str):
            if item.lower() == token.lower():
                return i
    return -1


# ---------- Main Assembler Pass 1 ----------
def assembler_pass1(base_path):
    regs = ["AX", "BX", "CX", "DX"]
    impr = ["STOP", "ADD", "SUB", "MULT", "MOVER", "MOVEM", "COMP", "BC", "DIV", "READ", "PRINT"]
    decl = ["DS", "DC"]

    symbol_table = []
    literal_table = []
    pool_table = []
    op_table = []
    already_processed = []

    input_path = os.path.join(base_path, "sample.txt")
    output_path = os.path.join(base_path, "OutputTextTry.txt")

    start = end = False
    loc = 0
    total_symb = total_ltr = optab_cnt = pooltab_cnt = 0

    with open(input_path, "r") as f_in, open(output_path, "w") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            line = line.replace(",", " ")
            print(line)
            words = line.split()
            ltorg = False

            # START
            if "START" in words:
                idx = words.index("START")
                start = True
                f_out.write("(AD,1)\n")
                loc = int(words[idx + 1])
                continue

            # END
            if "END" in words:
                end = True
                f_out.write("(AD,2)\n")
                for ltr in literal_table:
                    if ltr.address == 0:
                        ltr.address = loc
                        f_out.write(f"(DL,2)\t(C,{ltr.name[2]})\n")
                        loc += 1
                pool_table.append(PoolTable(0, len(literal_table)))
                break

            # ORIGIN
            if "ORIGIN" in words:
                f_out.write("(AD,3)\n")
                sym_name = words[1]
                pos = search(sym_name, symbol_table)
                if pos != -1:
                    f_out.write(f"(S,{pos + 1})\n")
                    loc = symbol_table[pos].address
                continue

            # LTORG
            if "LTORG" in words:
                ltorg = True
                for ltr in literal_table:
                    if ltr.address == 0:
                        ltr.address = loc
                        f_out.write(f"(DL,2)\t(C,{ltr.name[2]})\n")
                        loc += 1
                pool_table.append(PoolTable(0, len(literal_table)))
                continue

            # EQU
            if "EQU" in words:
                f_out.write("(AD,4)\n")
                lhs = words[0]
                rhs = words[2]
                pos1 = search(lhs, symbol_table)
                pos2 = search(rhs, symbol_table)
                if pos1 != -1 and pos2 != -1:
                    symbol_table[pos1].address = symbol_table[pos2].address
                continue

            # IMPERATIVE STATEMENTS
            if words[0] not in ["START", "END", "ORIGIN", "EQU", "LTORG"]:
                f_out.write(f"{loc}\t")

                for word in words:
                    pos = search(word, impr)
                    reg_idx = search(word, regs)

                    if pos != -1:
                        f_out.write(f"(IS,{pos})\t")
                        op_table.append(TableEntry(word, pos))
                    elif reg_idx != -1:
                        f_out.write(f"({reg_idx + 1})\t")
                    elif word in decl:
                        idx = decl.index(word)
                        f_out.write(f"(DL,{idx + 1})\t")
                    elif re.match(r"='[0-9]+'", word):
                        literal_table.append(TableEntry(word, 0))
                        total_ltr += 1
                        f_out.write(f"(L,{total_ltr})\t")
                    elif re.match(r"^[A-Za-z]+$", word):
                        # Label or symbol
                        pos = search(word, symbol_table)
                        if pos == -1:
                            symbol_table.append(TableEntry(word, loc))
                            total_symb += 1
                        f_out.write(f"(S,{total_symb})\t")

                f_out.write("\n")
                loc += 1

    # Write symbol, literal, pool, and opcode tables
    with open(os.path.join(base_path, "symTab.txt"), "w") as sw:
        sw.write("SYMBOL\tADDRESS\n")
        for s in symbol_table:
            sw.write(f"{s.name}\t\t{s.address}\n")

    with open(os.path.join(base_path, "litTab.txt"), "w") as lw:
        lw.write("INDEX\tLITERAL\tADDRESS\n")
        for i, l in enumerate(literal_table):
            lw.write(f"{i+1}\t{l.name}\t{l.address}\n")

    with open(os.path.join(base_path, "poolTab.txt"), "w") as pw:
        pw.write("POOL\tTOTAL LITERALS\n")
        for p in pool_table:
            pw.write(f"{p.first}\t\t{p.total_literals}\n")

    with open(os.path.join(base_path, "opTab.txt"), "w") as ow:
        ow.write("MNEMONIC\tOPCODE\n")
        for o in op_table:
            ow.write(f"{o.name}\t\t{o.address}\n")

    print("\n✅ Assembler Pass 1 executed successfully!")
    print(f"Output files generated in: {base_path}")


# ---------- Run ----------
if __name__ == "__main__":
    base_path = r"C:\Users\HP\OneDrive\Desktop\Spos-py"
    assembler_pass1(base_path)
