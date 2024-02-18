import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, END

def index_sentences_in_text(text, sentences_to_index, words_per_page=100):
    words = text.split()
    pages = [words[i:i + words_per_page] for i in range(0, len(words), words_per_page)]
    index = {}
    for sentence in sentences_to_index:
        for page_number, page in enumerate(pages, start=1):
            page_text = ' '.join(page)
            if sentence in page_text and sentence not in index:
                index[sentence] = page_number
                break
    return index

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        file_path_label.config(text=file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_input.delete('1.0', END)
                text_input.insert('1.0', file.read())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file\n{e}")

def save_index_to_file(index):
    if not index:
        messagebox.showinfo("Info", "No sentences indexed to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding='utf-8') as file:
                for sentence, page in index.items():
                    file.write(f'"{sentence}" وجدت في الصفحة {page}\n')
            messagebox.showinfo("Success", "The index was successfully saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file\n{e}")

def on_index_click():
    text = text_input.get("1.0", END)
    sentences = sentences_input.get().split(',')
    index = index_sentences_in_text(text, sentences)
    save_index_to_file(index)

# Function to add copy-paste functionality to a widget
def add_copy_paste(widget):
    def copy(event=None):
        widget.event_generate("<<Copy>>")

    def paste(event=None):
        widget.event_generate("<<Paste>>")

    def cut(event=None):
        widget.event_generate("<<Cut>>")

    widget.bind("<Control-c>", copy)
    widget.bind("<Control-v>", paste)
    widget.bind("<Control-x>", cut)

window = tk.Tk()
window.title("فهرسة الجمل")
window.configure(bg='#333')

load_file_button = tk.Button(window, text="Load Text File", command=load_file, bg='#555', fg='white')
load_file_button.pack()

file_path_label = tk.Label(window, text="No file selected", fg='white', bg='#333')
file_path_label.pack()

text_input = scrolledtext.ScrolledText(window, height=10, bg='#222', fg='white')
text_input.pack()

sentences_input_label = tk.Label(window, text="Enter sentences to index (comma-separated):", fg='white', bg='#333')
sentences_input_label.pack()

sentences_input = tk.Entry(window, bg='#222', fg='white')
sentences_input.pack()

index_button = tk.Button(window, text="Index and Save", command=on_index_click, bg='#555', fg='white')
index_button.pack()

# Apply copy-paste functionality
add_copy_paste(text_input)
add_copy_paste(sentences_input)

window.mainloop()
