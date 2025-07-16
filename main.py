import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PyPDF2 import PdfMerger


class PDFCombiner:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Combiner")
        self.root.geometry("600x400")

        # List to store selected PDF files
        self.pdf_files = []

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, text="PDF Combiner", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Add PDFs button
        add_button = tk.Button(
            button_frame,
            text="Add PDF Files",
            command=self.add_pdfs,
            font=("Arial", 10),
        )
        add_button.pack(side=tk.LEFT, padx=5)

        # Remove selected button
        remove_button = tk.Button(
            button_frame,
            text="Remove Selected",
            command=self.remove_selected,
            font=("Arial", 10),
        )
        remove_button.pack(side=tk.LEFT, padx=5)

        # Clear all button
        clear_button = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            font=("Arial", 10),
        )
        clear_button.pack(side=tk.LEFT, padx=5)

        # Files list label
        list_label = tk.Label(self.root, text="Selected PDF Files:", font=("Arial", 12))
        list_label.pack(pady=(20, 5), anchor="w", padx=20)

        # Frame for listbox and scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # Listbox to display selected files
        self.files_listbox = tk.Listbox(
            list_frame, selectmode=tk.SINGLE, font=("Arial", 10)
        )
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=scrollbar.set)

        # Move up/down buttons frame
        move_frame = tk.Frame(self.root)
        move_frame.pack(pady=10)

        move_up_button = tk.Button(
            move_frame,
            text="Move Up",
            command=self.move_up,
            font=("Arial", 10),
        )
        move_up_button.pack(side=tk.LEFT, padx=5)

        move_down_button = tk.Button(
            move_frame,
            text="Move Down",
            command=self.move_down,
            font=("Arial", 10),
        )
        move_down_button.pack(side=tk.LEFT, padx=5)

        # Combine button
        combine_button = tk.Button(
            self.root,
            text="Combine PDFs",
            command=self.combine_pdfs,
            font=("Arial", 12, "bold"),
        )
        combine_button.pack(pady=20)

        # Status label
        self.status_label = tk.Label(
            self.root, text="Ready to combine PDFs", font=("Arial", 10), fg="green"
        )
        self.status_label.pack(pady=5)

    def add_pdfs(self):
        """Add PDF files to the list"""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )

        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.files_listbox.insert(tk.END, os.path.basename(file))

        self.update_status(
            f"Added {len(files)} file(s). Total: {len(self.pdf_files)} files"
        )

    def remove_selected(self):
        """Remove selected file from the list"""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            self.pdf_files.pop(index)
            self.files_listbox.delete(index)
            self.update_status("File removed")
        else:
            messagebox.showwarning("No Selection", "Please select a file to remove")

    def clear_all(self):
        """Clear all files from the list"""
        self.pdf_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.update_status("All files cleared")

    def move_up(self):
        """Move selected file up in the list"""
        selection = self.files_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            # Swap in the list
            self.pdf_files[index], self.pdf_files[index - 1] = (
                self.pdf_files[index - 1],
                self.pdf_files[index],
            )
            # Update listbox
            self.files_listbox.delete(index)
            self.files_listbox.insert(
                index - 1, os.path.basename(self.pdf_files[index - 1])
            )
            self.files_listbox.selection_set(index - 1)

    def move_down(self):
        """Move selected file down in the list"""
        selection = self.files_listbox.curselection()
        if selection and selection[0] < len(self.pdf_files) - 1:
            index = selection[0]
            # Swap in the list
            self.pdf_files[index], self.pdf_files[index + 1] = (
                self.pdf_files[index + 1],
                self.pdf_files[index],
            )
            # Update listbox
            self.files_listbox.delete(index)
            self.files_listbox.insert(
                index + 1, os.path.basename(self.pdf_files[index + 1])
            )
            self.files_listbox.selection_set(index + 1)

    def combine_pdfs(self):
        """Combine all selected PDFs into one file"""
        if not self.pdf_files:
            messagebox.showwarning("No Files", "Please add PDF files to combine")
            return

        # Ask for output file location
        output_file = filedialog.asksaveasfilename(
            title="Save Combined PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )

        if not output_file:
            return

        try:
            self.update_status("Combining PDFs...")

            # Create PDF merger object
            merger = PdfMerger()

            # Add each PDF to the merger
            for pdf_file in self.pdf_files:
                merger.append(pdf_file)

            # Write the combined PDF
            merger.write(output_file)
            merger.close()

            self.update_status(
                f"Successfully combined {len(self.pdf_files)} PDFs into {os.path.basename(output_file)}"
            )
            messagebox.showinfo(
                "Success", f"PDFs combined successfully!\nSaved as: {output_file}"
            )

        except Exception as e:
            error_msg = f"Error combining PDFs: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Error", error_msg)

    def update_status(self, message):
        """Update the status label"""
        self.status_label.config(text=message)
        self.root.update_idletasks()


def main():
    root = tk.Tk()
    app = PDFCombiner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
