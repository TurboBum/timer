from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QApplication,
                             QSystemTrayIcon, QMenu, QAction)
from PyQt5.QtCore import Qt, QTimer, QTime, QRectF, QUrl, pyqtSlot
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import pus
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Обратный отчёт')
        self.initial_width = 300
        self.initial_height = 300
        self.setFixedSize(self.initial_width, self.initial_height)
        self.setMinimumSize(self.initial_width, self.initial_height)

        self.media_player = QMediaPlayer()
        url = QUrl.fromLocalFile("о.mp3")
        content = QMediaContent(url)
        self.media_player.setMedia(content)

        self.time_label = QLabel('00:00', self)
        self.text_label = QLabel("", self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        self.font = QFont()
        self.font.setPointSize(48)
        self.time_label.setFont(self.font)
        self.text_font = QFont()
        self.text_font.setPointSize(20)
        self.text_label.setFont(self.text_font)

        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = QTime(0, 0)
        self._total_seconds = 0
        self._start_angle = 90
        self._arc_length = 0
        self._circle_margin = 20
        self._ellipse_rect = QRectF(self._circle_margin, self._circle_margin, self.width() - 2 * self._circle_margin, self.height() - 2 * self._circle_margin)
        self.tray_icon = QSystemTrayIcon(QIcon("icon/c6d7e2ee38d97a222fc315cc3cf19652.jpg"), self)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
        tray_menu = QMenu(self)
        quit_action = QAction("Выйти", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.show()

    def start_countdown(self, minutes, seconds, text=""):
        total_seconds = minutes * 60 + seconds
        self.remaining_time = QTime(0, total_seconds // 60, total_seconds % 60)
        self._total_seconds = total_seconds
        self._arc_length = 0
        self.update_time_label()
        self.timer.start(1000)
        self.set_scaled_text(text)

    def update_timer(self):
        if self.remaining_time > QTime(0, 0):
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.update_time_label()
            self._arc_length = float((self._total_seconds - (
                        self.remaining_time.minute() * 60 + self.remaining_time.second())) * 360 / self._total_seconds)
        else:
            self.timer.stop()
            self.font.setPointSize(20)
            self.time_label.setFont(self.font)
            self.time_label.setText("Время вышло!")
            if pus:
                pus.push_message("Таймер", "Остановка таймера", "Время выщло")
            print("Время вышло!")
            self.media_player.play()
            self._arc_length = 360.0

        self.update()

    def update_time_label(self):
        self.time_label.setText(self.remaining_time.toString("mm:ss"))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen()
        pen.setWidth(8)
        pen.setColor(QColor(100, 100, 100))
        painter.setPen(pen)
        painter.drawEllipse(self._ellipse_rect)

        pen.setColor(QColor(0, 120, 212))
        painter.setPen(pen)

        painter.drawArc(self._ellipse_rect, self._start_angle * 16, -int(self._arc_length * 16))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Пересчитываем геометрию меток
        self.time_label.setGeometry(0, 0, self.width(), self.height())
        self.text_label.setGeometry(0, 0, self.width(), self.height())
        # self._ellipse_rect = self.calculate_ellipse_rect()
        self._ellipse_rect = QRectF(self._circle_margin, self._circle_margin, self.width() - 2 * self._circle_margin, self.height() - 2 * self._circle_margin)


    @pyqtSlot(str)
    def set_text_time(self, text):
        self.time_label.setText(text)

    def set_scaled_text(self, text):
        """Масштабирует текст и подстраивает размер окна и эллипса."""
        formatted_text = self.format_text(text)
        self.text_label.setText(formatted_text)

        self._ellipse_rect = self.calculate_ellipse_rect()
        self.adjust_window_size()

        self.update()

    def format_text(self, text):
        """Форматирует текст для переноса слов, не обрывая их.
        Ограничение 15 символов на строку."""
        words = text.split()
        lines = []
        current_line = ""
        max_line_length = 15

        for word in words:
            if not current_line:
                current_line = word
            elif len(current_line) + len(word) + 1 <= max_line_length:
                current_line += " " + word
            else:
                if len(word) > max_line_length:
                    while len(word) > max_line_length:
                         lines.append(word[:max_line_length])
                         word = word[max_line_length:]
                    current_line = word
                else:
                    lines.append(current_line)
                    current_line = word
        
        lines.append(current_line)
        return "\n".join(lines)

    def get_text_rect(self, text, font_size):
        """Получает прямоугольник, который занимает текст с заданной высотой."""
        font = QFont(self.text_font)
        font.setPointSize(font_size)
        font_metrics = self.text_label.fontMetrics()
        rect = font_metrics.boundingRect(text)
        return rect

    def calculate_ellipse_rect(self):
        """Вычисляет размеры эллипса на основе текущих размеров окна."""
        ellipse_x = self._circle_margin
        ellipse_y = self._circle_margin
        ellipse_width = self.width() - 2 * self._circle_margin
        ellipse_height = self.height() - 2 * self._circle_margin
        return QRectF(ellipse_x, ellipse_y, ellipse_width, ellipse_height)

    def adjust_window_size(self):
        """Подстраивает размер окна под количество строк текста."""
        num_lines = self.text_label.text().count('\n') + 1
        new_width = self.initial_width + (num_lines - 1) * 50
        new_height = self.initial_height + (num_lines - 1) * 50
        self.setFixedSize(max(self.initial_width, new_width), max(self.initial_height, new_height))
        # Принудительно пересчитываем геометрию
        self.time_label.setGeometry(0, 0, self.width(), self.height())
        self.text_label.setGeometry(0, 0, self.width(), self.height())

    def on_tray_icon_activated(self, reason):
      if reason == QSystemTrayIcon.ActivationReason.Trigger:
        self.show()
        self.activateWindow()

    def closeEvent(self, event):
        """Обработчик события закрытия окна."""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Приложение запущено в фоновом режиме",
                                    "Приложение свернуто в системный трей.",
                                    QSystemTrayIcon.Information)


def start(min, sec, text):
    window = Window()
    window.show()
    window.start_countdown(min, sec, text)
    return window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # Запуск обратного отсчета на 1 минуту 30 секунд
    window.start_countdown(0, 10, "Помыть посуду и сделать уроки гварп вашщароп варшщав хшах ахшщп авшоав хш поавпшх пщова")

    sys.exit(app.exec_())