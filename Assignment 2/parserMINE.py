from first_follow_getters import *
import copy
from Neuspeak_Lexer import *

read_cfg = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\CFG.txt'
write_productions = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\prod.txt'
write_first = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\first.txt'
write_follow = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\follow.txt'
write_table = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\table.txt'
stack_loc =  r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\stack.txt'
write_actionTable_loc = r'D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 2\actionTable.txt'


class ParseTree:
    def __init__(self):
        self.data = ''
        self.children = []
        self.parent = None
        self.index = 0

class Parser:
    def __init__(self):
        self.root = ParseTree()
        self.lex = Lexer() # lex object has a member self.lex.tokenStream is list of tokens
        self.tokenStream = self.lex.tokenStream
        
        #self.tokenStream = ts.split()
        self.fftObj = FirstFollowTable()
        self.start_nt = self.fftObj.start_nt
        self.stack = ['$', self.start_nt]
        self.table = self.fftObj.table
        self.NT = sorted(self.fftObj.NT)
        self.T = sorted(self.fftObj.T)
        self.actionTable = []
        self.max_actionTable_widths = []
        
        self.root.data = self.start_nt
        self.currNode = self.root
        
        self.getTree()
        self.writeActionTable()
    
    def addToTree(self, R):
        for ind, s in enumerate(R):
            node = ParseTree()
            node.parent = self.currNode
            node.index = ind
            node.data = s.strip()
            self.currNode.children.append(node)
        self.currNode = self.currNode.children[-1]               
        
    def setNode(self):
        while True:
            if self.currNode.data == self.root.data:
                return
            if self.currNode.index == 0:
                self.currNode = self.currNode.parent
            else:
                #print(self.currNode.data)
                break
        
        self.currNode = self.currNode.parent.children[self.currNode.index - 1]
                    
    def getTree(self):
        curr = 0
        count = 0
        while len(self.stack) > 0 and count < 1000 and curr < len(self.tokenStream):
            if self.stack[-1].startswith('{'): # means non-terminal
                row = self.NT.index(self.stack[-1]) + 1
                col = self.table[0].index(self.tokenStream[curr])
                if '=' in self.table[row][col]:
                    self.stack.pop()
                    ruleRHS = self.table[row][col].split('=')[1].strip().split(' ')
                    self.stack.extend(ruleRHS[::-1]) # get RHS of rule
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], self.table[row][col]])
                    self.addToTree(ruleRHS[::-1])
                else:
                    if self.table[row][col].strip() == 'sync':
                        self.stack.pop()
                        self.setNode()
                        self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6])
                    if self.table[row][col].strip() == 'skip':
                        curr += 1 if self.tokenStream[curr] != '$' else 0
                        if self.tokenStream[curr] == '$':
                            self.stack.pop()
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6])
                        else:
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'skip' + '*' * 6])
            elif self.stack[-1].startswith('['): # means top of stack is terminal or epsilon
                if self.stack[-1] == self.tokenStream[curr]: # match found
                    curr += 1
                    termin = self.stack.pop()
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'match ' + str(termin)])
                    self.setNode()
                elif self.stack[-1] == '[~]':
                    termin = self.stack.pop()
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'epsilon pop ' + str(termin)])
                    self.setNode()
                else:
                    row = self.NT.index(self.currNode.parent.data) + 1
                    col = self.table[0].index(self.tokenStream[curr])
                    if self.table[row][col].strip() == 'sync':
                        self.stack.pop()
                        self.setNode()
                        self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6])
                    elif self.table[row][col].strip() == 'skip':
                        curr += 1 if self.tokenStream[curr] != '$' else 0
                        if self.tokenStream[curr] == '$':
                            self.stack.pop()
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6])
                        else:
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'skip' + '*' * 6])
                    else:
                        self.stack.pop()
                        self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6])
            else:
                if self.stack[-1] == '$' and self.tokenStream[curr] == '$':
                    self.stack.pop()
                    curr += 1
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'matched. PARSING COMPLETE'])
                else:
                    curr += 1
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'skip' + '*' * 6])
            count += 1
    
    def writeActionTable(self):
        row_n = len(self.actionTable)
        for c in range(3):
            max_len = 0
            for r in range(row_n):
                if len(' '.join(self.actionTable[r][c])) > max_len:
                    max_len = len(' '.join(self.actionTable[r][c]))
            self.max_actionTable_widths.append(max_len)

        with open(write_actionTable_loc, 'w') as f:
            s1 = '{:<' + str(self.max_actionTable_widths[0] + 3)  + '}'
            s2 = '{:<' + str(self.max_actionTable_widths[1] + 3)  + '}'
            s3 = '{:<' + str(self.max_actionTable_widths[2] + 3)  + '}'
            s = s1 + s2 + s3
            f.write(s.format('TOKEN STREAM', 'STACK', 'ACTION') + '\n')
            for row in self.actionTable:
                f.write(s.format(' '.join(row[0]), ' '.join(row[1]), str(row[2])) + '\n')

obj = Parser()   
                    