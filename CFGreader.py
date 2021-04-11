class CFG:
    # ^ is tab
    # # is newline character
    # all that start with ~ is non terminal
    # all that start with . are pseudo terminal
    # ` is ||
    # all between {} is non-term in CFG
    # all between [] are terminal in CFG
    # everything not in {} and [] is terminal in CFG
    def __init__(self):
        self.productions = {} # key = NT. value is list of Nt and T.
        self.NT = set()
        self.T = set()
    
    def reader(self, loc):
        with open(loc, 'r') as f:
            n = int(f.readline().strip()) # nos productions
            for i in range(n):
                prod = f.readline().strip().split('@')
                nt = prod[0][1:-1]
                self.NT.add('~' + nt)
                self.productions[nt] = []
                for RHS in prod[1].split('|'):
                    rhs = []
                    i = 0
                    k = len(RHS)
                    while i < k:
                        if RHS[i] == '{':
                            nt_len = RHS[i + 1:].index('}')
                            nt_in = RHS[i + 1: i + nt_len + 1]
                            rhs.append('~' + nt_in)
                            self.NT.add('~' + nt_in)
                            i += nt_len + 2
                        elif RHS[i] == ' ':
                            i += 1
                        elif RHS[i] == '[':
                            t_len = RHS[i + 1:].index(']')
                            t_in = RHS[i + 1: i + t_len + 1]
                            rhs.append(t_in)
                            self.T.add(t_in)
                            i += t_len + 2
                        else:
                            rhs.append(RHS[i])
                            self.T.add(RHS[i])
                            i += 1
                    self.productions[nt].append(rhs)
    
    def printCFG(self):
        print('productions')
        for key in self.productions.keys():
            print('{:<30} = {}'.format(key, self.productions[key]))
        print()
        print('Non-terminals\n', sorted(self.NT))
        print()
        print('Terminals\n', sorted(self.T))
        print()
    
    def writeCFG(self, loc):
        with open(loc, 'w') as f:
            f.write('PRODUCTIONS\n')
            for key in self.productions.keys():
                f.write('{:<30} = {}\n'.format(key, self.productions[key]))
            f.write('\n' + 'NON TERMINALS' + ' ' + str(len(self.NT)) +'\n')
            for nt in sorted(self.NT):
                f.write(nt + '\n')
            f.write('\n' + 'TERMINALS' + ' ' + str(len(self.T)) +'\n')
            for t in sorted(self.T):
                f.write(t + '\n')

obj = CFG()
location1 = r'E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\Assignment 2\CFG.txt'
location2 = r'E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\Assignment 2\prod.txt'
obj.reader(location1)
#obj.printCFG()
obj.writeCFG(location2)

        
                            
        