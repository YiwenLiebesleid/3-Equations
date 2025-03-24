import random
import os
import re
import numpy as np
import pandas as pd
from sympy import Symbol, Eq, Function, Rational, latex, log
from sympy.printing.latex import LatexPrinter

# defined choices
ALPHABET = "qwertyuiopasdfghjklzxcvbnm"

# probailities
NO_VAR = 0.33
FRAC = 0.3
INT_COEFF_ABSENT = 0.3
EXP = 0.2
LOG = 0.1

# max values
EXP_MAX = 10
LOG_BASE_MAX = 10
MAX_NUM = 50

# custom latex printer to get "\frac{a}{b} x" format for Rationals
class CustomLatexPrinter(LatexPrinter):
    def _print_Mul(self, expr):
        # check that the first term is a rational
        if isinstance(expr.args[0], Rational):
            return r"\frac{%s}{%s} %s" % (self._print(expr.args[0].p), self._print(expr.args[0].q), self._print(expr.args[1]))
        else:
            return super()._print_Mul(expr)

def rand_term():
    """
    A random term will be in the format [log_a]?cv^e, where c is a coefficient, v is a variable, and e is an exponent.
     - c has FRAC probability of being a fraction vs an integer. If it's an integer, it will have an INT_COEFF_ABSENT 
       chance of being 1, meaning it's omitted from the equation.
     - v will either be nothing (probability = NO_VAR) or one of the 26 letters (the remaining probability divided 
       evenly among all letters). 
     - e has EXP probability of existing, and will be between 2 and EXP_MAX.
     - there is a LOG probability of having a log with random base (from 2 to LOG_BASE_MAX) around c or cv (50-50 chance).

    :return the term (LaTeX string) and the spoken word translation of the equation (str)
    """

    # get a random variable with a random exponent
    var = "" if (random.random() < NO_VAR) else random.choice(ALPHABET)
    var_expr = Symbol(var)
    var_plaintext = str(var)

    if var != "" and random.random() < EXP:
        e = random.randint(2, EXP_MAX)
        var_expr = Symbol(var)**e
        var_plaintext = f"{var_plaintext} to the power of {e}"

    # build coefficient
    if random.random() < FRAC:
        # build a random fraction according to rules
        numerator = random.randint(1, MAX_NUM)
        denominator = random.randint(2, MAX_NUM)
        coeff_expr = Rational(numerator, denominator)

        # because Rational automatically simplifies numbers
        numerator = coeff_expr.p
        denominator = coeff_expr.q

        # construct plaintext
        coeff_plaintext = f"{numerator} over {denominator}"
    else:
        # build a random integer according to rules
        coeff = "" if (random.random() < INT_COEFF_ABSENT and var != "") else str(random.randint(2, MAX_NUM))
        coeff_expr = Symbol(coeff)
        coeff_plaintext = str(coeff)
    
    # determine log (TODO add base manually bc sympy is stupid)
    if random.random() < LOG:
        r = random.random()
        if r < 0.5 and var_plaintext != "":
            # put log around just coeff
            expr = coeff_expr * log(var_expr)
            plaintext = f"{coeff_plaintext} log of {var_plaintext}"
        elif r > 0.5 and (coeff_plaintext != "" or var_plaintext != ""):
            # put log around both coeff and variable
            expr = log(coeff_expr * var_expr)
            plaintext = f"log of {coeff_plaintext} {var_plaintext}"
        else:
            expr = 1
            plaintext = "1"

    else:
        # attach coeff and variable
        expr = coeff_expr * var_expr
        plaintext = f"{coeff_plaintext} {var_plaintext}"

    # output constructed term
    plaintext = plaintext.replace("  ", " ").strip() # eliminate double/leading/trailing spaces
    return CustomLatexPrinter().doprint(expr), plaintext

def rand_equation():
    # generate 3-4 terms for the equation
    left_operand, left_plaintext = rand_term()
    right_operand, right_plaintext = rand_term()
    answer, answer_plaintext = rand_term()

    # randomly add or subtract terms, and add equals term at the end
    if random.random() < 0.5:
        expr = f"{left_operand} + {right_operand} = {answer}"
        plaintext = f"{left_plaintext} plus {right_plaintext} equals {answer_plaintext}"
    else:
        expr = f"{left_operand} - {right_operand} = {answer}"
        plaintext = f"{left_plaintext} minus {right_plaintext} equals {answer_plaintext}"

    # output combined expression and plaintext
    return expr, plaintext

def main():
    N = 10000 # number of examples
    E = 3 # number of equations per example
    data = np.zeros((N, 2*E), dtype=object)

    # generate data
    for i in range(N):
        for j in range(E):
            eqn_text, audio_text = rand_equation()
            data[i, j*2] = eqn_text
            data[i, j*2+1] = audio_text
    
    # save as a csv
    pd.DataFrame(data).to_csv("../dataset.csv", index=False, header=False)

if __name__ == "__main__":
    main()
