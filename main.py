import re
import tkinter as tk
from tkinter import ttk
tokens = [
    ('KEYWORD', r'\b(int|return|if|else|while|for|void|char)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('OPERATOR', r'[+\-*/=><]'),
    ('NUMERIC_CONSTANT', r'\b\d+\b'),
    ('CHARACTER_CONSTANT', r"'.'"),
    ('COMMENT', r'//.|/\[\s\S]?\/'),
    ('SPECIAL_CHARACTER', r'[;,\(\)\{\}]'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'.')
]
def scanner(code):
    token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in tokens)
    for match in re.finditer(token_regex, code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type == 'WHITESPACE':
            continue
        yield (token_type, token_value)
def highlight_syntax(event=None):
    text_area.tag_remove("keyword", "1.0", tk.END)
    content = text_area.get("1.0", tk.END)
    for token_type, token_value in scanner(content):
        if token_type == 'KEYWORD':  
            start_index = text_area.search(token_value, "1.0", stopindex=tk.END)
            while start_index:
                end_index = f"{start_index}+{len(token_value)}c"
                text_area.tag_add("keyword", start_index, end_index)
                start_index = text_area.search(token_value, end_index, stopindex=tk.END)
def print_content():
    content = text_area.get("1.0", tk.END)
    for i in tree.get_children():
        tree.delete(i)
    for token_type, token_value in scanner(content):
        tree.insert("", tk.END, values=(token_type, token_value))
frm = tk.Tk()
frm.title("Text Area with Syntax Highlighting")
text_area = tk.Text(frm, height=10, width=40)
text_area.pack(pady=10)
text_area.tag_configure("keyword", foreground="red")
text_area.bind("<KeyRelease>", highlight_syntax)
print_button = tk.Button(frm, text="Print Tokens", command=print_content)
print_button.pack(pady=5)
tree = ttk.Treeview(frm, columns=("token_type", "token_value"), show='headings', height=10)
tree.heading("token_type", text="Token Type")
tree.heading("token_value", text="Token Value")
tree.pack(pady=10)
frm.mainloop() 
