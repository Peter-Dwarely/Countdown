import sys
import requests
import threading
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer, QTime
from pystray import Icon, MenuItem, Menu
from PIL import Image

window_instance = None  # 全局变量
app_instance = None  # 保存 QApplication 实例

class TransparentWindow(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("color: red; font-size: 16px;")  # 调整字体大小
        self.update_countdown()
        self.adjustSize()
        # 获取屏幕大小并设置窗口位置
        screen_geometry = QApplication.desktop().availableGeometry()
        x = screen_geometry.width() - self.width() - 100  # 右上角，调整偏移量
        y = 10  # 距离顶部的偏移量
        self.move(x, y)
        self.show()

        # 设置定时器，每分钟更新一次
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(60000)  # 60,000 毫秒 = 1 分钟

    def update_countdown(self):
        now = QTime.currentTime()
        noon = QTime(12, 0)
        evening = QTime(18, 30)

        time_to_noon = now.secsTo(noon)
        time_to_evening = now.secsTo(evening)

        if time_to_noon < 0:
            time_to_noon += 24 * 3600  # 加一天的秒数

        if time_to_evening < 0:
            time_to_evening += 24 * 3600  # 加一天的秒数

        hours_noon, remainder_noon = divmod(time_to_noon, 3600)
        minutes_noon = remainder_noon // 60

        hours_evening, remainder_evening = divmod(time_to_evening, 3600)
        minutes_evening = remainder_evening // 60

        text = (f"Countdown to 12:00: {hours_noon}h {minutes_noon}m\n"
                f"Countdown to 18:30: {hours_evening}h {minutes_evening}m")
        print("Countdown info:", text)
        self.setText(text)
        self.adjustSize()

def create_window():
    global window_instance, app_instance
    app_instance = QApplication.instance()
    if app_instance is None:
        app_instance = QApplication(sys.argv)
    window_instance = TransparentWindow()
    app_instance.exec_()

def quit_action(icon, item):
    icon.stop()
    if window_instance:
        window_instance.close()  # 关闭透明窗口
    if app_instance:
        app_instance.quit()  # 退出应用程序事件循环
    sys.exit()

def create_tray_icon():
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    menu = Menu(MenuItem('Quit', quit_action))
    icon = Icon("countdown", image, menu=menu)
    icon.run()

def main():
    window_thread = threading.Thread(target=create_window, daemon=True)
    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    window_thread.start()
    tray_thread.start()
    window_thread.join()
    tray_thread.join()

if __name__ == "__main__":
    main()

