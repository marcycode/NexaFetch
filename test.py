import tkinter as tk
from tkinter import ttk, messagebox
from metaphor_python import Metaphor
import webbrowser


class MetaphorApp:

    def __init__(self, root, api_key):
        self.api = Metaphor(api_key=api_key)

        self.root = root
        self.root.title("Searchy")

        tk.Label(root, text="Enter your query:").pack(pady=20)

        self.search_entry = ttk.Entry(root, width=50)
        self.search_entry.pack(pady=20)

        self.search_button = ttk.Button(root, text="Search", command=self.search)
        self.search_button.pack(pady=20)

        self.results_listbox = tk.Listbox(root, width=50, height=10)
        self.results_listbox.pack(pady=20)
        self.results_listbox.bind("<Double-Button-1>", self.show_content)

        self.status_label = ttk.Label(root, text="Enter a query and click Search.")
        self.status_label.pack(pady=20)

    def search(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showerror("Error", "What would you like to search today?")
            return

        try:
            response = self.api.search(query=query, num_results=10)
            self.results_listbox.delete(0, tk.END)  # Clear current results

            if not response.results:
                self.status_label.config(text="No results found!")
                return

            for result in response.results:
                self.results_listbox.insert(tk.END, result.title)

            self.results = response.results
            self.status_label.config(text=f"Showing top {len(response.results)} results. Double click to view content.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_content(self, event=None):
        selected_index = self.results_listbox.curselection()[0]
        selected_result = self.results[selected_index]
        content = self.api.get_contents([selected_result.id])

        # Display content in a new window
        # Open the link in Chrome
        url = selected_result.url
        try:
            webbrowser.get("chrome").open(url)
        except webbrowser.Error:
            # If Chrome isn't found, fall back to the default web browser.
            webbrowser.open(url)


if __name__ == "__main__":
    API_KEY = "7bf46fdf-8ff4-4c36-ae4f-8b32513c8a63"  # Replace with your API key
    root = tk.Tk()
    app = MetaphorApp(root, API_KEY)
    root.mainloop()
