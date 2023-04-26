import sys
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

from dice_statistic_calculator.DiceStatCalculator import dice_calculator_wrapper, EmptyFormulaGivenError, InvalidInfixExpressionError


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        super().__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Dice Statistic Calculator")

        formula_label = QLabel("Roll Formula:")
        self.formula_input = QLineEdit()

        enter_button = QPushButton("Calculate")
        enter_button.clicked.connect(self.submit_roll_formula)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #FF0000")
        self.error_label.setHidden(True)

        self.stat_histogram = MplCanvas()

        layout = QVBoxLayout()
        layout.addWidget(formula_label)
        layout.addWidget(self.formula_input)
        layout.addWidget(enter_button)
        layout.addWidget(self.error_label)
        layout.addWidget(self.stat_histogram)

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)
    
    def submit_roll_formula(self):
        try:
            outcomes, quantity = dice_calculator_wrapper(self.formula_input.text())
        except EmptyFormulaGivenError:
            self.error_label.setText("Formula required!")
            self.error_label.setHidden(False)
            return
        except InvalidInfixExpressionError:
            self.error_label.setText("Formula misformatted!")
            self.error_label.setHidden(False)
            return
        
        self.error_label.setHidden(True)
        self.stat_histogram.axes.clear()
        self.stat_histogram.axes.set_xlabel("Roll Outcome")
        self.stat_histogram.axes.set_ylabel("Chance to Roll")
        self.stat_histogram.axes.bar(outcomes, quantity, label=outcomes)
        self.stat_histogram.draw()
        


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
