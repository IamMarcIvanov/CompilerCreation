from first_follow_getters import *
import copy
from Neuspeak_Lexer import *


class ParseTree:
    def __init__(self):
        self.data = ''
        self.children = []
        self.parent = None
        self.index = 0

class Parser:
    #Handling all the files involved in computing
    def __init__(self, 
                 path_to_code,
                 path_to_lexer_output,
                 read_cfg,
                 write_productions,
                 write_first,
                 write_follow,
                 write_table,
                 write_actionTable_loc,
                 read_first_follow_table):
        """
        Args:
            path_to_code ([str]): [The Path to the file that contains Neuspeak Code]
            path_to_lexer_output ([str]): [The path to the file in which the lexer will write the token stream]
            read_cfg ([str]): [The path to the file from with the CFG for Neuspeak is kept]
            write_productions ([str]): [The path to the file where the list of terminals, non-terminals and productions are written]
            write_first ([str]): [The path to the file where the first set is written]
            write_follow ([str]): [The path to the file where the follow set is written]
            write_table ([str]): [The path to the file where the Parse Table for the Neuspeak CFG is written]
            write_actionTable_loc ([str]): [The path to the file where the action table for the current file is written]
            read_first_follow_table ([str]): [The path to the file where the first follow table exists]
        """
        self.write_actionTable_loc = write_actionTable_loc
        
        self.root = ParseTree() 
        self.lex = Lexer(path_to_code, path_to_lexer_output) # lex object has a member self.lex.tokenStream is list of tokens
        self.tokenStream = self.lex.tokenStream
        
        #self.tokenStream = ts.split()
        self.fftObj = FirstFollowTable(read_first_follow_table,
                                       read_cfg,
                                       write_table,
                                       write_first,
                                       write_follow,
                                       write_productions)
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
        """
        Summary:
            When a non-terminal is at the top of the stack, it is expanded into its productions. 
            This function reflects that in the tree. A new node is created for every terminal and non-terminal.

        Args:
            R ([list of strings]): [When a non-terminal is at the top of the stack, it is expanded into its 
                                    productions. R contains the RHS of the rule]
        """
        for ind, s in enumerate(R):
            node = ParseTree()
            node.parent = self.currNode
            node.index = ind
            node.data = s.strip()
            self.currNode.children.append(node)
        self.currNode = self.currNode.children[-1]               
        
    def setNode(self):
        """
        Summary:
            This moves the current Node to the right location in the parse tree. This is used to 
            ensure that the current node and the top of the stack are always in sync.
        """
        while True:
            if self.currNode.data == self.root.data:
                return
            if self.currNode.index == 0:
                self.currNode = self.currNode.parent
            else:
                break
        
        self.currNode = self.currNode.parent.children[self.currNode.index - 1]
                    
    def getTree(self):
        curr = 0
        count = 0
        line = 1
        #loops till either stack or token Stream is empty
        while len(self.stack) > 0 and count < 1000 and curr < len(self.tokenStream): 
            # means element at the top of the stack is non-terminal
            if self.stack[-1].strip().startswith('{'): 
                row = self.NT.index(self.stack[-1].strip()) + 1
                col = self.table[0].index(self.tokenStream[curr])
                #Value in the parse table corresponding to given stack and tokenstream is a prodution
                if '=' in self.table[row][col]:
                    self.stack.pop()
                    ruleRHS = self.table[row][col].split('=')[1].strip().split(' ')
                    self.stack.extend(ruleRHS[::-1]) # get RHS of rule
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], self.table[row][col], str(line)])
                    self.addToTree(ruleRHS[::-1])
                #Error Handling
                else:
                    #Value in the parse table corresponding to given stack and tokenstream is Sync
                    if self.table[row][col].strip() == 'sync':
                        error = '   EXPECTED ' + self.stack[-1] + ' GOT ' + self.tokenStream[curr]
                        self.stack.pop()
                        self.setNode()
                        self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6, str(line) + error])
                    #Value in the parse table corresponding to given stack and tokenstream is Skip
                    if self.table[row][col].strip() == 'skip':
                        if self.tokenStream[curr] == '$':
                            error = '   EXPECTED ' + \
                                self.stack[-1] + ' GOT ' + \
                                    self.tokenStream[curr]
                            self.stack.pop()
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6, str(line) + error ])
                        else:
                            error = '   EXPECTED ' + \
                                self.stack[-1] + ' GOT ' + \
                                    self.tokenStream[curr]
                            curr += 1
                            self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'skip' + '*' * 6, str(line) + error])
            # means top of stack is terminal or epsilon                
            elif self.stack[-1].strip().startswith('['): 
                # Used to record line number of the code
                if self.stack[-1] == '[NL]':
                    line += 1
                # means the terminal at top of stack matches with current token on token Stream    
                if self.stack[-1].strip() == self.tokenStream[curr]: 
                    curr += 1
                    termin = self.stack.pop()
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'match ' + str(termin), str(line)])
                    self.setNode()
                # top of the stack is epsilon so would be popped    
                elif self.stack[-1].strip() == '[~]':
                    termin = self.stack.pop()
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'epsilon pop ' + str(termin), str(line)])
                    self.setNode()
                # ERROR Handling
                # terminal at top of stack and current token in token stream does not match    
                else:
                    row = self.NT.index(self.currNode.parent.data) + 1
                    col = self.table[0].index(self.tokenStream[curr])
                    # Value in parse table for NT corresponding to stack top terminal and tokenstream current terminal is Sync 
                    if self.table[row][col].strip() == 'sync':
                        error = '   EXPECTED ' + \
                            self.stack[-1] + ' GOT ' + self.tokenStream[curr]
                        self.stack.pop()
                        self.setNode()
                        self.actionTable.append(
                            [self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6, str(line) + error])
                    # Value in parse table for NT corresponding to stack top terminal and tokenstream current terminal is Skip
                    elif self.table[row][col].strip() == 'skip':
                        error = '   EXPECTED ' + \
                                self.stack[-1] + ' GOT ' + self.tokenStream[curr]
                        curr += 1 if self.tokenStream[curr] != '$' else 0
                        if self.tokenStream[curr] == '$':
                            self.tokenStream[curr]
                            self.stack.pop()
                            self.actionTable.append(
                                [self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6, str(line) + error])
                        else:
                            self.tokenStream[curr]
                            self.actionTable.append(
                                [self.tokenStream[curr:], self.stack[:], '*' * 6 + 'skip' + '*' * 6, str(line) + error])
                    else:
                        error = '   EXPECTED ' + self.stack[-1] + ' GOT ' + self.tokenStream[curr]
                        self.stack.pop()
                        self.actionTable.append(
                            [self.tokenStream[curr:], self.stack[:], '*' * 6 + 'sync' + '*' * 6, str(line) + error])
            else:
                # we reached the end of Stack and Token Stream hence the parsing is complete
                if self.stack[-1].strip() == '$' and self.tokenStream[curr] == '$':
                    self.stack.pop()
                    curr += 1
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], 'matched. PARSING COMPLETE', str(line)])
                else:
                    curr += 1
                    self.actionTable.append([self.tokenStream[curr:], self.stack[:], '*' * 6 + 'skip' + '*' * 6, str(line)])
            count += 1
    
    # writing action table in a file
    def writeActionTable(self):
        """
        Summary:
            Action table is written to a file. Max column width is simultaneously determined to 
            set the widths of the columns so that the columns do not become too difficult to read.
        """
        row_n = len(self.actionTable)
        for c in range(4):
            max_len = 0
            for r in range(row_n):
                try:
                    if len(' '.join(self.actionTable[r][c])) > max_len:
                        max_len = len(' '.join(self.actionTable[r][c]))
                except:
                    print(r, c)
            self.max_actionTable_widths.append(max_len)

        with open(self.write_actionTable_loc, 'w') as f:
            s1 = '{:<' + str(self.max_actionTable_widths[0] + 3)  + '}'
            s2 = '{:<' + str(self.max_actionTable_widths[1] + 3)  + '}'
            s3 = '{:<' + str(self.max_actionTable_widths[2] + 3)  + '}'
            s4 = '{:<' + str(self.max_actionTable_widths[3] + 3)  + '}'
            s = s1 + s2 + s3 + s4
            f.write(s.format('TOKEN STREAM', 'STACK', 'ACTION', 'LINE NUMBER') + '\n')
            for row in self.actionTable:
                f.write(s.format(' '.join(row[0]), ' '.join(row[1]), str(row[2]), str(row[3])) + '\n')
   
                    
