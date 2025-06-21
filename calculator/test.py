from pkg.calculator import Calculator
import sys

if __name__ == "__main__":
    expression = " ".join(sys.argv[1:])
    calculator = Calculator()
    result = calculator.evaluate(expression)
    print(result)
