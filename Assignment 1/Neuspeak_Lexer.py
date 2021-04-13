import string
import sys

keywords = ['main()', 'return', 'int', 'boolean', 'char', 'float', 'else', 'if', 'output', 'for', 'newline()', 'string']
booleans = ['true', 'false']
code_path = r"E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\file4.nspk"
output_path = r"E:\BITS\Yr 3 Sem 2\CS F363 Compiler Construction\Assignments\output4.txt"
with open(output_path, "w") as out_file:
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
                    for key in keywords:
                        leng = len(key)
                        if line[i] == key[0] and leng < len(line) - i:
                            if line[i: i + leng] == key and line[i + leng] in ' (\n;':
                                i += leng
                                print("{:^30}{:^30}{:^30}".format('keyword', key, line_counter + 1))
                    for boo in booleans:
                        leng = len(boo)
                        if line[i] == boo[0] and leng < len(line) - i:
                            if line[i: i + leng] == boo and line[i + leng] in ' ;':
                                i += leng
                                print("{:^30}{:^30}{:^30}".format('boolean', boo, line_counter + 1))
                    if line[i] == '>' and line[i + 1] == '=':
                        i += 2
                        print("{:^30}{:^30}{:^30}".format('relational_symbols', '>=', line_counter + 1))
                    elif line[i] == '<' and line[i + 1] == '=':
                        i += 2
                        print("{:^30}{:^30}{:^30}".format('relational_symbols', '<=', line_counter + 1))
                    elif line[i] == '!' and line[i + 1] == '=':
                        i += 2
                        print("{:^30}{:^30}{:^30}".format('relational_symbols', '!=', line_counter + 1))
                    elif line[i] == '=' and line[i + 1] == '=':
                        i += 2
                        print("{:^30}{:^30}{:^30}".format('relational_symbols', '==', line_counter + 1))
                    elif line[i] == '|' and line[i + 1] == '|':
                        i += 2
                        print("{:^30}{:^30}{:^30}".format('logical_symbols', '||', line_counter + 1))
                    elif line[i] == '&' and line[i + 1] == '&':
                        i += 2
                        print("{:^30}{:^30}{:^30}".format('logical_symbols', '&&', line_counter + 1))
                    elif line[i] == '(':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('special_symbols', '(', line_counter + 1))
                    elif line[i] == ')':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('special_symbols', ')', line_counter + 1))
                    elif line[i] == ',':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('special_symbols', ',', line_counter + 1))
                    elif line[i] == '+':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('arithmetic_symbol', '+', line_counter + 1))
                    elif line[i] == '-':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('arithmetic_symbol', '-', line_counter + 1))
                    elif line[i] == '*':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('arithmetic_symbol', '*', line_counter + 1))
                    elif line[i] == '/':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('arithmetic_symbol', '/', line_counter + 1))
                    elif line[i] == '<':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('relational_symbols', '<', line_counter + 1))
                    elif line[i] == '>':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('relational_symbols', '>', line_counter + 1))
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
                            print("{:^30}{:^30}{:^30}".format('string', temp, line_counter + 1))
                            i += 1
                        else:
                            print("{:^30}{:^30}{:^30}".format('LEXER ERROR', '"', line_counter + 1))
                    elif line[i] == "'":
                        if line[i + 1] in string.ascii_letters + string.digits + '_' and line[i + 2] == "'":
                            print("{:^30}{:^30}{:^30}".format('char', line[i + 1], line_counter + 1))
                            i += 3
                    elif line[i] == '\t':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('whitespace', '(tab)', line_counter + 1))
                    elif line[i] == '_':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('special_symbols', '_', line_counter + 1))
                    elif line[i] == '=':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('assignment_symbols', '=', line_counter + 1))
                    elif line[i] == ';':
                        i += 1
                        print("{:^30}{:^30}{:^30}".format('special_symbols', ';', line_counter + 1))
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
                            print("{:^30}{:^30}{:^30}".format('float', temp, line_counter + 1))
                        else:
                            print("{:^30}{:^30}{:^30}".format('integer', temp, line_counter + 1))
                    elif line[i] in string.ascii_letters:
                        temp = ''
                        while line[i] in string.ascii_letters + string.digits + '_':
                            temp += line[i]
                            i += 1
                        else:
                            print("{:^30}{:^30}{:^30}".format('name', temp, line_counter + 1))
                    elif line[i] == '\n':
                        if not comment_flag:
                            print("{:^30}{:^30}{:^30}".format("whitespace", "newline", line_counter + 1))
                            line_counter += 1
                        i += 1
                    else:
                        print("{:^30}{:^30}{:^30}".format('LEXER ERROR', line[i], line_counter + 1))
                        i += 1
                except IndexError:
                    print("{:^30}{:^30}{:^30}".format('LEXER ERROR', line[len(line) - 1], line_counter + 1))
                    break
            
            
            
