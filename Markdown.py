import tkinter as tk
import tkinter.simpledialog 
import re 
import enchant
import subprocess
#import enchant

chrome_script = 'tell application "Google Chrome" to set gmyText to execute front window\'s active tab javascript "window.getSelection().toString()"'

result = subprocess.run(['osascript', '-e', chrome_script], capture_output=True, text=True)

output = ''

if result.returncode == 0:
    output = result.stdout.strip()
    print(output)
else:
    error = result.stderr.strip()
    print(f"An error occurred: {error}")

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

# def spellcheck():
#     # Create an Enchant dictionary for the English language
#     d = enchant.Dict("en_US")

#     # Get the text in the input field
#     text = input_text.get("1.0", "end-1c")

#     # Split the text into words and iterate over them
#     for word in text.split():
#         # If the word is not in the dictionary, try to autocorrect it
#         if not d.check(word):
#             corrected_word = d.suggest(word)
#             if corrected_word:
#                 # If the word was autocorrected, highlight it in green
#                 start_index = input_text.search(word, "1.0", "end")
#                 end_index = f"{start_index}+{len(word)}c"
#                 input_text.delete(start_index, end_index)
#                 input_text.insert(start_index, corrected_word[0])
#                 input_text.tag_add("autocorrected", start_index, f"{start_index}+{len(corrected_word[0])}c")
#                 input_text.tag_config("autocorrected", foreground="green")
#             else:
#                 # If the word was not autocorrected, highlight it in red
#                 start_index = input_text.search(word, "1.0", "end")
#                 end_index = f"{start_index}+{len(word)}c"
#                 input_text.tag_add("misspelled", start_index, end_index)
#                 input_text.tag_config("misspelled", foreground="red")

    # num_misspelled = len(input_text.tag_ranges("misspelled"))
    # if num_misspelled == 0:
    #     status = "All words spelled correctly"
    # elif num_misspelled == 1:
    #     status = "1 misspelled word"
    # else:
    #     status = f"{num_misspelled} misspelled words"
    # spellcheck_status.set(status)

root = tk.Tk()
root.title('Text Formatting Tool')

button_frame = tk.Frame(root, pady=10)
button_frame.pack(side=tk.TOP, fill=tk.X)

# button_frame = tk.Frame(root, pady=10)
# button_frame.pack()

grave_button = tk.Button(root, text='Add Higlights', command=add_grave_accents)
grave_button.pack(side=tk.LEFT, padx=5)

asterisk_button = tk.Button(root, text='Bold', command=add_asterisks)
asterisk_button.pack(side=tk.LEFT, padx=5)

italics_button = tk.Button(root, text='Italicize', command=make_italics)
italics_button.pack(side=tk.LEFT, padx=5)

domain_ip_button = tk.Button(root, text='Add Higlights to Domains and IPs (works without text selection)', command=add_grave_to_domains_and_ips)
domain_ip_button.pack(side=tk.LEFT, padx=5)

block_button = tk.Button(root, text='Code Block', command=add_grave_accents_to_block)
block_button.pack(side=tk.LEFT, padx=5)

link_button = tk.Button(root, text='HyperLink Text', command=add_link)
link_button.pack(side=tk.LEFT, padx=5)

input_label = tk.Label(root, text='Enter text:')
input_label.pack()

input_text = tk.Text(root, height=50, width=85)
input_text.pack()

# spellcheck_button = tk.Button(root, text='Spellcheck', command=spellcheck)
# spellcheck_button.pack(side=tk.LEFT, padx=5)

input_text.insert('1.0', output)

root.mainloop()


