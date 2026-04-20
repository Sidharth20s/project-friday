import sys
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon
import pystray
from PIL import Image

class FridayGUI(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.setWindowTitle("FRIDAY — AI Assistant")
        self.setWindowIcon(QIcon("icon.png")) # We'll need a dummy icon
        self.resize(1000, 700)
        
        # Transparent/Frameless Window (optional, looks cool)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def closeEvent(self, event):
        # Instead of closing, just hide to tray
        event.ignore()
        self.hide()

def setup_tray(window):
    def on_quit(icon, item):
        icon.stop()
        QApplication.quit()
        sys.exit()

    def on_show(icon, item):
        window.show()
        window.activateWindow()

    # Create a simple colored icon for now
    image = Image.new('RGB', (64, 64), color=(0, 212, 255))
    icon = pystray.Icon("Friday", image, "FRIDAY AI", menu=pystray.Menu(
        pystray.MenuItem("Show FRIDAY", on_show),
        pystray.MenuItem("Quit", on_quit)
    ))
    
    icon.run()

def launch_gui(url):
    app = QApplication(sys.argv)
    window = FridayGUI(url)
    window.show()
    
    # Start tray in a separate thread
    tray_thread = threading.Thread(target=setup_tray, args=(window,), daemon=True)
    tray_thread.start()
    
    sys.exit(app.exec())
