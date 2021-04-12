from CFGreader import *
import copy
import itertools

read_cfg = r'E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\Assignment 2\CFG2.txt'
write_productions = r'E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\Assignment 2\prod.txt'
r = CFG()
r.reader(read_cfg)
r.writeCFG(write_productions)

def compare(d1, d2):
    keys1 = sorted(d1.keys())
    keys2 = sorted(d2.keys())
    vals1 = list(d1.values())
    vals2 = list(d2.values())
    for key1, key2 in zip(keys1, keys2):
        if not key1 == key2:
            return False
    for val1, val2 in zip(vals1, vals2):
        if not sorted(val1) == sorted(val2):
            return False
    return True

FIRST = {}
FOLLOW = {}

with open(read_cfg, 'r') as f:
    start_nt = f.readline()
    line2 = f.readline()
    start_nt = '~' + line2[1:line2.index('}')]

for nt in r.NT:
    FIRST[nt] = set()
    FOLLOW[nt] = set()
FOLLOW[start_nt].add('$')

#for t in r.T:
    #FIRST[t] = set([t])
    # FOLLOW[t] = set()

# FIRST
while(True):
    fi  = copy.deepcopy(FIRST)
    for nt in r.productions.keys():
        for rhs in r.productions[nt]:
            if rhs[0][0] != '~':
                FIRST[nt].add(rhs[0])
            else:
                if FIRST[rhs[0]]:
                    FIRST[nt].update(FIRST[rhs[0]])
                else:
                    continue
    if compare(fi, FIRST):
        break


# FOLLOW
while(True):
    fo = copy.deepcopy(FOLLOW)
    for Ai in r.NT:
        for Aj in r.NT:
            for rhs in r.productions[Aj]:
                if Ai in rhs:
                    if rhs[-1] == Ai:
                        FOLLOW[Ai].update(FOLLOW[Aj])
                    else:
                        ind = rhs.index(Ai)
                        if rhs[ind + 1][0] == '~':
                            FOLLOW[Ai].update(FIRST[rhs[ind+1]])
                        else:
                            FOLLOW[Ai].update([rhs[ind + 1]])
    if compare(fo, FOLLOW):
        break

# PRSE TABLE
table = [[]]
table[0].append('')
for t in sorted(r.T):
    table[0].append(t)
table[0].append('$')

for nt in sorted(r.NT):
    table.append([nt[1:].upper()] + [''] * (len(r.T) + 1))

for row, nt in enumerate(sorted(r.NT)):
    for rhs in r.productions[nt]:
        if rhs[0][0] == '~':
            for t in FIRST[rhs[0]]:
                row_n = row + 1
                col_n = sorted(r.T).index(t) + 1
                if not table[row_n][col_n]:
                    rule = [x.upper() if x.startswith('~') else x.lower() for x in rhs]
                    table[row_n][col_n] = nt.upper() + ' = ' + ' '.join(rule)
        else:
            row_n = row + 1
            col_n = sorted(r.T).index(rhs[0]) + 1
            if not table[row_n][col_n]:
                rule = [x.upper() if x.startswith('~') else x.lower() for x in rhs]
                table[row_n][col_n] = nt.upper() + ' = ' + ' '.join(rule)
            
for row_n, row in enumerate(table):
    for col_n, col in enumerate(row):
        if row_n == 0 or col_n == 0:
            continue
        else:
            if table[row_n][col_n] == '':
                if table[0][col_n] in FOLLOW['~' + table[row_n][0].lower()]:
                    table[row_n][col_n] = 'sync'
                else:
                    table[row_n][col_n] = 'skip'
            
            
write_first = r'E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\Assignment 2\first.txt'
write_follow = r'E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\Assignment 2\follow.txt'
write_table = r'E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\Assignment 2\table.txt'
with open(write_first, 'w') as f:
    f.write(str(len(FIRST.keys())) + '\n')
    for key in sorted(FIRST.keys()):
        f.write('{:<30} = {}\n'.format(key, sorted(FIRST[key])))

with open(write_follow, 'w') as f:
    f.write(str(len(FOLLOW.keys())) + '\n')
    for key in sorted(FOLLOW.keys()):
        f.write('{:<30} = {}\n'.format(key, sorted(FOLLOW[key])))


with open(write_table, 'w') as f:
    for row_n, row in enumerate(table):
        n_cols = len(row)
        for col_n, cell in enumerate(row):
                cell = cell.replace('~', '').replace('`', '||')
                f.write('{:^50} | '.format(cell))
        if row_n == 0:
                f.write('\n' + '-' * (53 * (len(row))) + '\n')
        else:
                f.write('\n')

                