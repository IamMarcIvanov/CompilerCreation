from CFGreader import *
import copy

read_cfg = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\CFG.txt'
write_productions = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\prod.txt'
write_first = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\first.txt'
write_follow = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\follow.txt'
write_table = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\table.txt'

class FFT:
    def __init__(self, writeFiles=True,
                       read_cfg_loc=read_cfg,
                       rules=write_productions, 
                       first=write_first, 
                       follow=write_follow, 
                       table=write_table):
        self.cfg = CFG(True, read_cfg, write_productions)
        self.FIRST = {}
        self.FOLLOW = {}
        self.table = [[]]
        self.initialise()
        
        self.setFirstSet()
        self.setFollowSet()
        self.setParseTable()
        
        
        if writeFiles:
            self.writeFirst(first)
            self.writeFollow(follow)
            self.writeTable(table)
        
    def initialise(self):
        for nt in self.cfg.NT:
            self.FIRST[nt] = set()
            self.FOLLOW[nt] = set()
        self.FOLLOW[self.cfg.start_nt].add('$')
        self.FIRST['~'] = set('~')
        
        self.table[0].append('')
        for t in sorted(self.cfg.T):
            self.table[0].append(t)
        self.table[0].append('$')
        
        for nt in sorted(self.cfg.NT):
            self.table.append([nt] + [''] * (len(self.cfg.T) + 1))
    
    def compare(self, d1, d2):
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
    
    def setFirstSet(self):
        while(True):
            fi  = copy.deepcopy(self.FIRST)
            for nt in self.cfg.productions.keys():
                for rhs in self.cfg.productions[nt]:
                    if rhs[0][0].isupper(): # begins with terminal
                        self.FIRST[nt].add(rhs[0])
                    else: # begins with non-terminal
                        if rhs[0] in self.FIRST.keys(): # if first of that non-terminal exists
                            if '~' not in self.FIRST[rhs[0]]: # non-terminal in RHS does NOT have epsilon in first
                                self.FIRST[nt].update(self.FIRST[rhs[0]])
                            else:
                                
                        else:
                            continue
            if self.compare(fi, self.FIRST):
                break
    
    def setFollowSet(self):
        while(True):
            fo = copy.deepcopy(self.FOLLOW)
            for Ai in self.cfg.NT:
                for Aj in self.cfg.NT:
                    for rhs in self.cfg.productions[Aj]:
                        if Ai in rhs:
                            if rhs[-1] == Ai:
                                self.FOLLOW[Ai].update(self.FOLLOW[Aj])
                            else:
                                ind = rhs.index(Ai)
                                if rhs[ind + 1][0].islower():
                                    (self.FOLLOW[Ai]).update(self.FIRST[rhs[ind+1]])
                                else:
                                    self.FOLLOW[Ai].update([rhs[ind + 1]])
            if self.compare(fo, self.FOLLOW):
                break

    
    def setParseTable(self):
        for row, nt in enumerate(sorted(self.cfg.NT)):
            for rhs in self.cfg.productions[nt]:
                if rhs[0][0].islower():
                    for t in self.FIRST[rhs[0]]:
                        row_n = row + 1
                        col_n = sorted(self.cfg.T).index(t) + 1
                        if not self.table[row_n][col_n]:
                            self.table[row_n][col_n] = nt + ' = ' + ' '.join(rhs)
                else:
                    row_n = row + 1
                    col_n = sorted(self.cfg.T).index(rhs[0]) + 1
                    if not self.table[row_n][col_n]:
                        self.table[row_n][col_n] = nt + ' = ' + ' '.join(rhs)
                    
        for row_n, row in enumerate(self.table):
            for col_n, col in enumerate(row):
                if row_n == 0 or col_n == 0:
                    continue
                else:
                    if self.table[row_n][col_n] == '':
                        if self.table[0][col_n] in self.FOLLOW[self.table[row_n][0]]:
                            self.table[row_n][col_n] = 'sync'
                        else:
                            self.table[row_n][col_n] = 'skip'
    
    def writeFirst(self, write_first_loc):
        with open(write_first_loc, 'w') as f:
            f.write(str(len(self.FIRST.keys())) + '\n')
            for key in sorted(self.FIRST.keys()):
                f.write('{:<30} = {}\n'.format(key, sorted(self.FIRST[key])))
    
    def writeFollow(self, write_follow_loc):
        with open(write_follow_loc, 'w') as f:
            f.write(str(len(self.FOLLOW.keys())) + '\n')
            for key in sorted(self.FOLLOW.keys()):
                f.write('{:<30} = {}\n'.format(key, sorted(self.FOLLOW[key])))

    def writeTable(self, write_table_loc):
        with open(write_table_loc, 'w') as f:
            for row_n, row in enumerate(self.table):
                for col_n, cell in enumerate(row):
                        f.write('{:^140} | '.format(cell))
                if row_n == 0:
                        f.write('\n' + '-' * (143 * (len(row))) + '\n')
                else:
                        f.write('\n')

obj = FFT(True)
