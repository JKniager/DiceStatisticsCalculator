from dice_statistic_calculator.DiceStatCalculator import BadFormulaFormatError, CombinerFactory
import pytest


class TestFactory:

    def test_no_space_split_single_digits(self):
        formula = "3d6"
        out = CombinerFactory.formula_split(formula)

        answer = ["3", "d", "6"]

        for o, a in zip(out, answer):
            assert o == a

    def test_no_space_split_multi_digits(self):
        formula = "32+56"
        out = CombinerFactory.formula_split(formula)

        answer = ["32", "+", "56"]

        for o, a in zip(out, answer):
            assert o == a
    
    def test_no_space_split_decimal_points(self):
        formula = "3.2 + 56"
        out = CombinerFactory.formula_split(formula)

        answer = ["3.2", "+", "56"]

        for o, a in zip(out, answer):
            assert o == a
    
    def test_bad_format(self):
        formula = "6..0"
        with pytest.raises(BadFormulaFormatError):
            out = CombinerFactory.formula_split(formula)
