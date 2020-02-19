from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMainWindow, QMessageBox, QListWidget, QApplication, QAbstractItemView, QCheckBox, QVBoxLayout
import threading


class Order(QWidget):
    def __init__(self):
        super(Order, self).__init__()
        self.game_on = False
        self.required_bosses = ['Asylum Demon', 'Bell Gargoyle',
                                'Quelaag', 'Iron Golem', 'ornstein & smough',
                                'Ceaseless Discharge', 'Sif', '4 Kings',
                                'Bed Of Chaos', 'Seath', 'Pinwheel',
                                'Nito', 'Gwyn']
        self.order_list = QListWidget()
        self.order_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.capra_box = QCheckBox("Capra Demon")
        self.capra_box.toggled.connect(lambda: self.add_to_list(self.capra_box))
        self.centipede_box = QCheckBox("Centipede Demon")
        self.centipede_box.toggled.connect(lambda: self.add_to_list(self.centipede_box))
        self.priscilla_box = QCheckBox("Priscilla")
        self.priscilla_box.toggled.connect(lambda: self.add_to_list(self.priscilla_box))
        self.gwyndolin_box = QCheckBox("Gwyndolin")
        self.gwyndolin_box.toggled.connect(lambda: self.add_to_list(self.gwyndolin_box))
        self.firesage_box = QCheckBox("Demon Firesage")
        self.firesage_box.toggled.connect(lambda: self.add_to_list(self.firesage_box))
        self.gaping_box = QCheckBox("Gaping Dragon")
        self.gaping_box.toggled.connect(lambda: self.add_to_list(self.gaping_box))
        self.butterfly_box = QCheckBox("Moonlight Butterfly")
        self.butterfly_box.toggled.connect(lambda: self.add_to_list(self.butterfly_box))

        self.start_button = QPushButton("Start New Game")
        self.start_button.clicked.connect(self.start_game)
        self.selected_bosses = []
        for i in self.required_bosses:
            self.order_list.addItem(i)
            self.selected_bosses.append(i)
        self.layout = QGridLayout()
        self.layout.addWidget(self.capra_box, 0, 0)
        self.layout.addWidget(self.centipede_box, 0, 1)
        self.layout.addWidget(self.priscilla_box, 1, 0)
        self.layout.addWidget(self.gwyndolin_box, 1, 1)
        self.layout.addWidget(self.firesage_box, 2, 0)
        self.layout.addWidget(self.gaping_box, 2, 1)
        self.layout.addWidget(self.butterfly_box, 3, 0)
        self.layout.addWidget(self.order_list, 4, 0, 1, 2)
        self.setLayout(self.layout)

    def start_game(self):
        self.game_on = True

    def add_to_list(self, item):
        if item.checkState():
            self.order_list.addItem(item.text())
            self.selected_bosses.append(item.text())
        else:
            self.order_list.clear()
            del self.selected_bosses[self.selected_bosses.index(item.text())]
            for i in self.selected_bosses:
                self.order_list.addItem(i)


class OrderGui(QMainWindow):
    def __init__(self):
        super(OrderGui, self).__init__()
        self.setWindowTitle("Boss Order")
        self.setGeometry(600, 500, 300, 455)
        self.order = Order()
        self.setCentralWidget(self.order)


if __name__ == '__main__':
    app = QApplication()
    gui = OrderGui()
    gui.show()
    app.exec_()