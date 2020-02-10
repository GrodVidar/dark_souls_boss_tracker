from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMainWindow, QMessageBox, QListWidget, QApplication
import re
import boss_tracker


class ErrorWindow(QMessageBox):
    def __init__(self, message):
        super(ErrorWindow, self).__init__()
        self.error_win = QMessageBox()
        self.error_win.setWindowTitle("Message")
        self.error_win.setText(message)
        self.error_win.exec_()


class Widgets(QWidget):
    def __init__(self):
        super(Widgets, self).__init__()
        self.setWindowTitle("Dark Souls Boss Tracker")
        self.setGeometry(800, 400, 250, 200)
        self.new_run_field = QLineEdit(self)
        self.new_run_button = QPushButton("Start New Run", self)
        self.new_run_button.clicked.connect(self.new_run)
        self.previous_label = QLabel("Previous runs:")
        self.previous_runs = QListWidget(self)
        self.previous_runs.itemClicked.connect(self.select_run)
        self.selected = None
        self.resume_button = QPushButton("Resume Run", self)
        self.resume_button.clicked.connect(self.resume)
        self.delete_button = QPushButton("Delete Run", self)
        self.delete_button.clicked.connect(self.delete_run)

        self.layout = QGridLayout()
        self.layout.addWidget(self.new_run_field, 0, 0)
        self.layout.addWidget(self.new_run_button, 0, 1)
        self.layout.addWidget(self.previous_label, 1, 0)
        self.layout.addWidget(self.previous_runs, 2, 0)
        self.layout.addWidget(self.resume_button, 3, 0)
        self.layout.addWidget(self.delete_button, 3, 1)
        self.get_tables()

        self.setLayout(self.layout)

    def get_tables(self):
        self.previous_runs.clear()
        my_list = boss_tracker.get_tables()
        for i in my_list:
            self.previous_runs.addItem(i[0])
        # print(my_list)

    def select_run(self, item):
        self.selected = item.text()

    def new_run(self):
        new_run_pattern = re.compile(r"[^a-zA-Z0-9_-]")
        error = new_run_pattern.search(self.new_run_field.text())
        for i in range(self.previous_runs.count()):
            if self.new_run_field.text() == self.previous_runs.item(i).text():
                error = True
        if not error and len(self.new_run_field.text()) > 3:
            boss_tracker.start_new_run(self.new_run_field.text())
            self.previous_runs.addItem(self.new_run_field.text())
        ErrorWindow("Username too short has special characters or already in use.")

    def resume(self):
        if self.selected is not None:
            boss_tracker.resume_run(self.selected)

    def delete_run(self):
        print(self.selected)
        if self.selected is not None:
            boss_tracker.delete_table(self.selected)
            self.get_tables()


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()

        self.widget = Widgets()
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Widgets()
    gui.show()
    app.exec_()