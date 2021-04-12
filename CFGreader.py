read_cfg = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\CFG.txt'
write_productions = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\prod.txt'


class CFG:
    # all between {} is non-term in CFG
    # all between [] are terminal in CFG
    def __init__(self, write=True, read_loc=read_cfg, write_loc=write_productions):
        self.productions = {} # key = NT. value is list of Nt and T.
        self.NT = set()
        self.T = set()
        self.start_nt = None
        
        self.readCFG(read_loc)
        if write:
            self.writeCFG(write_loc)
    
    def readCFG(self, loc):
        with open(loc, 'r') as f:
            n = int(f.readline().strip()) # nos productions
            for i in range(n):
                prod = f.readline().strip().split('@')
                nt = prod[0][1:-1]
                if i == 0:
                    self.start_nt = nt
                self.NT.add(nt)
                self.productions[nt] = []
                for RHS in prod[1].split('|'):
                    rhs = []
                    i = 0
                    k = len(RHS)
                    while i < k:
                        if RHS[i] == '{':
                            nt_len = RHS[i + 1:].index('}')
                            nt_in = RHS[i + 1: i + nt_len + 1]
                            rhs.append(nt_in)
                            self.NT.add(nt_in)
                            i += nt_len + 2
                        elif RHS[i] == ' ':
                            i += 1
                        elif RHS[i] == '[':
                            t_len = RHS[i + 1:].index(']')
                            t_in = RHS[i + 1: i + t_len + 1]
                            rhs.append(t_in)
                            self.T.add(t_in)
                            i += t_len + 2
                    self.productions[nt].append(rhs)
    
    def writeCFG(self, loc):
        with open(loc, 'w') as f:
            f.write('PRODUCTIONS ' + str(len(self.productions.keys())) + '\n')
            for key in sorted(self.productions.keys()):
                f.write('{:<30} = {}\n'.format(key, self.productions[key]))
            f.write('\n' + 'NON TERMINALS' + ' ' + str(len(self.NT)) +'\n')
            for nt in sorted(self.NT):
                f.write(nt + '\n')
            f.write('\n' + 'TERMINALS' + ' ' + str(len(self.T)) +'\n')
            for t in sorted(self.T):
                f.write(t + '\n')
