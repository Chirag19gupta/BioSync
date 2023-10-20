import tkinter as tk
from tkinter import ttk
import csv

# Function to search for data in the CSV file and display results
def search_data():
    search_term = entry.get()
    result_text.config(state=tk.NORMAL)  # Enable text widget for editing
    result_text.delete("1.0", tk.END)  # Clear previous results

    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            found = False  # Flag to check if any results were found
            for row in reader:
                if any(search_term in cell for cell in row):
                    found = True
                    result_text.insert(tk.END, ', '.join(row) + '\n\n')  # Add newline between rows

        if not found:
            result_text.insert(tk.END, "No results found.")
    except Exception as e:
        result_text.insert(tk.END, f"Error: {str(e)}")

    result_text.config(state=tk.DISABLED)  # Disable text widget for editing

# Create the main application window
root = tk.Tk()
root.title("CSV Data Search")

# Create and place GUI elements
style = ttk.Style()
style.configure("TButton", padding=(10, 5), font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 14))
style.configure("TEntry", font=("Helvetica", 14))

label = ttk.Label(root, text="Enter data to search:")
label.pack(pady=10)

entry = ttk.Entry(root)
entry.pack()

search_button = ttk.Button(root, text="Search", command=search_data)
search_button.pack()

# Create a text widget to display search results
result_text = tk.Text(root, width=60, height=10, state=tk.DISABLED, font=("Helvetica", 12))
result_text.pack(pady=10)

# Specify the path to the CSV file
csv_path = r"C:\Users\Chirag Gupta\Downloads\tether - Sheet1.csv"

# Start the GUI application
root.mainloop()
