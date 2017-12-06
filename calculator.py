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
        self.result = 'undefined'
        self.operations()

    def __get_operation(self):
        operation = self.input.split()
        return operation

    def operations(self):
        counter = 0
        inpt = self.__get_operation()
        output = self.__to_numbers(inpt)
        operands = output[0]
        operations = output[1]
        for operand in operands:
            if self.result == 'undefined':
                self.result = operand
            else:
                self.result = self.processing_result(self.result, operand, operations[counter/2-1])
            counter += 1
        return self.result

    @staticmethod
    def processing_result(result, operand, operation):
        if operation == '*':
            result *= operand
        elif operation == '/':
            if operand == 0:
                raise ZeroDivisionError('float division by zero')
            else:
                result /= operand
        elif operation == '+':
            result += operand
        elif operation == '-':
            result -= operand
        elif operation == '^':
            result **= operand
        return result

    @property
    def get_result(self):
        return self.result

    def __to_numbers(self, inpt):
        operands = []
        operator = []
        for item in inpt:
            try:
               operands.append(float(item))
            except ValueError:
                operator.append(item)
        return (operands, operator)
