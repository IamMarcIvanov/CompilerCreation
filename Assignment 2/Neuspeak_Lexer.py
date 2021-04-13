import string
import sys


code_path = r"E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\Assignment 1\file4.nspk"
output_path = r"D:\Mimisbrunnr\Github Repositories\CompilerCreation\Assignment 1\output4.txt"

class Lexer:
    def __init__(self):
        self.tokenStream = []
        self.keywords = ['main()', 'return', 'else', 'if', 'output', 'for', 'newline()']
        self.dataType = ['int', 'boolean', 'char', 'float', 'string']
        self.booleans = ['true', 'false']
        
        self.getTokenStream()
        self.tokenStream.append('$')
        a = []
        for item in self.tokenStream:
            a.append('[' + item + ']')
        print(a)

    def getTokenStream(self):
        with open(output_path, "w") as out_file:
            console = sys.stdout
            sys.stdout = out_file
            print("{:*^30}{:*^30}{:*^30}".format("Token", "Lexeme", "Line Number"))
            with open(code_path, 'r') as f:
                line_counter = 0
                for line_nos, line in enumerate(f.readlines()):
                    temporary_line = line[:].strip()
                    if temporary_line == '' or temporary_line[0] == '#':
                        continue
                    line = line.strip(' ')
                    comment_flag = False
                    i = 0
                    while i < len(line):
                        try:
                            if line[i] == '#':
                                if i == 0:
                                    comment_flag = True
                                    if 0 == len(f.readlines()):
                                        break
                                i = len(line) - 1
                            for dt in self.dataType:
                                leng = len(dt)
                                if line[i] == dt[0] and leng < len(line) - i:
                                    if line[i: i + leng] == dt and line[i + leng] == ' ':
                                        i += leng
                                        print("{:^30}{:^30}{:^30}".format('DATA_TYPE', dt, line_counter + 1))
                                        self.tokenStream.append('DATA_TYPE')
                            for dt in self.keywords:
                                leng = len(dt)
                                if line[i] == dt[0] and leng < len(line) - i:
                                    if line[i: i + leng] == dt and line[i + leng] in ' \n(;':
                                        i += leng
                                        ty = dt.replace('()', '').upper()
                                        if ty == 'NEWLINE':
                                            ty = 'OP_NEWLINE'
                                        if ty == 'OUTPUT':
                                            ty = "OP"
                                        print("{:^30}{:^30}{:^30}".format(ty, dt, line_counter + 1))
                                        self.tokenStream.append(ty)
                            for boo in self.booleans:
                                leng = len(boo)
                                if line[i] == boo[0] and leng < len(line) - i:
                                    if line[i: i + leng] == boo and line[i + leng] in ' ;':
                                        i += leng
                                        print("{:^30}{:^30}{:^30}".format('LITERAL', boo, line_counter + 1))
                                        self.tokenStream.append('LITERAL')
                            if line[i] == '>' and line[i + 1] == '=':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '>=', line_counter + 1))
                                self.tokenStream.append('REL_OP')
                            elif line[i] == '<' and line[i + 1] == '=':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '<=', line_counter + 1))
                                self.tokenStream.append('REL_OP')
                            elif line[i] == '!' and line[i + 1] == '=':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '!=', line_counter + 1))
                                self.tokenStream.append('REL_OP')
                            elif line[i] == '=' and line[i + 1] == '=':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '==', line_counter + 1))
                            elif line[i] == '|' and line[i + 1] == '|':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('LOGIC_OP', '||', line_counter + 1))
                                self.tokenStream.append('LOGIC_OP')
                            elif line[i] == '&' and line[i + 1] == '&':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('LOGIC_OP', '&&', line_counter + 1))
                                self.tokenStream.append('LOGIC_OP')
                            elif line[i] == '(':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('OPEN_BRACKET', '(', line_counter + 1))
                                self.tokenStream.append('OPEN_BRACKET')
                            elif line[i] == ')':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('CLOSE_BRACKET', ')', line_counter + 1))
                                self.tokenStream.append('CLOSE_BRACKET')
                            elif line[i] == ',':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('COMMA', ',', line_counter + 1))
                                self.tokenStream.append('COMMA')
                            elif line[i] == '+':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('LOW_ARITH', '+', line_counter + 1))
                                self.tokenStream.append('LOW_ARITH')
                            elif line[i] == '-':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('LOW_ARITH', '-', line_counter + 1))
                                self.tokenStream.append('LOW_ARITH')
                            elif line[i] == '*':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('HIGH_ARITH', '*', line_counter + 1))
                                self.tokenStream.append('HIGH_ARITH')
                            elif line[i] == '/':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('HIGH_ARITH', '/', line_counter + 1))
                                self.tokenStream.append('HIGH_ARITH')
                            elif line[i] == '<':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '<', line_counter + 1))
                                self.tokenStream.append('REL_OP')
                            elif line[i] == '>':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '>', line_counter + 1))
                                self.tokenStream.append('REL_OP')
                            elif line[i] == '#':
                                i = len(line) - 1
                                line_counter += 1
                                comment_flag = True
                            elif line[i] == ' ':
                                i += 1
                            elif line[i] == '"':
                                temp = ''
                                i += 1
                                while line[i] in string.ascii_letters + string.digits + '_ ':
                                    temp += line[i]
                                    i += 1
                                if line[i] == '"':
                                    print("{:^30}{:^30}{:^30}".format('LITERAL', '"' + temp + '"', line_counter + 1))
                                    self.tokenStream.append('LITERAL')
                                    i += 1
                                else:
                                    print("{:^30}{:^30}{:^30}".format('LEXER ERROR', '"', line_counter + 1))
                            elif line[i] == "'":
                                if line[i + 1] in string.ascii_letters + string.digits + '_' and line[i + 2] == "'":
                                    print("{:^30}{:^30}{:^30}".format('LITERAL', "'" + line[i + 1] + "'", line_counter + 1))
                                    self.tokenStream.append('LITERAL')
                                    i += 3
                            elif line[i] == '\t':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('TAB', '(tab)', line_counter + 1))
                                self.tokenStream.append('TAB')
                            # elif line[i] == '_':
                                # i += 1
                                # print("{:^30}{:^30}{:^30}".format('special_symbols', '_', line_counter + 1))
                            elif line[i] == '=':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('ASMT', '=', line_counter + 1))
                                self.tokenStream.append('ASMT')
                            elif line[i] == ';':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('SEMI_COLON', ';', line_counter + 1))
                                self.tokenStream.append('SEMI_COLON')
                            elif line[i] in string.digits:
                                temp = ''
                                while line[i] in string.digits:
                                    temp += line[i]
                                    i += 1
                                else:
                                    if line[i] == '.':
                                        temp += line[i]
                                        i += 1
                                        while line[i] in string.digits:
                                            temp += line[i]
                                            i += 1
                                if '.' in temp:
                                    print("{:^30}{:^30}{:^30}".format('NUMBER', temp, line_counter + 1))
                                    self.tokenStream.append('NUMBER')
                                else:
                                    print("{:^30}{:^30}{:^30}".format('NUMBER', temp, line_counter + 1))
                                    self.tokenStream.append('NUMBER')
                            elif line[i] in string.ascii_letters:
                                temp = ''
                                while line[i] in string.ascii_letters + string.digits + '_':
                                    temp += line[i]
                                    i += 1
                                else:
                                    if line[i] in ' (;),':
                                        print("{:^30}{:^30}{:^30}".format('IDENTIFIER', temp, line_counter + 1))
                                        self.tokenStream.append('IDENTIFIER')
                            elif line[i] == '\n':
                                if not comment_flag:
                                    print("{:^30}{:^30}{:^30}".format("NEWLINE", "newline", line_counter + 1))
                                    self.tokenStream.append('NEWLINE')
                                    line_counter += 1
                                i += 1
                            else:
                                print("{:^30}{:^30}{:^30}".format('LEXER ERROR', line[i], line_counter + 1))
                                #i += 1
                                i = len(line) - 1
                        except IndexError:
                            print("{:^30}{:^30}{:^30}".format('LEXER ERROR', line[len(line) - 1], line_counter + 1))
                            break
            sys.stdout = console
obj = Lexer()               
                
