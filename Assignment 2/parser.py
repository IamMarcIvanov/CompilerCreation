from Neuspeak_Lexer import *
from FFT import *


read_cfg = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\CFG.txt'
write_productions = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\prod.txt'
write_first = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\first.txt'
write_follow = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\follow.txt'
write_table = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\table.txt'
stack_loc =  r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\stack.txt'

class ParseTree:
    def __init__(self):
        self.n_children = 0
        self.data = ''
        self.children = []
        
        
class Parser:
    def __init__(self):
        self.root = ParseTree()
        self.lex = Lexer() # lex object has a member self.lex.tokens is list of tokens
        self.tokenStream = self.lex.tokenStream
        
        self.fftObj = FFT()
        self.start_nt = self.fftObj.cfg.start_nt
        self.stack = ['$', self.start_nt]
        self.table = self.fftObj.table
        self.NT = sorted(self.fftObj.cfg.NT)
        with open(stack_loc, 'w') as f:
            f.write(self.start_nt + '\n')
            # for token in self.tokenStream:
                # f.write(str(token) + '\n')
        self.T = sorted(self.fftObj.cfg.T)
        
        self.getTree()
        
    def getTree(self):
        curr = 0
        count = 0
        while len(self.stack) > 0 and count < 100:
            if self.stack[-1].islower(): # means non-terminal
                with open(stack_loc, 'a') as f:
                    f.write('here1\n')
                row = self.NT.index(self.stack.pop()) + 1
                col = self.T.index(self.tokenStream[curr]) + 1
                self.stack + self.table[row][col].split('=')[1].strip().split(' ')[::-1]
            elif self.stack[-1].isupper(): # means terminal
                if self.stack[-1] == self.tokenStream[curr]:
                    with open(stack_loc, 'a') as f:
                        f.write('here1\n')
                    curr += 1
                    self.stack.pop()
                else:
                    print('Fallen heros')
            else:
                if self.stack[-1] == '$' and self.tokenStream[curr] == '$':
                    self.stack.pop()
                    curr += 1
            with open(stack_loc, 'a') as f:
                f.write(str(self.stack) + '\n')
            count += 1

obj = Parser()   
                    