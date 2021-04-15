import string
import sys

class Lexer:
    def __init__(self, code_path, out_path):
        """[summary]
        """
        self.tokenStream = []
        self.lineNumbers = []
        self.keywords = ['main()', 'return', 'else', 'if', 'output', 'while', 'newline()']
        self.dataType = ['int', 'boolean', 'char', 'float', 'string']
        self.booleans = ['true', 'false']
        
        self.code_path = code_path
        self.output_path = out_path
        
        self.getTokenStream()
        self.tokenStream.append('$')
        self.writeStream()

    def getTokenStream(self):
        with open(self.output_path, "w") as out_file:
            console = sys.stdout
            sys.stdout = out_file
            print("{:*^30}{:*^30}{:*^30}".format("Token", "Lexeme", "Line Number"))
            with open(self.code_path, 'r') as f:
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
                                        self.tokenStream.append('[DT]')
                                        self.lineNumbers.append(line_counter + 1)
                            for dt in self.keywords:
                                leng = len(dt)
                                if line[i] == dt[0] and leng < len(line) - i:
                                    if line[i: i + leng] == dt and line[i + leng] in ' \n(;':
                                        i += leng
                                        ty = dt.replace('()', '').upper()
                                        ts = ''
                                        if ty == 'NEWLINE':
                                            ts = 'ON'
                                            ty = 'OUTPUT NEWLINE'
                                        if ty == 'OUTPUT':
                                            ts = "OP"
                                        if ty == 'WHILE':
                                            ts = 'W'
                                        if ty == 'ELSE':
                                            ts='E'
                                        if ty == 'RETURN':
                                            ts = 'R'
                                        if ty == 'MAIN':
                                            ts = 'M'
                                        if ty == 'IF':
                                            ts = 'IF'
                                        ts = '[' + ts + ']'
                                        print("{:^30}{:^30}{:^30}".format(ty, dt, line_counter + 1))
                                        self.tokenStream.append(ts)
                                        self.lineNumbers.append(line_counter + 1)
                            for boo in self.booleans:
                                leng = len(boo)
                                if line[i] == boo[0] and leng < len(line) - i:
                                    if line[i: i + leng] == boo and line[i + leng] in ' ;':
                                        i += leng
                                        print("{:^30}{:^30}{:^30}".format('LITERAL', boo, line_counter + 1))
                                        self.tokenStream.append('[L]')
                                        self.lineNumbers.append(line_counter + 1)
                            if line[i] == '>' and line[i + 1] == '=':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '>=', line_counter + 1))
                                self.tokenStream.append('[RO]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '<' and line[i + 1] == '=':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '<=', line_counter + 1))
                                self.tokenStream.append('[RO]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '!' and line[i + 1] == '=':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '!=', line_counter + 1))
                                self.tokenStream.append('[RO]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '=' and line[i + 1] == '=':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '==', line_counter + 1))
                                self.tokenStream.append('[RO]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '|' and line[i + 1] == '|':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('LOGIC_OP', '||', line_counter + 1))
                                self.tokenStream.append('[LO]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '&' and line[i + 1] == '&':
                                i += 2
                                print("{:^30}{:^30}{:^30}".format('LOGIC_OP', '&&', line_counter + 1))
                                self.tokenStream.append('[LO]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '(':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('OPEN_BRACKET', '(', line_counter + 1))
                                self.tokenStream.append('[OB]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '{':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('CURLY_OPEN', '(', line_counter + 1))
                                self.tokenStream.append('[CO]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == ')':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('CLOSE_BRACKET', ')', line_counter + 1))
                                self.tokenStream.append('[CB]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '}':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('CURLY_CLOSE', ')', line_counter + 1))
                                self.tokenStream.append('[CC]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == ',':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('COMMA', ',', line_counter + 1))
                                self.tokenStream.append('[C]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '+':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('LOW_ARITH', '+', line_counter + 1))
                                self.tokenStream.append('[LA]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '@':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('CALL', ',', line_counter + 1))
                                self.tokenStream.append('[CL]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '-':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('LOW_ARITH', '-', line_counter + 1))
                                self.tokenStream.append('[LA]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '*':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('HIGH_ARITH', '*', line_counter + 1))
                                self.tokenStream.append('[HA]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '/':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('HIGH_ARITH', '/', line_counter + 1))
                                self.tokenStream.append('[HA]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '<':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '<', line_counter + 1))
                                self.tokenStream.append('[RO]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '>':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('REL_OP', '>', line_counter + 1))
                                self.tokenStream.append('[RO]')
                                self.lineNumbers.append(line_counter + 1)
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
                                    self.tokenStream.append('[L]')
                                    self.lineNumbers.append(line_counter + 1)
                                    i += 1
                                else:
                                    print("{:^30}{:^30}{:^30}".format('---lexer error---', '"', line_counter + 1))
                            elif line[i] == "'":
                                if line[i + 1] in string.ascii_letters + string.digits + '_' and line[i + 2] == "'":
                                    print("{:^30}{:^30}{:^30}".format('LITERAL', "'" + line[i + 1] + "'", line_counter + 1))
                                    self.tokenStream.append('[L]')
                                    self.lineNumbers.append(line_counter + 1)
                                    i += 3
                            elif line[i] == '\t':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('TAB', '(tab)', line_counter + 1))
                                self.tokenStream.append('[T]')
                                self.lineNumbers.append(line_counter + 1)
                            # elif line[i] == '_':
                                # i += 1
                                # print("{:^30}{:^30}{:^30}".format('special_symbols', '_', line_counter + 1))
                            elif line[i] == '=':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('ASMT', '=', line_counter + 1))
                                self.tokenStream.append('[AS]')
                                self.lineNumbers.append(line_counter + 1)
                            elif line[i] == ';':
                                i += 1
                                print("{:^30}{:^30}{:^30}".format('SEMI_COLON', ';', line_counter + 1))
                                self.tokenStream.append('[SC]')
                                self.lineNumbers.append(line_counter + 1)
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
                                    self.tokenStream.append('[N]')
                                    self.lineNumbers.append(line_counter + 1)
                                else:
                                    print("{:^30}{:^30}{:^30}".format('NUMBER', temp, line_counter + 1))
                                    self.tokenStream.append('[N]')
                                    self.lineNumbers.append(line_counter + 1)
                            elif line[i] in string.ascii_letters:
                                temp = ''
                                while line[i] in string.ascii_letters + string.digits + '_':
                                    temp += line[i]
                                    i += 1
                                else:
                                    if line[i] in ' (;),':
                                        print("{:^30}{:^30}{:^30}".format('IDENTIFIER', temp, line_counter + 1))
                                        self.tokenStream.append('[ID]')
                                        self.lineNumbers.append(line_counter + 1)
                            elif line[i] == '\n':
                                if not comment_flag:
                                    print("{:^30}{:^30}{:^30}".format("NEWLINE", "newline", line_counter + 1))
                                    self.tokenStream.append('[NL]')
                                    self.lineNumbers.append(line_counter + 1)
                                    line_counter += 1
                                i += 1
                            else:
                                print("{:^30}{:^30}{:^30}".format('---lexer error---', line[i], line_counter + 1))
                                #i += 1
                                i = len(line) - 1
                        except IndexError:
                            print("{:^30}{:^30}{:^30}".format('---lexer error---', line[len(line) - 1], line_counter + 1))
                            break
            sys.stdout = console
    
    def writeStream(self):
        self.lineNumbers.append(100)
        with open(self.output_path, 'a') as f:
            f.write('\n\n\nTOKEN STREAM\n')
            for ts, ln in zip(self.tokenStream, self.lineNumbers):
                f.write(ts + '\t' + str(ln) + '\n')
                
