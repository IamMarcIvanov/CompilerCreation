from first_follow_getters import *
import copy

read_cfg = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\CFG.txt'
write_productions = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\prod.txt'
write_first = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\first.txt'
write_follow = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\follow.txt'
write_table = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\table.txt'
stack_loc =  r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\stack.txt'
write_actionTable_loc = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\actionTable.txt'

ts = '[MAIN] [NEWLINE] [TAB] [WHILE] [OPEN_BRACKET] [IDENTIFIER] [REL_OP] [NUMBER] [CLOSE_BRACKET] [NEWLINE] [CURLY_OPEN] [NEWLINE] [TAB] [IDENTIFIER] [ASMT] [NUMBER] [SEMI_COLON] [NEWLINE] [CURLY_CLOSE] [SEMI_COLON] [NEWLINE] $'

class ParseTree:
    def __init__(self):
        self.n_children = 0
        self.data = ''
        self.children = []
        
        
class Parser:
    def __init__(self):
        self.root = ParseTree()
        #self.lex = Lexer() # lex object has a member self.lex.tokenStream is list of tokens
        #self.tokenStream = self.lex.tokenStream
        
        self.tokenStream = ts.split()
        self.fftObj = FirstFollowTable()
        self.start_nt = self.fftObj.start_nt
        self.stack = ['$', self.start_nt]
        self.table = self.fftObj.table
        self.NT = sorted(self.fftObj.NT)
        self.T = sorted(self.fftObj.T)
        self.actionTable = []
        
        self.getTree()
        self.writeActionTable()
        
    def getTree(self):
        curr = 0
        count = 0
        latestNT = None
        while len(self.stack) > 0 and count < 100 and curr < len(self.tokenStream):
            if self.stack[-1].startswith('{'): # means non-terminal
                row = self.NT.index(self.stack.pop()) + 1
                col = self.table[0].index(self.tokenStream[curr])
                latestNT = self.table[row][0]
                if '=' in self.table[row][col]:
                    self.stack.extend(self.table[row][col].split('=')[1].strip().split(' ')[::-1]) # get RHS of rule
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], copy.deepcopy(self.table[row][col])])
                else:
                    if self.table[row][col].strip() == 'sync':
                        while(not self.stack[-1] in ['[SEMI_COLON]', '$']):
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'sync'[:]])
                            self.stack.pop()
                    if self.table[row][col].strip() == 'skip':
                        self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'skip'])
                        curr += 1
            elif self.stack[-1].startswith('['): # means terminal
                if self.stack[-1] == self.tokenStream[curr]:
                    curr += 1
                    termin = self.stack.pop()
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'match terminal ' + str(termin)])
                elif self.stack[-1] == '[~]':
                    termin = self.stack.pop()
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'match terminal ' + str(termin)])
                else:
                    if self.tokenStream[curr] == '$':
                        termin = self.stack.pop()
                        self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'sync ' + str(termin)])
                    else:
                        row = self.NT.index(latestNT) + 1
                        col = self.table[0].index(self.tokenStream[curr])
                        if self.table[row][col].strip() == 'sync':
                            while(not self.stack[-1] in ['[SEMI_COLON]', '$']):
                                self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'sync'])
                                self.stack.pop()
                        elif self.table[row][col].strip() == 'skip':
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'skip'])
                            curr += 1
                        else:
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'ERROR'])
            else:
                if self.stack[-1] == '$' and self.tokenStream[curr] == '$':
                    self.stack.pop()
                    curr += 1
                if curr < len(self.tokenStream):
                    if self.tokenStream[curr] == '$':
                        self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'skip'])
                        curr += 1
            count += 1
    
    def writeActionTable(self):
        with open(write_actionTable_loc, 'w') as f:
            f.write('{:^300}{:^300}{:^300}'.format('TOKEN STREAM', 'STACK', 'ACTION') + '\n')
            for row in self.actionTable:
                f.write('{:^300}{:^300}'.format(str(row[0]), str(row[1]), str(row[2])) + '\n')
            

obj = Parser()   
                    