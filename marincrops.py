#!/usr/bin/env python

import re
from copy import deepcopy
from datetime import datetime

louder = False

def error(expression, message):
    if type(expression) is list:
        expression = ' '.join(expression)
    print("\n\n8=>  " + str(expression))
    if louder:
        print("8==> " + message)
    else:
        print("8==> SCREAM LOUDER!!")
    quit()

class MarinEnv:
    keywords = []
    ranks_for_vars = [
        "Pvt",
        "PFC",
        "LCpl",
        "Cpl",
        "Sgt",
        "SSgt",
        "GySgt",
        "MSgt",
        "1stSgt",
        "MGySgt",
        "SgtMaj"
    ]
    expression_keywords = [
        "no",
        "yes"
    ]
    keywords = [
        "BAMCIS"
    ]
    
    short_functions = [
        'has'
    ]
    
    def parse_program_lines(lines):
        if not lines:
            lines = [" "]
        if lines[0].strip() != "attention on deck":
            global louder
            louder = True
            error(lines[0].strip(), "Well?? What do you say when your Commander steps on deck??")
        else:
            env = MarinEnv()
            env.parse_lines(lines[:2])  # Parse just the greeting.
            env.parse_lines(lines[2:])  # Parse everything else to allow the lookahead for "Louder"
        error(lines[-1].strip(), "Scream go away!!")
    
    def tokenize(line):
        parts = re.split(r'(?<!\\)(?<=(?<=^)|(?<=\s))"(.*?)(?<!\\)"(?=\s|$)', line)
        if len(parts) % 2 == 0:
            error(line, "Unmatched string literal, idiot")
        tokens = []
        count = 0
        for part in parts:
            if count % 2 == 0:
                tokens += part.strip().split(" ")
            else:
                tokens.append('"' + part + '"')
            count += 1
        return [token for token in tokens if token != '']
        
    def check_args(func_name, args, min_num, infinite = False):
        if infinite:
            if len(args) >= min_num:
                return True
            else:
                error(func_name, func_name + " requires at least " + str(min_num) + " value(s), idiot")
        else:
            if len(args) == min_num:
                return True
            else:
                error(func_name, func_name + " requires exactly " + str(min_num) + " value(s), idiot")
        
    def check_time(greeting):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        if (hour < 12 and greeting != "good morning sir") or (hour >= 12 and hour < 18 and greeting != "good afternoon sir") or (hour >= 18 and greeting != "good evening sir"):
            error(greeting, "Get back. Wrong proper greeting of the day for %04d" % (hour * 100 + minute,))
        
    def is_expression(line):
        line = line.strip()
        return (line and (line[0].isupper() or line[0] == '"' or line[0] in [str(i) for i in range(10)] or 
            any([line.startswith(exp) for exp in MarinEnv.expression_keywords])) and 
            not any([line.startswith(key) for key in MarinEnv.keywords]))
    
    def __init__(self):
        self.vars = {} # this will hold all data: ints, lists, etc.
        self.functions = {}
        
    # step through the lines. not recursive unless a function is defined.
    def parse_lines(self, lines):
        i = 0
        line = lines[0].strip()
        while MarinEnv.is_expression(line) or not line:
            if line:
                result = self.parse_blocks([line])
                if result:
                    return result
            i += 1
            line = lines[i]
        blocks = self.scan_lines(lines[i:], continue_processing = True)[0]
        #print(blocks)
        return self.parse_blocks(blocks)
    
    def parse_blocks(self, blocks):
        block_stack = []
        block_flag = None
        if not blocks or type(blocks[0]) is list:
            pass
        elif blocks[0].startswith("let's break "):
            block_flag = "func"
            func_name = re.search("(?<=^let's break )[A-Z]\S+(?= down barney-style)", blocks[0])
            if func_name is None:
                error(blocks[0], "Looks like you don't know how to write a proper name, idiot")
            func_name = func_name.group()
            var_names_matches = re.search("(?<= down barney-style for )[A-Z]\S+ [A-Z]\S+( and [A-Z]\S+ [A-Z]\S+)*(?=, frickin$)", blocks[0])
            func_var_names = []
            if var_names_matches:
                func_var_names = var_names_matches.group(0).split(' and ')
            elif not re.search("^let's break [A-Z]\S+ down barney-style, frickin$", blocks[0]):
                error(blocks[0], "You should probably go back and read the manual dummy")
            while '' in func_var_names:
                func_var_names.remove('')
            #print(func_var_names)
            self.functions[func_name] = {
                'var_names': func_var_names,
                'block': blocks
            }
            return None
        elif blocks[0].startswith('trust '):
            block_flag = 'cond'
            cond_exp = re.search("(?<=^trust ).+(?=, frickin$)", blocks[0])
            if cond_exp is None:
                error(blocks[0], "Looks like you don't know how to write a proper conditional, idiot")
            cond_exp = cond_exp.group()
            result = self.parse_expression(cond_exp, continue_processing = True)
            if result[1] not in ['yes sir', 'no sir']:
                error(blocks[0], '"yes sir" or "no sir"!!')
            else:
                if result[1] == 'no sir':
                    return None
                else:
                    blocks = blocks[1:-1]
            
        for block in blocks:
            if type(block) is list:
                result = self.parse_blocks(block)
                if result:
                    return result
            else:
                block = block.strip()
                if not block:
                    continue
                elif MarinEnv.is_expression(block):
                    result = self.parse_expression(block, continue_processing = True)
                elif block.startswith("motivate "):
                    return self.parse_expression(block.replace("motivate ", ""), continue_processing = True)
                else:
                    error(block, "Is that how you talk to a superior?")

    def scan_lines(self, lines, continue_processing = False):
        block_type = None
        enclosed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            #print(str(i) + ": scanning '" + line + "'")
            if not line:
                pass
            elif not MarinEnv.is_expression(line) or (block_type == "comment" and line != "attention on deck"):
                if block_type == "comment" and line != "attention on deck":
                    if not line.endswith(" sir"):
                        error(line, "You are still talking to your LT. You will use sir.")
                elif block_type == 'attn' and line not in ["good morning sir", "good afternoon sir", "good evening sir"]:
                    error("attention on deck\n\t" + line, "I know we scream the proper greeting of the day.")
                elif i == 0:
                    if line.startswith("let's break "): # Defining a function
                        block_type = "func"
                        enclosed_lines.append(line)
                    elif line.startswith("trust "):
                        block_type = "cond"
                        enclosed_lines.append(line)
                    elif line == "i heard through the lance corporal underground":
                        block_type = "comment"
                    elif line == "attention on deck":
                        block_type = "attn"
                    else:
                        error(line, "Unrecognized keyword")
                elif line == 'kill' or line == 'BAMCIS':
                    if line == 'kill':
                        if block_type != "cond":
                            error(line, "You're on the wrong block")
                    elif line == 'BAMCIS':
                        if block_type != 'func':
                            error(line, "You're on the wrong block")
                    enclosed_lines.append(line)
                    if not continue_processing:
                        return (enclosed_lines, i)
                    else:
                        result = self.scan_lines(lines[i+1:], continue_processing = True)[0]
                        result.insert(0, enclosed_lines)
                        return result
                    return (enclosed_lines, i)
                elif line == "attention on deck" and block_type == "comment":
                    block_type = "attn"
                elif line in ["good morning sir", "good afternoon sir", "good evening sir"]:
                    if block_type != "attn":
                        error(line, "What are you saying that for? Do I look like I care?")
                    MarinEnv.check_time(line)
                    if not continue_processing:
                        return ([], i)
                    else:
                        return self.scan_lines(lines[i+1:], continue_processing = True)
                elif line.startswith("motivate "):
                    enclosed_lines.append(line)
                else:
                    # start a new block
                    scan_result = self.scan_lines(lines[i:])
                    enclosed_lines.append(scan_result[0])
                    i += scan_result[1]
            else:
                enclosed_lines.append(line)
            i += 1
        
        return (enclosed_lines, i)
    
    def parse_expression(self, expression, last_var = None, continue_processing = False):
        flag = None
        remainder = []
        rank = None
        function_name = None
        current_vars = []
        if last_var:
            current_vars.append(last_var)
        
        i = 0
        tokens = expression
        if type(expression) != list:
            tokens = MarinEnv.tokenize(expression)
        
        while i < len(tokens):
            word = tokens[i]
            if flag == "aye" and word != "sir":
                error(expression, "AYE WHAT? WHAT??")
            if flag == "int" and word != "crayon" and word != "crayons":
                error(expression, str(last_var[1]) + " WHAT? WHAT??")
            
            if word in MarinEnv.ranks_for_vars or word[0] == '"' or word[0] in [str(i) for i in range(1, 10)]:
                if current_vars and not function_name:
                    error(expression, "Yeah right get back")
                elif flag == "func" or (flag == "and" and function_name) or flag == None:
                    if word in MarinEnv.ranks_for_vars:
                        rank = word
                        flag = "rank"
                    elif word[0] == '"':
                        word = word[1:-1] #strips the quotes off. tokenize always leaves the quotes on the outside
                        word = word.replace('\\"', '"').replace('\\t', "\t").replace('\\n', "\n")
                        flag = "var"
                        last_var = (None, [ord(c) for c in word])
                        current_vars.append(last_var) # converts all strings to a list of characters
                    elif word[0] in [str(i) for i in range(1, 10)]:
                        if word == '1':
                            error(expression, "We aren't in the Air Force here. A crayon! A crayon!")
                        value = int(word)
                        flag = "int"
                        last_var = (None, value)
                        current_vars.append(last_var)
                    else:
                        error(expression, "Good job, dunce. You broke something.")
                elif flag == "var" and function_name: # regular nesting starting with an infix operation
                    result = self.parse_expression(tokens[i:])
                    last_var = (None, result[0])
                    current_vars.append(last_var)
                    i += result[1]
                    flag = "var"
                else:
                    error(expression, "Improper use of rank")
            elif word[0].isupper():
                if flag == "rank":
                    var_name = rank + " " + word
                    last_var = (var_name, self.get_value(var_name))
                    current_vars.append(last_var)
                    rank = None
                    flag = "var"
                else:
                    if function_name: # nesting
                        if flag == "and" or flag == "func":
                            result = self.parse_expression(tokens[i:])
                            last_var = (None, result[0])
                            current_vars.append(last_var)
                            i += result[1]
                            flag = "var"
                        elif flag == "var": # infix nesting
                            result = self.parse_expression(tokens[i:], last_var = last_var)
                            current_vars.pop()
                            last_var = (None, result[0])
                            current_vars.append(last_var)
                            i += result[1]
                            flag = "var"
                    else:
                        function_name = word
                        flag = "func"
            elif word[0].islower():
                if flag == "rank":
                    error(expression, "Yeah right! I know we capitalize our names")
                elif word == "no" or word == "yes" or word == "a":
                    flag = word
                elif flag == "and":
                    error(expression, "Yeah right! I know we capitalize our names")
                elif word == "aye":
                    if not function_name:
                        error(expression, "What are you saying aye for? Do you even know what you're saying?")
                    else:
                        flag = "aye"
                elif word == "sir":
                    if flag == "aye":
                        last_var = (None, self.run_function(function_name, current_vars))
                        if not continue_processing:
                            return (last_var[1], i)
                        else:
                            if i + 1 < len(tokens): # There are still tokens left to process
                                return self.parse_expression(tokens[i+1:], last_var = last_var, continue_processing = True)
                            else:
                                return last_var
                    elif flag == "no" or flag == "yes":
                        last_var = (None, flag + " sir")
                        current_vars.append(last_var)
                        flag = "var"
                    else:
                        error(expression, "SIR WHAT? WHAT??")
                elif word == "and":
                    if flag == "func":
                        error(expression, "It's not the same Marin Crops as when I was a Lance Coolie.")
                    else:
                        flag = "and"
                elif word in MarinEnv.short_functions:
                    function_name = word
                    flag = "func"
                elif word == "crayon" or word == "crayons":
                    if flag == "no":
                        if word == "crayon":
                            error(expression, "Go retake Grammar for Marines on MarineNet, idiot")
                        else:
                            last_var = (None, 0)
                            current_vars.append(last_var)
                            flag = "var"
                    elif flag == "a":
                        if word == "crayon":
                            last_var = (None, 1)
                            current_vars.append(last_var)
                            flag = "var"
                        else:
                            error(expression, "Go retake Grammar for Marines on MarineNet, idiot")
                    else:
                        if flag != "int":
                            error(expression, "You must not be a real Marine. Don't even know what a crayon is, idiot")
                        else:
                            if (last_var[1] == 1 and word == "crayons") or (last_var[1] != 1 and word == "crayon"):
                                error(expression, "Go retake Grammar for Marines on MarineNet, idiot")
                            else:
                                flag = "var"
                else:
                    error(expression, "Yeah right! I know we capitalize our names")
            else:
                error(expression, "Unrecognized initial character, idiot")
            i += 1
        
        if function_name in MarinEnv.short_functions:
            return self.run_function(function_name, current_vars)
        elif not function_name and len(current_vars) > 0:
            return last_var
        else:
            error(expression, "Scream aye sir!")
    
    def run_function(self, function_name, args): #args is a list of tuples with names and values
        if function_name in self.functions.keys():
            func = self.functions[function_name]
            MarinEnv.check_args(function_name, args, len(func['var_names']))
            env = MarinEnv()
            env.vars = deepcopy(self.vars)
            env.functions = deepcopy(self.functions)
            for i in range(len(args)):
                env.vars[func['var_names'][i]] = args[i][1]
            result = env.parse_blocks(func['block'][1:-1]) # remove the header and footer keywords in the function
            if result:
                return result[1]
            else:
                return "no sir"
        elif function_name == "has":
            MarinEnv.check_args(function_name, args, 2)
            if args[0][0] == None:
                error(function_name, "You know you can't assign to a literal value, idiot")
            self.set_value(args[0][0], args[1][1])
            return args[1][1]
        elif function_name == "Is":
            MarinEnv.check_args(function_name, args, 2)
            return "yes sir" if args[0][1] == args[1][1] else "no sir"
        elif function_name == "Has":
            MarinEnv.check_args(function_name, args, 2)
            return "yes sir" if args[0][1] == args[1][1] else "no sir"
        elif function_name == "Has_less_than":
            MarinEnv.check_args(function_name, args, 2)
            return "yes sir" if args[0][1] < args[1][1] else "no sir"
        elif function_name == "Has_more_than":
            MarinEnv.check_args(function_name, args, 2)
            return "yes sir" if args[0][1] > args[1][1] else "no sir"
        elif function_name == "Louder":
            MarinEnv.check_args(function_name, args, 0)
            global louder
            louder = True
            return "yes sir"
        elif function_name == "Scream":
            MarinEnv.check_args(function_name, args, 1, True)
            for arg in args:
                value = arg[1]
                if type(value) == list:
                    value = ''.join([chr(i) for i in value])
                print(str(value).upper(), end="")
            return args[0][1]
        elif function_name == "Next_motivator":
            MarinEnv.check_args(function_name, args, 0)
            return input()
        elif function_name == "One_more_than":
            MarinEnv.check_args(function_name, args, 1)
            return args[0][1] + 1
        elif function_name == "One_less_than":
            MarinEnv.check_args(function_name, args, 1)
            return args[0][1] - 1
        elif function_name == "Go_away":
            MarinEnv.check_args(function_name, args, 0)
            quit()
        else:
            error(function_name, "Function not found")
        
    def get_value(self, var_name):
        if var_name in self.vars.keys():
            return self.vars[var_name]
        else:
            return None
            
    def set_value(self, var_name, value):
        self.vars[var_name] = value
        
        
# ============== main logic ==============

import sys

filename = sys.argv[1]

program_lines = ""
with open(filename) as f:
    program_lines = f.readlines()

MarinEnv.parse_program_lines(program_lines)