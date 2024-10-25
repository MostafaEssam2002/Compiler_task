import re
import tkinter as tk
from tkinter import ttk
# Define token types
tokens = [
    ('KEYWORD', r'\b(int|return|if|else|while|for|void|char)\b'),  # Keywords in C
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),                 # Identifiers
    ('NUMBER', r'\b\d+\b'),                                         # Integer numbers
    ('OPERATOR', r'[+\-*/=><]'),                                    # Operators
    ('DELIMITER', r'[;,\(\)\{\}]'),                                 # Delimiters
    ('WHITESPACE', r'\s+'),                                         # Whitespaces
    ('UNKNOWN', r'.')                                               # Catch-all for unknown characters
]
# Function to create a scanner for the subset of C
def scanner(code):
    token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in tokens)
    for match in re.finditer(token_regex, code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        if token_type == 'WHITESPACE':
            continue  # Skip whitespaces
        yield (token_type, token_value)
# Function to highlight keywords in the text area
def highlight_syntax(event=None):
    # Remove previous highlights
    text_area.tag_remove("keyword", "1.0", tk.END)
    # Get the current content of the text area
    content = text_area.get("1.0", tk.END)
    # Use the scanner to tokenize the content
    for token_type, token_value in scanner(content):
        if token_type == 'KEYWORD':  # Check if the token is a keyword
            # Find the start and end indices of the keyword in the text area
            start_index = text_area.search(token_value, "1.0", stopindex=tk.END)
            while start_index:
                end_index = f"{start_index}+{len(token_value)}c"
                # Apply the tag to highlight the keyword
                text_area.tag_add("keyword", start_index, end_index)
                start_index = text_area.search(token_value, end_index, stopindex=tk.END)

# Function to display the tokens in the table
def print_content():
    content = text_area.get("1.0", tk.END)
    # Clear the table first
    for i in tree.get_children():
        tree.delete(i)
    # Add token_type and token_value to the tree view (table)
    for token_type, token_value in scanner(content):
        tree.insert("", tk.END, values=(token_type, token_value))

# Create the main window
frm = tk.Tk()
frm.title("Text Area with Syntax Highlighting")

# Create a Text widget
text_area = tk.Text(frm, height=10, width=40)
text_area.pack(pady=10)

# Configure the tag for keywords (changing the color to red)
text_area.tag_configure("keyword", foreground="red")

# Bind the event of typing in the text area to the highlight_syntax function
text_area.bind("<KeyRelease>", highlight_syntax)

# Create a Button to print the content
print_button = tk.Button(frm, text="Print Tokens", command=print_content)
print_button.pack(pady=5)

# Create a Treeview widget (table) to display token_type and token_value
tree = ttk.Treeview(frm, columns=("token_type", "token_value"), show='headings', height=10)
tree.heading("token_type", text="Token Type")
tree.heading("token_value", text="Token Value")
tree.pack(pady=10)

# Run the Tkinter event loop
frm.mainloop()
