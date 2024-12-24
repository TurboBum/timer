import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime, QTimer, pyqtSlot, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTimeEdit
)
from PyQt5.QtGui import QPixmap, QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Таймер и напоминалка')
        self._closable = False

        # Удаление стандартных кнопок управления окном
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint & 
                            ~Qt.WindowMaximizeButtonHint & ~Qt.WindowCloseButtonHint)
        
        # Установка фонового изображения
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)  # Масштабируем содержимое
        self.set_background_image()

        # Элементы управления
        self.button = QPushButton(u'Закрыть', self)
        self.button.clicked.connect(self.on_click)

        self.text_time_minutes = QLabel("Введите через сколько должен сработать таймер")
        self.time_minute = QTimeEdit(self)
        self.time_minute.setDisplayFormat("mm:ss")  # Устанавливаем формат на минуты и секунды
        self.time_minute.setTime(self.time_minute.time().fromString("00:00", "mm:ss"))  # Устанавливаем начальное время
        self.minutes_button = QPushButton("Запустить таймер")  # Кнопка "Запустить таймер"
        self.minutes_button.clicked.connect(self.handle_minutes_button_click)

        self.text_time_hours = QLabel("Введите во сколько должен сработать таймер")
        self.time_hours = QTimeEdit(self)
        self.time_hours.setDateTime(QDateTime.currentDateTime())
        self.text = QLineEdit(self)
        self.text.setPlaceholderText("Введите напоминание")
        self.hours_button = QPushButton("Добавить напоминание")  # Кнопка "Добавить напоминание"
        self.hours_button.clicked.connect(self.handle_hours_button_click)

        # Установка layout
        layout = QVBoxLayout()
        hbox_minutes = QHBoxLayout()
        hbox_minutes.addWidget(self.text_time_minutes)
        hbox_minutes.addWidget(self.time_minute)
        hbox_minutes.addWidget(self.minutes_button)

        hbox_hours = QHBoxLayout()
        hbox_hours.addWidget(self.text_time_hours)
        hbox_hours.addWidget(self.time_hours)
        hbox_hours.addWidget(self.hours_button)

        vbox_hours = QVBoxLayout()
        vbox_hours.addLayout(hbox_hours)
        vbox_hours.addWidget(self.text)

        layout.addWidget(self.button)
        layout.addLayout(hbox_minutes)
        layout.addLayout(vbox_hours)

        # Установка layout для главного виджета
        self.setLayout(layout)

    def set_background_image(self):
        """Устанавливает изображение фона."""
        background_pixmap = QPixmap("icon/c6d7e2ee38d97a222fc315cc3cf19652.jpg")  # Указать путь к изображению
        self.background_label.setPixmap(background_pixmap)
        self.background_label.setGeometry(self.rect())

    def resizeEvent(self, event):
        """Обновляем размер QLabel при изменении размера окна."""
        self.background_label.setGeometry(self.rect())
        super().resizeEvent(event)

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
        minutes = self.time_minute.time().toString("mm:ss")
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
    window.resize(600, 400)
    
    window.setWindowIcon(QIcon("icon/key.jpeg"))# Устанавливаем иконку окна
    window.show()
    # window.showFullScreen()  # Переводим окно в полноэкранный режим
    sys.exit(app.exec_())