import tkinter as tk
import re
import threading
from tkinter import messagebox, filedialog

def extract_emails():
    text = text_input.get("1.0", "end-1c")
    if not text:
        messagebox.showwarning("Empty Text", "Please enter some text to extract emails.")
        return
    
    # Disable buttons during extraction
    extract_button.config(state="disabled")
    clear_button.config(state="disabled")
    save_button.config(state="disabled")
    
    # Start extraction in a separate thread
    thread = threading.Thread(target=perform_extraction, args=(text,))
    thread.start()

def perform_extraction(text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    
    # Update the GUI with extracted emails
    email_output.delete("1.0", "end")
    if emails:
        for email in emails:
            email_output.insert("end", email + "\n")
        messagebox.showinfo("Extraction Complete", "Email extraction is complete.")
    else:
        email_output.insert("end", "No email addresses found.")
        messagebox.showinfo("Extraction Complete", "No email addresses found.")

    # Re-enable buttons after extraction
    extract_button.config(state="normal")
    clear_button.config(state="normal")
    save_button.config(state="normal")

def clear_text():
    text_input.delete("1.0", "end")
    email_output.delete("1.0", "end")

def save_emails():
    emails = email_output.get("1.0", "end-1c")
    if not emails:
        messagebox.showwarning("No Emails", "No emails to save.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(emails)
            messagebox.showinfo("Save Complete", "Emails saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving emails:\n{str(e)}")

# Create the main window
window = tk.Tk()
window.title("Email Extractor")

# Create the text input box
text_input = tk.Text(window, height=10, width=50)
text_input.pack(padx=10, pady=10)

# Create the extract button
extract_button = tk.Button(window, text="Extract Emails", command=extract_emails)
extract_button.pack(padx=10, pady=5)

# Create the clear button
clear_button = tk.Button(window, text="Clear", command=clear_text)
clear_button.pack(padx=10, pady=5)

# Create the save button
save_button = tk.Button(window, text="Save Emails", command=save_emails)
save_button.pack(padx=10, pady=5)

# Create the email output box
email_output = tk.Text(window, height=10, width=50)
email_output.pack(padx=10, pady=10)

# Run the main window loop
window.mainloop()
