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

def main():
    pass

if __name__ == '__main__': main()
