from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer,QDateTime, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication, QFileDialog,
    QListWidgetItem, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDateEdit, QTimeEdit
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Таймер и напоминалка')
        self._closable = False

        self.button = QPushButton(u'Закрыть', self)
        self.button.clicked.connect(self.on_click)

        self.text_time_minutes = QLabel("Введите через сколько должен сработать таймер")
        self.time_minute = QTimeEdit(self)
        self.minutes_button = QPushButton("Запустить таймер")
        
        self.text_time_hours = QLabel("Введите во сколько должен сработать таймер")
        self.time_hours = QTimeEdit(self)
        self.time_hours.setDateTime(QDateTime.currentDateTime())
        self.text = QLineEdit(self)
        self.text.setPlaceholderText("Введите напоминание")
        self.hours_button = QPushButton("Добавить напоминание")


        layout = QVBoxLayout()
        hbox_minutes = QHBoxLayout()
        hbox_minutes.addWidget(self.text_time_minutes)
        hbox_minutes.addWidget(self.time_minute)
        Vbox_hours = QVBoxLayout()
        hbox_hours = QHBoxLayout()
        hbox_hours.addWidget(self.text_time_hours)
        hbox_hours.addWidget(self.time_hours)
        
        Vbox_hours.addLayout(hbox_hours)
        layout.addWidget(self.button)
        Vbox_hours.addWidget(self.text)
        layout.addLayout(hbox_minutes)
        layout.addLayout(Vbox_hours)
        layout.addLayout
        self.setLayout(layout)

    #Код для отключения кнопки закрытия
    def closeEvent(self, evnt):
        if self._closable:
            super(MainWindow, self).closeEvent(evnt)
        else:
            evnt.ignore()
    ################################################################

    @pyqtSlot()
    def on_click(self):
        self._closable = True
        self.close()

        


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())