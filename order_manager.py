from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMainWindow, QMessageBox, QListWidget, QApplication, QAbstractItemView


class Order(QWidget):
    def __init__(self):
        super(Order, self).__init__()
        self.order_list = QListWidget()
        self.required_bosses = ['asylum', 'gargoyle',
                                'spider', 'iron_golem', 'o_s',
                                'ceaseless', 'sif', 'kings',
                                'chaosbed', 'seath', 'pinwheel',
                                'nito', 'gwyn']

        self.order_list.setDragDropMode(QAbstractItemView.InternalMove)
        for i in self.required_bosses:
            self.order_list.addItem(i)

        self.layout = QGridLayout()
        self.layout.addWidget(self.order_list, 0, 0)
        self.setLayout(self.layout)


class OrderGui(QMainWindow):
    def __init__(self):
        super(OrderGui, self).__init__()
        self.order = Order()
        self.setCentralWidget(self.order)