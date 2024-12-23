from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer, QDateTime, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication, QFileDialog,
    QListWidgetItem, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDateEdit, QTimeEdit
)
from PyQt5 import QtCore
from pus import push_message

push_message('Дьяволок', 'мудень', 'icon/key.jpeg')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Таймер и напоминалка')
        self._closable = False
        
        # Удаление стандартных кнопок управления окном
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinimizeButtonHint & ~QtCore.Qt.WindowMaximizeButtonHint & ~QtCore.Qt.WindowCloseButtonHint)

        # Пример использования Qt.FramelessWindowHint для полной настройки окна
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)


        self.button = QPushButton(u'Закрыть', self)
        self.button.clicked.connect(self.on_click)

        self.text_time_minutes = QLabel("Введите через сколько должен сработать таймер")
        self.time_minute = QTimeEdit(self)
        self.minutes_button = QPushButton("Запустить таймер")  # Кнопка "Запустить таймер"
        self.minutes_button.clicked.connect(self.handle_minutes_button_click)


        self.text_time_hours = QLabel("Введите во сколько должен сработать таймер")
        self.time_hours = QTimeEdit(self)
        self.time_hours.setDateTime(QDateTime.currentDateTime())
        self.text = QLineEdit(self)
        self.text.setPlaceholderText("Введите напоминание")
        self.hours_button = QPushButton("Добавить напоминание")  # Кнопка "Добавить напоминание"
        self.hours_button.clicked.connect(self.handle_hours_button_click)


        layout = QVBoxLayout()
        hbox_minutes = QHBoxLayout()
        hbox_minutes.addWidget(self.text_time_minutes)
        hbox_minutes.addWidget(self.time_minute)
        hbox_minutes.addWidget(self.minutes_button)  # Добавляем кнопку в layout

        hbox_hours = QHBoxLayout()
        hbox_hours.addWidget(self.text_time_hours)
        hbox_hours.addWidget(self.time_hours)
        hbox_hours.addWidget(self.hours_button)  # Добавляем кнопку в layout

        vbox_hours = QVBoxLayout()
        vbox_hours.addLayout(hbox_hours)
        vbox_hours.addWidget(self.text)

        layout.addWidget(self.button)
        layout.addLayout(hbox_minutes)
        layout.addLayout(vbox_hours)

        self.setLayout(layout)

    # Код для отключения кнопки закрытия
    def closeEvent(self, evnt):
        if self._closable:
            super(MainWindow, self).closeEvent(evnt)
        else:
            evnt.ignore()

    @pyqtSlot()
    def on_click(self):
        self._closable = True
        self.close()
        
    
    def handle_minutes_button_click(self):
        # Логика для запуска таймера
        minutes = self.time_minute.time().toString("mm")
        print(minutes)  # Выводим значение в консоль для проверки
        # ... (Ваша реализация запуска таймера)

    def handle_hours_button_click(self):
        # Логика для добавления напоминания
        selected_time = self.time_hours.time().toString("hh:mm")
        print(f"Напоминание на {selected_time}") # Выводим значение в консоль
        # ... (Ваша реализация добавления напоминания)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    #window.resize(600, 400) # Это больше не нужно, так как мы используем full screen.
    window.show()
    window.showFullScreen()  # Переводим окно в полноэкранный режим
    sys.exit(app.exec_())