import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QTime, pyqtSlot, QRect, QPoint, QRectF, QUrl
from PyQt5.QtGui import QPainter, QPen, QFont, QColor, QFontMetrics
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Обратный отчёт')
        self.setFixedSize(300, 300)

        # создание музыкального проигрывателя
        self.media_player = QMediaPlayer()
        url = QUrl.fromLocalFile("music/03b3a427eeb52e37b162584ef1f2fb25.mp3")
        content = QMediaContent(url)
        self.media_player.setMedia(content)

        self.time_label = QLabel('00:00', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(48)
        self.time_label.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = QTime(0, 0)  # Инициализация времени до отсчета
        self._total_seconds = 0  # общее количество секунд
        self._start_angle = 90  # начало кругового индикатора
        self._arc_length = 0  # длина кругового индикатора

    def start_countdown(self, minutes, seconds):
        """
        Запускает обратный отсчет с указанным временем.
        """
        total_seconds = minutes * 60 + seconds
        self.remaining_time = QTime(0, total_seconds // 60, total_seconds % 60)
        self._total_seconds = total_seconds
        self._arc_length = 0
        self.update_time_label()
        self.timer.start(1000)  # Обновлять таймер каждую секунду

    def update_timer(self):

        if self.remaining_time > QTime(0, 0):
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.update_time_label()
            self._arc_length = float((self._total_seconds - (
                        self.remaining_time.minute() * 60 + self.remaining_time.second())) * 360 / self._total_seconds)
        else:
            self.timer.stop()
            self.time_label.setText("Время вышло!")
            self.media_player.play()
            self._arc_length = 360.0

        self.update()  # перерисовываем круговой индикатор

    def update_time_label(self):
        """
        Обновляет текст на time_label.
        """
        self.time_label.setText(self.remaining_time.toString("mm:ss"))

    def paintEvent(self, event):
        """
        Отрисовка кругового индикатора
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Сглаживание
        pen = QPen()
        pen.setWidth(8)  # Толщина круга
        pen.setColor(QColor(100, 100, 100))  # Цвет круга
        painter.setPen(pen)
        rect = QRectF(20, 20, self.width() - 40, self.height() - 40)  # Изменен QRect на QRectF
        painter.drawEllipse(rect)

        pen.setColor(QColor(0, 120, 212))  # Цвет индикатора
        painter.setPen(pen)

        painter.drawArc(rect, self._start_angle * 16, -int(self._arc_length * 16))

    def resizeEvent(self, event):
        """
        Выравнивает по центру при изменении размера
        """
        super().resizeEvent(event)
        self.time_label.setGeometry(0, 0, self.width(), self.height())

    @pyqtSlot(str)
    def set_text_time(self, text):
        self.time_label.setText(text)


# Функция запуска таймера
def start(min, sec):
    window = Window()
    window.show()
    window.start_countdown(min, sec)
    return window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = start(1, 30)
    sys.exit(app.exec_())