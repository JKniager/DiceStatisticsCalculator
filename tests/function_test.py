import pytest
from dice_statistic_calculator.DiceStatCalculator import Add, Constant, Dice, Div, Mul, Sub


class TestConstant:

    def test_constant_yields_stored_value(self):
        test_value = 4
        test_constant = Constant(test_value)

        for i in test_constant.iterateValues():
            assert i == test_value


class TestCombiner:

    def test_addition(self):
        test_value = 2 + 2
        test_combiner = Add(Constant(2), Constant(2))

        for i in test_combiner.iterateValues():
            assert i == test_value
    
    def test_subtraction(self):
        test_value = 2 - 2
        test_combiner = Sub(Constant(2), Constant(2))

        for i in test_combiner.iterateValues():
            assert i == test_value
    
    def test_multiplication(self):
        test_value = 2 * 2
        test_combiner = Mul(Constant(2), Constant(2))

        for i in test_combiner.iterateValues():
            assert i == test_value
    
    def test_division(self):
        test_value = 2 / 2
        test_combiner = Div(Constant(2), Constant(2))

        for i in test_combiner.iterateValues():
            assert i == test_value
    
    def test_multiple_addition(self):
        test_value = 2 + 2 + 4
        test_combiner = Add(Add(Constant(2), Constant(2)), Constant(4))

        for i in test_combiner.iterateValues():
            assert i == test_value
    
    def test_multiple_subtraction(self):
        test_value = 2 - 2 - 4
        test_combiner = Sub(Sub(Constant(2), Constant(2)), Constant(4))

        for i in test_combiner.iterateValues():
            assert i == test_value
    
    def test_multiple_multiplication(self):
        test_value = 2 * 2 * 4
        test_combiner = Mul(Mul(Constant(2), Constant(2)), Constant(4))

        for i in test_combiner.iterateValues():
            assert i == test_value
    
    def test_multiple_division(self):
        test_value = 2 / 2 / 4
        test_combiner = Div(Div(Constant(2), Constant(2)), Constant(4))

        for i in test_combiner.iterateValues():
            assert i == test_value
    
    def test_mixed_operators(self):
        test_values = [
            2 + 2 - 4,
            2 * 2 / 4,
            2 + 2 / 4,
            (2 + 2) / 4
        ]

        test_combiners = [
            Sub(Add(Constant(2), Constant(2)), Constant(4)),
            Div(Mul(Constant(2), Constant(2)), Constant(4)),
            Add(Div(Constant(2), Constant(4)), Constant(2)),
            Div(Add(Constant(2), Constant(2)), Constant(4))
        ]

        for value, combiner in zip(test_values, test_combiners):
            for i in combiner.iterateValues():
                assert value == i


class TestDice:

    def test_six_sided_die(self):
        test_range = [1, 2, 3, 4, 5, 6]
        test_dice = Dice(Constant(1), Constant(6))
        test_rolls = [i for i in test_dice.iterateValues()]

        for ans, roll in zip(test_range, test_rolls):
            assert ans == roll
    
    def test_multiple_six_sided_die(self):
        test_range = [i + j + k for i in range(1, 7) for j in range(1, 7) for k in range(1, 7)]
        test_dice = Dice(Constant(3), Constant(6))
        test_rolls = [i for i in test_dice.iterateValues()]

        for ans, roll in zip(test_range, test_rolls):
            assert ans == roll


class TestCombinedCombiners:

    def test_dice_with_addition(self):
        test_range = [3 + i + j + k for i in range(1, 7) for j in range(1, 7) for k in range(1, 7)]
        test_dice = Add(Constant(3), Dice(Constant(3), Constant(6)))
        test_rolls = [i for i in test_dice.iterateValues()]

        for ans, roll in zip(test_range, test_rolls):
            assert ans == roll
