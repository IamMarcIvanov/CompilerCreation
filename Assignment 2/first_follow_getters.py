FFTloc = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\first_follow_table2.txt'
prodLoc = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\CFG_scratch2.txt'
write_table_loc = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\table.txt'
write_first_loc = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\first.txt'
write_follow_loc = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\follow.txt'
write_prod_loc = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\prod.txt'

class FirstFollowTable:
    def __init__(self):
        self.table = [[]]
        self.T = set()
        self.NT = set()
        self.FIRST = dict()
        self.FOLLOW = dict()
        self.productions = {}
        self.col_max_widths = []
        self.start_nt = None
        
        self.getTNT()
        self.writeFirst()
        self.writeFollow()
        self.getProductions()
        self.writeProductions()
        self.setTable()
        self.setColWidths()
        self.writeTable()
    
    def getTNT(self):
        with open(FFTloc, 'r') as f:
            n = int(f.readline())
            for _ in range(n):
                line = f.readline().split('=')
                nt = line[0].strip()
                self.NT.add(nt)
                fi = line[1].split(',')
                for ff in fi:
                    if ff.strip() != '[~]':
                        self.T.add(ff.strip())
                    self.FIRST[nt] = self.FIRST.get(nt, [])
                    self.FIRST[nt].append(ff.strip())
                fo = line[2].split(',')
                for ff in fo:
                    if ff.strip() != '$':
                        self.T.add(ff.strip())
                    self.FOLLOW[nt] = self.FOLLOW.get(nt, [])
                    self.FOLLOW[nt].append(ff.strip())
        self.FIRST['[~]'] = ['[~]']

    def getProductions(self):
        with open(prodLoc, 'r') as f:
            n = int(f.readline())
            for i in range(n):
                line = f.readline().split('::=')
                nt = line[0].strip()
                if i == 0:
                    self.start_nt = nt
                self.productions[nt] = self.productions.get(nt, [])
                self.productions[nt].append(line[1].strip().split(' '))
                for t in line[1].strip().split(' '):
                    if t.strip().startswith('[') and '~' not in t:
                        self.T.add(t.strip())
                
    def setTable(self):
        self.table[0].append('')
        for t in sorted(self.T):
            self.table[0].append(t)
        self.table[0].append('$')
        
        for nt in sorted(self.NT):
            self.table.append([nt] + [''] * (len(self.T) + 1))
            
        for row, nt in enumerate(sorted(self.NT)):
            for rhs in self.productions[nt]:
                if rhs[0][0] == '{':
                    if '[~]' not in self.FIRST[rhs[0]]:
                        for t in self.FIRST[rhs[0]]:
                            row_n = row + 1
                            col_n = self.table[0].index(t)
                            if not self.table[row_n][col_n]:
                                self.table[row_n][col_n] = nt + ' = ' + ' '.join(rhs)
                    # else:
                        # for t in self.FOLLOW[nt]:
                            # row_n = row + 1
                            # col_n = self.table[0].index(t)
                            # if not self.table[row_n][col_n]:
                                # self.table[row_n][col_n] = nt + ' = ' + ' '.join(rhs)
                else:
                    if rhs[0] != '[~]':
                        row_n = row + 1
                        col_n = self.table[0].index(rhs[0])
                        if not self.table[row_n][col_n]:
                            self.table[row_n][col_n] = nt + ' = ' + ' '.join(rhs)
                    else:
                        for t in self.FOLLOW[nt]:
                            row_n = row + 1
                            col_n = self.table[0].index(t)
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
    
    def setColWidths(self):
        n_rows = len(self.table)
        n_cols = len(self.table[0])
        for c in range(n_cols):
            max_len = 0
            for r in range(n_rows):
                if len(self.table[r][c]) > max_len:
                    max_len = len(self.table[r][c])
            self.col_max_widths.append(max_len)
            
        
    def writeProductions(self):
        with open(write_prod_loc, 'w') as f:
            f.write('PRODUCTIONS ' + str(len(self.productions.keys())) + '\n')
            for key in sorted(self.productions.keys()):
                f.write('{:<30} = {}\n'.format(key, self.productions[key]))
            f.write('\n' + 'NON TERMINALS' + ' ' + str(len(self.NT)) +'\n')
            for nt in sorted(self.NT):
                f.write(nt + '\n')
            f.write('\n' + 'TERMINALS' + ' ' + str(len(self.T)) +'\n')
            for t in sorted(self.T):
                f.write(t + '\n')
     
    def writeTable(self):
        with open(write_table_loc, 'w') as f:
            for row_n, row in enumerate(self.table):
                for col_n, cell in enumerate(row):
                    s = '{:^' + str(self.col_max_widths[col_n]) + '} | '
                    f.write(s.format(cell))
                if row_n == 0:
                    f.write('\n' + '-' * (sum(self.col_max_widths) + 3 * (len(row))) + '\n')
                else:
                    f.write('\n')
                        
    def writeFirst(self):
        with open(write_first_loc, 'w') as f:
            f.write(str(len(self.FIRST.keys())) + '\n')
            for key in sorted(self.FIRST.keys()):
                f.write('{:<30} = {}\n'.format(key, sorted(self.FIRST[key])))
    
    def writeFollow(self):
        with open(write_follow_loc, 'w') as f:
            f.write(str(len(self.FOLLOW.keys())) + '\n')
            for key in sorted(self.FOLLOW.keys()):
                f.write('{:<30} = {}\n'.format(key, sorted(self.FOLLOW[key])))

#obj = FirstFollowTable()