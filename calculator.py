#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
"""Abstract representation of the basic behaviour of a calculator."""
import logging

class Calculator():
    """Main behaviour"""
    def __init__(self,input_str):
        self.logging = logging.basicConfig(filename='caluclator.log', level=logging.INFO)
        self.input = input_str
        self.result = 0.0
        self.operations()

    def __get_operation(self):
        operation = self.input.split()
        return operation

    def operations(self):
        inpt = self.__get_operation()
        operation = ''
        for item in inpt:
            if isinstance(item, str):
                operation = item
            else:
                self.result = Calculator.processing_result(self.result, float(item), operation)
        return self.result

    @staticmethod
    def processing_result(result, item, operation):
        if operation == '*':
            result = result * item
        elif operation == '/':
            result = result / item
        elif operation == '+':
            result = result + item
        elif operation == '-':
            result = result - item
        return result

    @property
    def get_result(self):
        return self.result

def main():
    calc = Calculator('0.2 + 0.1')

main()