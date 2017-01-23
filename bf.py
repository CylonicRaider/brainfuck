#!/usr/bin/env python
# -*- coding: ascii -*-

# Brainfuck interpreter.

TAPESIZE = 1000

class Brainfuck:
    def __init__(self, input, output, tapesize=None):
        if tapesize is None: tapesize = TAPESIZE
        self.tapesize = tapesize
        self.input = input
        self.output = output
        self.pointer = 0
        self.code = None
        self._cmdp = None
        self._bytecode = None
    def compile(self, code):
        self.code = code
        self._cmdp = 0
        bytecode = []
        stack = []
        for ch in code:
            if ch == '>':
                bytecode.append([self.do_right])
            elif ch == '<':
                bytecode.append([self.do_left])
            elif ch == '+':
                bytecode.append([self.do_incr])
            elif ch == '-':
                bytecode.append([self.do_decr])
            elif ch == '.':
                bytecode.append([self.do_output])
            elif ch == ',':
                bytecode.append([self.do_input])
            elif ch == '[':
                instr = [self.do_cjmp, None]
                stack.append(len(bytecode))
                bytecode.append(instr)
            elif ch == ']':
                try:
                    top = stack.pop()
                except IndexError:
                    raise SyntaxError('Unmatched closing brace')
                bytecode[top][1] = len(bytecode)
                bytecode.append([self.do_jmp, top])
            # Other characters are ignored.
        if stack:
            raise SyntaxError('Unmatched opening braces')
        self._bytecode = tuple(map(tuple, bytecode))

def main():
    pass

if __name__ == '__main__': main()
