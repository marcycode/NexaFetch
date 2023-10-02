import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QTextBrowser, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from metaphor_python import Metaphor
from plyer import notification
from scheduler import Scheduler

def get_api_key_from_file(filename):
    """Read API key from the given file."""
    with open(filename, 'r') as f:
        return f.read().strip()

class ContentAggregator(QMainWindow):
    def __init__(self, api_key):
        super().__init__()
        self.api = Metaphor(api_key=api_key)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout()

       
        welcome_label = QLabel("Welcome to NexaFetch!", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        font = welcome_label.font()
        font.setPointSize(18)
        welcome_label.setFont(font)
        layout.addWidget(welcome_label)

       
        instruction_label = QLabel("Enter a topic and set a schedule to fetch curated content.", self)
        instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_label)

        self.topic_input = QLineEdit(self)
        self.topic_input.setPlaceholderText("Enter topic of interest...")
        layout.addWidget(self.topic_input)

        self.search_button = QPushButton('Search Now', self)
        self.search_button.clicked.connect(self.fetch_and_notify)
        layout.addWidget(self.search_button)

        self.results_list = QListWidget(self)
        self.results_list.itemClicked.connect(self.open_link_in_browser)  
        layout.addWidget(self.results_list)

        self.content_display = QTextBrowser(self)
        layout.addWidget(self.content_display)

        self.scheduler = Scheduler(self.fetch_and_notify)
        layout.addWidget(self.scheduler)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('NexaFetch')
        
        
        self.setWindowIcon(QIcon('nexafetch_icon.ico'))
        
        self.resize(600, 500)

    def fetch_and_notify(self):
        query = self.topic_input.text()
        if not query:
            return

        try:
            response = self.api.search(query=query, num_results=10)
            self.results_list.clear()
            for result in response.results:
                self.results_list.addItem(f"{result.title} ({result.url})")
            notification.notify(
                title='NexaFetch Update',
                message=f'Found {len(response.results)} new articles for "{query}"!',
                app_name='NexaFetch',
                timeout=5,
               
                app_icon='nexafetch_icon.ico'
            )
        except Exception as e:
            print(f"An error occurred: {e}")

    def open_link_in_browser(self, item):  
        url = item.text().split("(")[-1].rstrip(")")
        webbrowser.open(url)

if __name__ == '__main__':
    api_key = get_api_key_from_file("API_KEY.txt")
    app = QApplication(sys.argv)
    window = ContentAggregator(api_key)
    window.show()
    sys.exit(app.exec_())
