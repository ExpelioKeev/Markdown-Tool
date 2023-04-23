#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Markdown Helper
# @raycast.mode silent

# Optional parameters:
# @raycast.icon https://expel.com/favicon.ico

# Documentation:
# @raycast.author Akeva
# @raycast.description we dont know yet :o

import tkinter as tk
import tkinter.simpledialog
import re 
import subprocess

#Use subprocess and osascript to natively import the highlighted text into the textbox.
#There are libraries that do this but I didn't want to import random libs -TC 4/23/2023
chrome_script = 'tell application "Google Chrome" to set gmyText to execute front window\'s active tab javascript "window.getSelection().toString()"'
result = subprocess.run(['osascript', '-e', chrome_script], capture_output=True, text=True)
if result.returncode == 0:
    output = result.stdout.strip()
    print(output)
else:
    error = result.stderr.strip()
    print(f"An error occurred: {error}")

#Button Functions
def add_grave_accents():
    text = input_text.get('1.0', 'end-1c')
    selected_text = input_text.selection_get()
    start_index = input_text.search(selected_text, '1.0', 'end')
    end_index = f"{start_index}+{len(selected_text)}c"
    input_text.delete(start_index, end_index)
    input_text.insert(start_index, f'`{selected_text}`')
def add_asterisks():
    text = input_text.get('1.0', 'end-1c')
    selected_text = input_text.selection_get()
    start_index = input_text.search(selected_text, '1.0', 'end')
    end_index = f"{start_index}+{len(selected_text)}c"
    input_text.delete(start_index, end_index)
    input_text.insert(start_index, f'**{selected_text}**')
def make_italics():
    text = input_text.get('1.0', 'end-1c')
    selected_text = input_text.selection_get()
    start_index = input_text.search(selected_text, '1.0', 'end')
    end_index = f"{start_index}+{len(selected_text)}c"
    input_text.delete(start_index, end_index)
    input_text.insert(start_index, f'*{selected_text}*')
def add_grave_to_domains_and_ips():
    text = input_text.get('1.0', 'end-1c')
    domains_and_ips = re.findall(r'(?i)\b((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:[a-z]{2,6}|[a-z]{2}\.[a-z]{2}))\b|\b((?:\d{1,3}\.){3}\d{1,3})\b', text)
    for match in domains_and_ips:
        if match[0]:
            start_index = input_text.search(match[0], '1.0', 'end')
            end_index = f"{start_index}+{len(match[0])}c"
            input_text.delete(start_index, end_index)
            input_text.insert(start_index, f'`{match[0]}`')
        elif match[1]:
            start_index = input_text.search(match[1], '1.0', 'end')
            end_index = f"{start_index}+{len(match[1])}c"
            input_text.delete(start_index, end_index)
            input_text.insert(start_index, f'`{match[1]}`')    
def add_grave_accents_to_block():
    if input_text.tag_ranges("sel"):
        start_index = input_text.index("sel.first")
        end_index = input_text.index("sel.last")
        selected_text = input_text.get(start_index, end_index)
        input_text.delete(start_index, end_index)
        grave_text = f'``` \n {selected_text} \n````'
        input_text.insert(start_index, grave_text)
    else:
        text = input_text.get('1.0', 'end-1c')
        grave_text = f'``` \n {text} \n```'
        input_text.delete('1.0', 'end')
        input_text.insert('1.0', grave_text)
def add_link():
    selected_text = input_text.selection_get()
    start_index = input_text.search(selected_text, '1.0', 'end')
    end_index = f"{start_index}+{len(selected_text)}c"
    input_text.delete(start_index, end_index)
    hyperlink = tk.simpledialog.askstring(title='Enter Hyperlink', prompt='Enter hyperlink:')
    if hyperlink:
        input_text.insert(start_index, f'[{selected_text}]({hyperlink})')
    else:
        input_text.insert(start_index, f'{selected_text}')
#Get content into the clipboard -tc
def copy():
    text = input_text.get('1.0', 'end-1c')
    inp = text.encode('utf8')
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(inp)
    p.stdin.close()
#Get content into clipboard, then close the editor -tc
def copyandclose():
    text = input_text.get('1.0', 'end-1c')
    inp = text.encode('utf8')
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(inp)
    p.stdin.close()
    root.destroy()

#Tk
root = tk.Tk()
root.geometry("955x520")
root.title('Text Formatting Tool')

#Theme shenanigans
root.config(bg="White")
light = tk.PhotoImage(file="../resources/light.png")
dark = tk.PhotoImage(file="../resources/dark.png")
switch_value = True
def toggle():
    global switch_value
    if switch_value == True:
        switch.config(image=dark, bg="#26242f",
                      activebackground="#26242f")
        # Changes the window to dark theme
        root.config(bg="#26242f")  
        switch_value = False
    else:
        switch.config(image=light, bg="white", 
                      activebackground="white")  
        # Changes the window to light theme
        root.config(bg="white")  
        switch_value = True
# Creating a button to toggle
# between light and dark themes
switch = tk.Button(root, image=light, 
                bd=0, bg="white",
                activebackground="white", 
                command=toggle)

#Labels
input_label = tk.Label(root, text='Text Editor', font='Helvetica 24 bold')
flabel = tk.Label(root, text='Formatting Options', font='Helvetica 18 bold')
clabel = tk.Label(root, text='Copy Options', font='Helvetica 18 bold')

#Textbox
input_text = tk.Text(root, height=30, width=86, pady=10)

#Frames
button_frame = tk.Frame(root, pady=2)
copy_frame = tk.Frame(root, pady=2)

#buttons
grave_button = tk.Button(button_frame, text='Higlights', command=add_grave_accents)
grave_button.pack(side=tk.TOP)
asterisk_button = tk.Button(button_frame, text='Bold', command=add_asterisks)
asterisk_button.pack(side=tk.TOP)
italics_button = tk.Button(button_frame, text='Italicize', command=make_italics)
italics_button.pack(side=tk.TOP)
domain_ip_button = tk.Button(button_frame, text='''Higlight Domains and IPs 
(works without text selection)''', command=add_grave_to_domains_and_ips)
domain_ip_button.pack(side=tk.TOP)
block_button = tk.Button(button_frame, text='Code Block', command=add_grave_accents_to_block)
block_button.pack(side=tk.TOP)
link_button = tk.Button(button_frame, text='HyperLink Text', command=add_link)
link_button.pack(side=tk.TOP)
copy_button = tk.Button(copy_frame, text='Set Clipboard', fg="green", command=copy)
copy_button.pack(side=tk.TOP, pady=10)
copy_close_button = tk.Button(copy_frame, text='''Set Clipboard and
Close Editor''', fg="red", command=copyandclose)
copy_close_button.pack(side=tk.TOP)
 
#Structure
flabel.grid(row = 0, column = 0, pady = 10, padx = 3)
input_label.grid(row = 0, column = 1, pady = 10, padx = 3, sticky=tk.N)
clabel.grid(row = 0, column = 2, pady = 10, padx = 3, sticky=tk.NE)
button_frame.grid(row = 1, column = 0, pady = 2, padx = 3, sticky=tk.N)
input_text.grid(row = 1, column = 1, pady = 2, padx = 3, sticky=tk.N)
copy_frame.grid(row = 1, column = 2, pady = 2, padx = 3, sticky=tk.N)
switch.grid(row = 2, column = 2, sticky=tk.SE)


#Insert the highlighted and stripped stdout text -TC
input_text.insert('1.0', output)
#Focus the cursor in the textbox cause the box is pretty when its got the border around it -TC 4/23/23
input_text.focus_set()

root.mainloop()
