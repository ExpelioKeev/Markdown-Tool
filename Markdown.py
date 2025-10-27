import sys
import re
import requests
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog, QMessageBox

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

        domain_ip_button = QPushButton('Add Highlights to Domains, IPs & Emails', self)
        domain_ip_button.clicked.connect(self.add_grave_to_domains_and_ips)
        button_layout.addWidget(domain_ip_button)

        block_button = QPushButton('Code Block', self)
        block_button.clicked.connect(self.add_grave_accents_to_block)
        button_layout.addWidget(block_button)

        link_button = QPushButton('HyperLink Text', self)
        link_button.clicked.connect(self.add_link)
        button_layout.addWidget(link_button)
        
        # NEW: Ollama formatting button
        ollama_button = QPushButton('Auto-Format with Ollama', self)
        ollama_button.clicked.connect(self.format_with_ollama)
        button_layout.addWidget(ollama_button)
        
        self.clear_button = QPushButton('Clear Formatting', self)
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
        text = self.text_edit.toPlainText()
        
        # Regular expression to find domains and IPs that are not already enclosed in grave accents
        domains_and_ips = re.findall(
            r'(?<!`)\b(?:'
            r'((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:[a-z]{2,6}|[a-z]{2}\.[a-z]{2}))'  # Domain
            r'|'
            r'((?:\d{1,3}\.){3}\d{1,3})'  # IP address
            r'|'
            r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'  # Email address
            r')\b(?!`)', 
            text, 
            re.IGNORECASE
        )

        # Loop over each found domain or IP and wrap with grave accents
        for match in domains_and_ips:
            if match[0]:  # This is a domain
                text = text.replace(match[0], f'`{match[0]}`')
            elif match[1]:  # This is an IP address
                text = text.replace(match[1], f'`{match[1]}`')
            elif match[2]:  # This is an email address
                text = text.replace(match[2], f'`{match[2]}`')
        
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
        # Remove grave accents (inline code)
        text = re.sub(r'`([^`]*)`', r'\1', text)
        # Remove grave accents (triple backticks) for code blocks
        text = re.sub(r'```([^`]*)```', r'\1', text, flags=re.DOTALL)
        # Remove asterisks (Bold)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        # Remove askterisks (italics)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        # Remove hyperlinks [text](url)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)       
        
        # Set the updated text back to the text edit
        self.text_edit.setPlainText(text)

    # NEW: Ollama formatting method
    def format_with_ollama(self):
        """Format text using Ollama with preconfigured prompt"""
        cursor = self.text_edit.textCursor()
        
        # Get text to format (selected or all)
        if cursor.hasSelection():
            text_to_format = cursor.selectedText()
            had_selection = True
        else:
            text_to_format = self.text_edit.toPlainText()
            had_selection = False
        
        # Check if there's text to format
        if not text_to_format.strip():
            QMessageBox.warning(self, "No Text", "There is no text to format.")
            return
        
        # Send to Ollama
        formatted_text = self.send_to_ollama(text_to_format)
        
        # Replace text with formatted result
        if formatted_text and formatted_text != text_to_format:
            if had_selection:
                cursor.insertText(formatted_text)
            else:
                self.text_edit.setPlainText(formatted_text)
    
    # NEW: Helper method to communicate with Ollama
    def send_to_ollama(self, text):
        """Send text to Ollama API and return formatted result"""
        try:
            # Prepare API request - model handles formatting based on its Modelfile
            request_data = {
                "model": "phi4",  # Change to your custom model name
                "prompt": text,
                "stream": False,
                "temperature": 0.1  # Low temperature for consistent formatting
            }
            
            # Send request to Ollama
            # Try localhost first, fallback to 127.0.0.1 if needed
            ollama_url = "http://127.0.0.1:11434/api/generate"
            
            response = requests.post(
                ollama_url,
                headers={"Content-Type": "application/json"},
                json=request_data,
                timeout=60  # 60 second timeout
            )
            
            # Check if request was successful
            if response.status_code == 200:
                response_json = response.json()
                formatted_text = response_json.get("response", "").strip()
                return formatted_text
            else:
                QMessageBox.critical(
                    self, 
                    "Ollama Error", 
                    f"Ollama returned error code {response.status_code}.\n\nMake sure Ollama is running and the model exists."
                )
                return text
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, 
                "Connection Error", 
                "Cannot connect to Ollama.\n\nMake sure Ollama is running:\n  ollama serve"
            )
            return text
            
        except requests.exceptions.Timeout:
            QMessageBox.critical(
                self, 
                "Timeout Error", 
                "Ollama took too long to respond.\n\nTry with shorter text or increase timeout."
            )
            return text
            
        except json.JSONDecodeError:
            QMessageBox.critical(
                self, 
                "Parse Error", 
                "Could not parse Ollama response.\n\nCheck Ollama logs for errors."
            )
            return text
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Unexpected Error", 
                f"An error occurred:\n\n{str(e)}"
            )
            return text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextFormattingTool()
    ex.show()
    sys.exit(app.exec_())