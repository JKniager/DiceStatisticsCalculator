from enum import Enum, auto
import math
import queue
from queue import LifoQueue
from typing import List, Tuple


class Function:
    def iterateValues(self):
        raise NotImplementedError


class Constant(Function):
    def __init__(self, num_const: float):
        self.num_const = num_const
    
    def iterateValues(self):
        yield self.num_const


class Combiner(Function):
    def __init__(self, func_1, func_2):
        self.func_1 = func_1
        self.func_2 = func_2
    
    def iterateValues(self):
        raise NotImplementedError


class Dice(Combiner):
    def __init__(self, count: Function, sides: Function):
        super().__init__(count, sides)
    
    def iterateValues(self):
        '''For all dice and possibilities, calculate the sum of each of those possible roll combinations.
        Since number of dice or number of sides could technically be an equation, we must also iterate through
        the possible outputs of those other equations.
        '''
        for side_count in self.func_2.iterateValues():
            for dice_count in self.func_1.iterateValues():
                dice = [1 for i in range(dice_count)]
                done = False
                
                while not done:
                    dice_total = sum(dice)
                    yield dice_total
                    for i in range(dice_count):
                        dice[i] += 1
                        if dice[i] > side_count:
                            dice[i] = 1
                            done = True
                        else:
                            done = False
                            break

        yield None


class Add(Combiner):
    def __init__(self, func_1, func_2):
        super().__init__(func_1, func_2)
    
    def iterateValues(self):
        for i in self.func_1.iterateValues():
            if i is None:
                yield None
            for j in self.func_2.iterateValues():
                if j is None:
                    break
                yield i + j

class Sub(Combiner):
    def __init__(self, func_1, func_2):
        super().__init__(func_1, func_2)
    
    def iterateValues(self):
        for i in self.func_1.iterateValues():
            if i is None:
                yield None
            for j in self.func_2.iterateValues():
                if j is None:
                    break
                yield i - j

class Mul(Combiner):
    def __init__(self, func_1, func_2):
        super().__init__(func_1, func_2)
    
    def iterateValues(self):
        for i in self.func_1.iterateValues():
            if i is None:
                yield None
            for j in self.func_2.iterateValues():
                if j is None:
                    break
                yield i * j

class Div(Combiner):
    def __init__(self, func_1, func_2):
        super().__init__(func_1, func_2)
    
    def iterateValues(self):
        for i in self.func_1.iterateValues():
            if i is None:
                yield None
            for j in self.func_2.iterateValues():
                if j is None:
                    break
                yield i / j


class StatCalculator(Function):
    def __init__(self, combiner):
        self.combiner = combiner
        
        self.average = 0
        self.std_dev = 0
        self.total_combinations = 0
        self.database = {}
    
    def calcStats(self):
        self.average = 0
        self.std_dev = 0
        self.total_combinations = 0
        self.database = {}
        
        for v in self.combiner.iterateValues():
            if v is None:
                break
            
            if v in self.database:
                self.database[v] += 1
            else:
                self.database[v] = 1
            self.average += v
            self.total_combinations += 1
        
        self.average /= self.total_combinations
        
        for k, v in self.database.items():
            num = int(k) - self.average
            num *= num
            
            self.std_dev += num * v
        
        self.std_dev /= self.total_combinations
        self.std_dev = math.sqrt(self.std_dev)
    
    def iterateValues(self):
        for k, v in self.database.items():
            yield (k, v)
    
    def iterateStats(self):
        for k, v in self.database.items():
            yield (k, v / self.total_combinations)


class InvalidInfixExpressionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BadFormulaFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CombinerFactory:
    operators = {
        '+': Add,
        '-': Sub,
        '*': Mul,
        '/': Div,
        'd': Dice
    }
    
    operator_order = {
        'd' : 0,
        '*' : 1,
        '/' : 1,
        '+' : 2,
        '-' : 2
    }
    
    @staticmethod
    def formula_split(f: str) -> List[str]:
        working_string = "".join(f.split())
        working_string = working_string.replace(",", "")

        out = []
        num_string = ""
        decimal_last = False
        for c in working_string:
            if c.isdigit():
                num_string += c
                decimal_last = False
            elif c == '.':
                if decimal_last:
                    raise BadFormulaFormatError("Two decimal points found next to each other!")
                num_string += c
                decimal_last = True
            elif len(num_string) > 0:
                out.append(num_string)
                num_string = ""
                out.append(c.lower())
        
        if len(num_string) > 0:
            out.append(num_string)
        
        return out
            

    @staticmethod
    def is_operator(c: str) -> bool:
        return c in CombinerFactory.operators
    
    @staticmethod
    def compare_operator_order(first_operator: str, second_operator: str) -> bool:
        return CombinerFactory.operator_order[first_operator] <= CombinerFactory.operator_order[second_operator]
    
    @staticmethod
    def evaluate_operator(operator: Function, first_operand: Function, second_operand: Function) -> Function:
        return CombinerFactory.operators[operator](first_operand, second_operand)
    
    def __init__(self, equation: str):
        self.equation = equation
    
    def constructCombinerPostfix(self):
        stack = []
        instructions = self.equation.split()
        for i in instructions:
            if i.isnumeric():
                stack.append(Constant(int(i)))
            elif i in self.operators:
                second = stack.pop()
                first = stack.pop()
                stack.append(self.evaluate_operator(first, second, self.operators[i]))
            else:
                raise NameError
        return stack[0]
    
    def constructCombiner(self):
        instructions = CombinerFactory.formula_split(self.equation)
        if len(instructions) == 0:
            return None

        operator_stack = LifoQueue()
        number_stack = LifoQueue()

        expecting_number = True
        for i in instructions:
            if CombinerFactory.is_operator(i):
                if expecting_number:
                    raise InvalidInfixExpressionError(f"Expression '{self.equation}' is misformatted!")
                # Make sure there aren't any operations we have to perform before the current operator 'i'.
                while not operator_stack.empty():
                    test_operator = operator_stack.get_nowait()
                    if test_operator == '(' or not CombinerFactory.compare_operator_order(test_operator, i):
                        operator_stack.put_nowait(test_operator)
                        break
                    else:
                        second_operand = None
                        first_operand = None
                        try:
                            second_operand = number_stack.get_nowait()
                            first_operand = number_stack.get_nowait()
                        except queue.Empty:
                            raise InvalidInfixExpressionError(f"Expression '{self.equation}' is missing an operand!")
                        number_stack.put_nowait(CombinerFactory.evaluate_operator(test_operator, first_operand, second_operand))
                operator_stack.put_nowait(i)
                expecting_number = True
            elif i == '(':
                if not expecting_number:
                    raise InvalidInfixExpressionError(f"Expression '{self.equation}' is misformatted!")
                operator_stack.put_nowait(i)
            elif i == ')':
                if expecting_number:
                    raise InvalidInfixExpressionError(f"Expression '{self.equation}' is misformatted!")
                test_operator = ''
                try:
                    test_operator = operator_stack.get_nowait()
                except queue.Empty:
                    raise InvalidInfixExpressionError(f"Expression '{self.equation}' is missing a '('!")
                while test_operator != '(':
                    second_operand = None
                    first_operand = None
                    try:
                        second_operand = number_stack.get_nowait()
                        first_operand = number_stack.get_nowait()
                    except queue.Empty:
                        raise InvalidInfixExpressionError(f"Expression '{self.equation}' is missing an operand!")
                    number_stack.put_nowait(CombinerFactory.evaluate_operator(test_operator, first_operand, second_operand))
                    try:
                        test_operator = operator_stack.get_nowait()
                    except queue.Empty:
                        raise InvalidInfixExpressionError(f"Expression '{self.equation}' is missing a '('!")
            else:
                if not expecting_number:
                    raise InvalidInfixExpressionError(f"Expression '{self.equation}' is misformatted!")
                number_stack.put_nowait(Constant(int(i)))
                expecting_number = False
        
        while not operator_stack.empty():
            operator = operator_stack.get_nowait()
            if operator == '(':
                raise InvalidInfixExpressionError(f"Expression '{self.equation}' is missing a ')'!")

            second_operand = None
            first_operand = None
            try:
                second_operand = number_stack.get_nowait()
                first_operand = number_stack.get_nowait()
            except queue.Empty:
                raise InvalidInfixExpressionError(f"Expression '{self.equation}' is missing an operand!")
            number_stack.put_nowait(CombinerFactory.evaluate_operator(operator, first_operand, second_operand))
        
        if number_stack.qsize() > 1:
            raise InvalidInfixExpressionError(f"Expression '{self.equation}' has an extra operand!")

        return number_stack.get_nowait()


class EmptyFormulaGivenError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def dice_calculator_wrapper(formula: str) -> Tuple[List[float], List[float]]:
    cf = CombinerFactory(formula)
    co = cf.constructCombiner()
    if co is None:
        raise EmptyFormulaGivenError("Given formula was an empty string!")

    sc = StatCalculator(co)
    sc.calcStats()
    stats = sc.iterateValues()
    outcomes = []
    quantities = []

    for s in stats:
        outcomes.append(s[0])
        quantities.append(s[1] / sc.total_combinations)
    
    return (outcomes, quantities)

def main():
    cf = CombinerFactory("3 d 4 - 3 + 3 d 6")
    sc = StatCalculator(cf.constructCombiner())
    sc.calcStats()
    stats = sc.iterateValues()
    
    print("{} / {}".format(sc.average, sc.std_dev))
    for s in stats:
        print("{0}: {1} ({2:.3f})".format(s[0], s[1], (s[1] / sc.total_combinations) * 100))


if __name__ == '__main__':
    main()