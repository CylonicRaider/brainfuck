#!/usr/bin/env python
# -*- coding: ascii -*-

# Brainfuck interpreter.

import sys

def read_byte():
    try:
        ch = sys.stdin.buffer.read(1)
    except AttributeError:
        ch = sys.stdin.read(1)
    return ord(ch) if ch else 0
def write_byte(b):
    try:
        sys.stdout.buffer.write(bytes([b]))
        sys.stdout.buffer.flush()
    except AttributeError:
        sys.stdout.write(chr(b))
        sys.stdout.flush()

class Brainfuck:
    def _compile(self, ch, bytecode, state):
        if ch is None:
            if state['loopstack']:
                raise SyntaxError('Unmatched opening bracket')
        elif ch == '>':
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
            state['loopstack'].append(len(bytecode))
            bytecode.append(instr)
        elif ch == ']':
            try:
                top = state['loopstack'].pop()
            except IndexError:
                raise SyntaxError('Unmatched closing bracket')
            bytecode.append([self.do_jmp, top])
            bytecode[top][1] = len(bytecode)
    COMPILERS = {'>': _compile, '<': _compile, '+': _compile, '-': _compile,
                 '.': _compile, ',': _compile, '[': _compile, ']': _compile}
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.pointer = 0
        self.tape = {}
        self.code = None
        self._cmdp = None
        self._bytecode = None
    def compile(self, code):
        self.code = code
        self._cmdp = 0
        bytecode = []
        state = {'loopstack': []}
        for ch in code:
            comp = self.COMPILERS.get(ch)
            if comp: comp(self, ch, bytecode, state)
        handled = set()
        for c in self.COMPILERS.values():
            if c in handled: continue
            handled.add(c)
            comp(self, None, bytecode, state)
        self._bytecode = tuple(map(tuple, bytecode))
    def do_right(self):
        self.pointer += 1
    def do_left(self):
        self.pointer -= 1
    def do_incr(self):
        value = self.tape.get(self.pointer, 0)
        self.tape[self.pointer] = (value + 1) % 255
    def do_decr(self):
        value = self.tape.get(self.pointer, 0)
        self.tape[self.pointer] = (value - 1) % 255
    def do_output(self):
        self.output(self.tape.get(self.pointer, 0))
    def do_input(self):
        self.tape[self.pointer] = self.input()
    def do_cjmp(self, where):
        if not self.tape.get(self.pointer): return where
    def do_jmp(self, where):
        return where
    def run(self, code=None):
        if code is not None: self.compile(code)
        while self._cmdp < len(self._bytecode):
            instr = self._bytecode[self._cmdp]
            res = instr[0](*instr[1:])
            if res is None:
                self._cmdp += 1
            else:
                self._cmdp = res

def main():
    commands, cmdfile = None, None
    if len(sys.argv) <= 1:
        usage(1)
    elif sys.argv[1] == '--help':
        usage(0)
    elif sys.argv[1] == '-c':
        if len(sys.argv) != 3: usage(1)
        commands = sys.argv[2]
    elif sys.argv[1] == '--':
        if len(sys.argv) != 3: usage(1)
        cmdfile = sys.argv[1]
    elif sys.argv[1].startswith('-'):
        usage(1)
    else:
        cmdfile = sys.argv[1]
    if cmdfile is not None:
        with open(cmdfile) as f:
            commands = f.read()
    bf = Brainfuck(read_byte, write_byte)
    bf.run(commands)

if __name__ == '__main__': main()
