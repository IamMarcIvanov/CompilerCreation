from first_follow_getters import *

read_cfg = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\CFG.txt'
write_productions = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\prod.txt'
write_first = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\first.txt'
write_follow = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\follow.txt'
write_table = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\table.txt'
stack_loc =  r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\stack.txt'

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
        
        self.getTree()
        
    def getTree(self):
        curr = 0
        count = 0
        while len(self.stack) > 0 and count < 100:
            if self.stack[-1].startswith('{'): # means non-terminal
                row = self.NT.index(self.stack.pop()) + 1
                col = self.table[0].index(self.tokenStream[curr])
                self.stack.extend(self.table[row][col].split('=')[1].strip().split(' ')[::-1]) # get RHS of rule
            elif self.stack[-1].startswith('['): # means terminal
                if self.stack[-1] == self.tokenStream[curr]:
                    curr += 1
                    self.stack.pop()
                elif self.stack[-1] == '[~]':
                    self.stack.pop()
                else:
                    print('Fallen heros')
            else:
                if self.stack[-1] == '$' and self.tokenStream[curr] == '$':
                    self.stack.pop()
                    curr += 1
            count += 1
            print('stack', self.stack)


obj = Parser()   
                    