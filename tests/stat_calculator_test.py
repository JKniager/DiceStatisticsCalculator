from dice_statistic_calculator.DiceStatCalculator import Constant, Dice, StatCalculator
import pytest
from . import utils

class TestStats:

    def test_constant(self):
        test_constant = Constant(2)
        true_ave = 2.0
        true_std = 0.0
        true_prob = (2.0, 1.0)

        calc = StatCalculator(test_constant)
        calc.calcStats()
        assert utils.check_within_error(true_ave, calc.average, 0.01)
        assert utils.check_within_error(true_std, calc.std_dev, 0.01)
        for i in calc.iterateStats():
            assert true_prob[0] == i[0] and utils.check_within_error(true_prob[1], i[1], 0.01)
    
    def test_six_sided_die(self):
        test_dice = Dice(Constant(1), Constant(6))
        true_ave = 3.5
        true_std = 1.71
        true_prob = [(x, 1.0 / 6.0) for x in range(1, 7)]

        calc = StatCalculator(test_dice)
        calc.calcStats()
        assert utils.check_within_error(true_ave, calc.average, 0.01)
        assert utils.check_within_error(true_std, calc.std_dev, 0.01)

        cur_prob = 0

        for i in calc.iterateStats():
            assert true_prob[cur_prob][0] == i[0] and utils.check_within_error(true_prob[cur_prob][1], i[1], 0.01)
            cur_prob += 1
    
    def test_multiple_six_sided_die(self):
        test_dice = Dice(Constant(3), Constant(6))
        true_ave = 10.5
        true_std = 2.96
        true_prob = [
            (3, 0.0046),
            (4, 0.0139),
            (5, 0.0278),
            (6, 0.0463),
            (7, 0.0694),
            (8, 0.0972),
            (9, 0.1157),
            (10, 0.1250),
            (11, 0.1250),
            (12, 0.1157),
            (13, 0.0972),
            (14, 0.0694),
            (15, 0.0463),
            (16, 0.0278),
            (17, 0.0139),
            (18, 0.0046)
        ]

        calc = StatCalculator(test_dice)
        calc.calcStats()
        assert utils.check_within_error(true_ave, calc.average, 0.01)
        assert utils.check_within_error(true_std, calc.std_dev, 0.01)

        cur_prob = 0

        for i in calc.iterateStats():
            assert true_prob[cur_prob][0] == i[0] and utils.check_within_error(true_prob[cur_prob][1], i[1], 0.0001)
            cur_prob += 1
