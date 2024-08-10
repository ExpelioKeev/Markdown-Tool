import sys
import re
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog

chrome_script = 'tell application "Google Chrome" to set gmyText to execute front window\'s active tab javascript "window.getSelection().toString()"'

result = subprocess.run(['osascript', '-e', chrome_script], capture_output=True, text=True)

output = ''

if result.returncode == 0:
    output = result.stdout.strip()
    print(output)
else:
    error = result.stderr.strip()
    print(f"An error occurred: {error}")

class TextFormattingTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Text Formatting Tool')

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText('')

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Buttons
        button_layout = QHBoxLayout()

        grave_button = QPushButton('Add Highlights', self)
        grave_button.clicked.connect(self.add_grave_accents)
        button_layout.addWidget(grave_button)

        asterisk_button = QPushButton('Bold', self)
        asterisk_button.clicked.connect(self.add_asterisks)
        button_layout.addWidget(asterisk_button)

        italics_button = QPushButton('Italicize', self)
        italics_button.clicked.connect(self.make_italics)
        button_layout.addWidget(italics_button)

        domain_ip_button = QPushButton('Add Highlights to Domains and IPs', self)
        domain_ip_button.clicked.connect(self.add_grave_to_domains_and_ips)
        button_layout.addWidget(domain_ip_button)

        block_button = QPushButton('Code Block', self)
        block_button.clicked.connect(self.add_grave_accents_to_block)
        button_layout.addWidget(block_button)

        link_button = QPushButton('HyperLink Text', self)
        link_button.clicked.connect(self.add_link)
        button_layout.addWidget(link_button)
        
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.clicked.connect(self.clear_formatting)
        button_layout.addWidget(self.clear_button)


        main_layout.addLayout(button_layout)

        # Text Input
        main_layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def add_grave_accents(self):
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            replacement_text = f'`{selected_text}`'
            self.text_edit.insertPlainText(replacement_text)

    def add_asterisks(self):
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            replacement_text = f'**{selected_text}**'
            self.text_edit.insertPlainText(replacement_text)

    def make_italics(self):
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            replacement_text = f'*{selected_text}*'
            self.text_edit.insertPlainText(replacement_text)

    def add_grave_to_domains_and_ips(self):
    # Obtain the text from the text_edit widget
        text = self.text_edit.toPlainText()
    
    # Regular expression to find domains and IPs that are not already enclosed in grave accents
    def add_grave_to_domains_and_ips(self):
        text = self.text_edit.toPlainText()
        
        # Regular expression to find domains and IPs that are not already enclosed in grave accents
        domains_and_ips = re.findall(
            r'(?<!`)\b(?:'
            r'((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:[a-z]{2,6}|[a-z]{2}\.[a-z]{2}))'
            r'|'
            r'((?:\d{1,3}\.){3}\d{1,3}))\b(?!`)', 
            text, 
            re.IGNORECASE
        )

        # Loop over each found domain or IP and wrap with grave accents
        for match in domains_and_ips:
            if match[0]:  # This is a domain
                text = text.replace(match[0], f'`{match[0]}`')
            elif match[1]:  # This is an IP address
                text = text.replace(match[1], f'`{match[1]}`')
        
        # Update the text in the text edit field
        self.text_edit.setPlainText(text)

        
    def add_grave_accents_to_block(self):
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            replacement_text = f'```\n{selected_text}\n```'
            self.text_edit.insertPlainText(replacement_text)
        else:
            text = self.text_edit.toPlainText()
            replacement_text = f'```\n{text}\n```'
            self.text_edit.setPlainText(replacement_text)

    def add_link(self):
        selected_text = self.text_edit.textCursor().selectedText()
        if selected_text:
            hyperlink, ok = QInputDialog.getText(self, 'Enter Hyperlink', 'Enter hyperlink:')
            if ok:
                replacement_text = f'[{selected_text}]({hyperlink})'
                self.text_edit.insertPlainText(replacement_text)
            else:
                self.text_edit.insertPlainText(selected_text)
    
    def clear_formatting(self):
        cursor = self.text_edit.textCursor()
        cursor.removeSelectedText()  # Remove selected text
        text = self.text_edit.toPlainText()
        
        # Remove grave accents
        text = re.sub(r'```(.*?)```', r'\1', text, flags=re.DOTALL)
        # Remove grave accents (triple backticks) for code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Remove asterisks (Bold)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        # Remove askterisks (italics)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        # Remove hyperlinks [text](url)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        
        # Set the updated text back to the text edit
        self.text_edit.setPlainText(text) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextFormattingTool()
    ex.show()
    sys.exit(app.exec_())
