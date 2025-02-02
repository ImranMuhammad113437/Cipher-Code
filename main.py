import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox as messagebox
import random
from math import gcd
from PIL import Image, ImageTk
import hashlib

class CipherInterface:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x590+0+0")  # Fixed window size
        self.root.title("Cipher Vault")
        self.root.resizable(False, False)

        # Load the background image
        image_path = "wp2701680-electronic-wallpaper.png"
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1024, 590), Image.Resampling.LANCZOS)  # Resize image to fit frame dimensions
        self.bg_photo = ImageTk.PhotoImage(bg_image)  # Save to instance variable to avoid garbage collection

        # Create the top frame
        self.top_frame = Frame(root, height=590, width=1024)
        self.top_frame.place(x=0, y=0)

        # Add the image as the background
        bg_label = Label(self.top_frame, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label, centered at the top with border color
        self.title_label = tk.Label(
            self.top_frame, 
            text="Cipher Vault", 
            font=("Arial", 24, "bold"), 
            bg="#111111", 
            fg="#05cacf", 
            bd=2,  # Border thickness
            highlightbackground="#05cacf",  # Border color
            highlightcolor="#05cacf",       # Border color when focused
            highlightthickness=2            # Border thickness around the label
        )
        self.title_label.place(relx=0.5, y=20, anchor="center")  # Centered horizontally with relx=0.5

        # Input Frame
        self.left_frame = tk.LabelFrame(
            self.top_frame,
            text="Input",
            width=300,
            height=230,
            bg="#111111",
            fg="#05cacf",
            font=("Comic Sans MS", 12),
            bd=0,
            highlightbackground="#05cacf",
            highlightcolor="#05cacf",
            highlightthickness=2,
        )
        self.left_frame.place(x=10, y=60)

        self.input_textbox = tk.Text(self.left_frame, width=30, height=10, font=("Arial", 12), bg="#111111", fg="#05cacf")
        self.input_textbox.place(x=10, y=10)

        # Process Frame
        self.middle_frame = tk.LabelFrame(
            self.top_frame,
            text="Process",
            width=300,
            height=320,
            bg="#111111",
            fg="#05cacf",
            bd=0,
            font=("Comic Sans MS", 12),
            highlightbackground="#05cacf",
            highlightcolor="#05cacf",
            highlightthickness=2,
        )
        self.middle_frame.place(x=340, y=60)

        self.cipher_type_label = tk.Label(self.middle_frame, text="Select Cipher Type", bg="#111111", fg="#05cacf")
        self.cipher_type_label.place(x=10, y=10)

        self.cipher_names = ["Select Cipher", "Caesar Cipher", "Vigenère Cipher", "One-Time Pad", 
                             "Playfair Cipher", "Monoalphabetic Cipher", "Brute Force",
                             "Transposition Cipher", "Rail Fence Cipher", "Affine Cipher"]
        self.selected_cipher = tk.StringVar()
        self.selected_cipher.set(self.cipher_names[0])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            background="#111111", 
            fieldbackground="#111111",
            foreground="#05cacf", 
            bordercolor="#05cacf", 
            arrowsize=15
        )
        style.map(
            "TCombobox",
            background=[("readonly", "#111111")],  
            fieldbackground=[("readonly", "#111111")],  
            foreground=[("readonly", "#05cacf")]
        )

        self.cipher_combobox = ttk.Combobox(self.middle_frame, textvariable=self.selected_cipher, values=self.cipher_names, state="readonly", style="TCombobox")
        self.cipher_combobox.place(x=10, y=40, width=280)
        self.cipher_combobox.current(0)

        self.key_label = tk.Label(self.middle_frame, text="Key (Numerical): ", bg="#111111", fg="#05cacf")
        self.key_label.place(x=10, y=70)
        self.key_entry = tk.Entry(self.middle_frame, width=25, bg="#111111", fg="#05cacf")
        self.key_entry.place(x=120, y=70)

        self.keyword_label = tk.Label(self.middle_frame, text="Keyword: ", bg="#111111", fg="#05cacf")
        self.keyword_label.place(x=10, y=100)
        self.keyword_entry = tk.Entry(self.middle_frame, width=25, bg="#111111", fg="#05cacf")
        self.keyword_entry.place(x=120, y=100)

        # Rail Cipher Additional Fields
        self.railrows_label = tk.Label(self.middle_frame, text="Number of Rows (Rail Cipher): ", bg="#111111", fg="#05cacf")
        self.railrows_label.place(x=10, y=130)
        self.railrows_entry = tk.Entry(self.middle_frame, width=12, bg="#111111", fg="#05cacf")
        self.railrows_entry.place(x=200, y=130)

        self.colseq_label = tk.Label(self.middle_frame, text="Column Sequence: ", bg="#111111", fg="#05cacf")
        self.colseq_label.place(x=10, y=160)
        self.colseq_entry = tk.Entry(self.middle_frame, width=20, bg="#111111", fg="#05cacf")
        self.colseq_entry.place(x=150, y=160)

        # Transposition ComboBox
        self.transposition_combo = ttk.Combobox(self.middle_frame, values=["Select position for Transposition (default)", "Row-wise", "Column-wise"], state="readonly", style="TCombobox")
        self.transposition_combo.place(x=10, y=190, width=280)
        self.transposition_combo.set("Select position for Transposition:")

        # Key a and Key b for Affine Cipher
        self.key_a_label = tk.Label(self.middle_frame, text="Key (a):", bg="#111111", fg="#05cacf")
        self.key_a_label.place(x=10, y=220)
        self.key_a_combobox = ttk.Combobox(self.middle_frame, values=[1, 3, 5, 7, 11, 15, 17, 19, 21, 23, 25], width=9)
        self.key_a_combobox.place(x=70, y=220)
        self.key_a_combobox.set(1)

        self.key_b_label = tk.Label(self.middle_frame, text="Key (b):", bg="#111111", fg="#05cacf")
        self.key_b_label.place(x=160, y=220)
        self.key_b_combobox = ttk.Combobox(self.middle_frame, values=list(range(26)), width=8)
        self.key_b_combobox.place(x=220, y=220)
        self.key_b_combobox.set(0)

        # Reset Button
        self.reset_button = tk.Button(self.middle_frame, text="Reset", bg="#05cacf", fg="#111111", font=("Comic Sans MS", 12), command=self.reset_inputs, width=20)
        self.reset_button.place(x=40, y=250)

        self.cipher_combobox.bind("<<ComboboxSelected>>", self.check_on_cipher)

        # Output Frame
        self.right_frame = tk.LabelFrame(
            self.top_frame, 
            text="Output", 
            width=300, 
            height=320, 
            bg="#111111", 
            fg="#05cacf", 
            bd=0, 
            font=("Comic Sans MS", 12),
            highlightbackground="#05cacf",  
            highlightcolor="#05cacf",       
            highlightthickness=2            
        )
        self.right_frame.place(x=670, y=60)

        self.output_textbox = tk.Text(self.right_frame, width=30, height=15, font=("Arial", 12), bg="#111111", fg="#05cacf")
        self.output_textbox.place(x=10, y=10)

        #-----------------------------------------------------------------------------------------------------------------------

        # Creating the "Action" LabelFrame below the "left_frame" with the same width and height 50
        self.action_frame = tk.LabelFrame(
            self.top_frame, 
            text="Action", 
            width=300, 
            height=120, 
            bg="#111111", 
            fg="#05cacf", 
            bd=0, 
            font=("Comic Sans MS", 12),
            highlightbackground="#05cacf",  # Border color
            highlightcolor="#05cacf",       # Border color when focused
            highlightthickness=2            # Border thickness
        )
        self.action_frame.place(x=10, y=320)  # Adjust the y-coordinate to place it below the left_frame

        # Encrypt button
        self.encrypt_button = tk.Button(
            self.action_frame, 
            text="Encrypt",
            bg="#05cacf",
            fg="#111111",
            font=("Comic Sans MS", 12), 
            command=self.encryption_action
        )
        self.encrypt_button.place(x=5, y=0, width=140, height=30)  # Place the Encrypt button

        # Decrypt button
        self.decrypt_button = tk.Button(
            self.action_frame, 
            text="Decrypt",
            bg="#05cacf",
            fg="#111111",
            font=("Comic Sans MS", 12), 
            command=self.decryption_action
        )
        self.decrypt_button.place(x=155, y=0, width=140, height=30)  # Place the Decrypt button

        # SHA-256 button
        self.sha256_button = tk.Button(
            self.action_frame, 
            text="SHA-256",
            bg="#05cacf",
            fg="#111111",
            font=("Comic Sans MS", 12), 
            command=self.hashing_SHA_256  # Replace with the actual function
        )
        self.sha256_button.place(x=5, y=40, width=140, height=30)  # Place the SHA-256 button below Encrypt

        # MD5 button
        self.md5_button = tk.Button(
            self.action_frame, 
            text="MD5",
            bg="#05cacf",
            fg="#111111",
            font=("Comic Sans MS", 12), 
            command=self.hashing_MD5  # Replace with the actual function
        )
        self.md5_button.place(x=155, y=40, width=140, height=30)  # Place the MD5 button below Decrypt

        #-----------------------------------------------------------------------------------------------------------------------    
        # Creating the "Monoalphabetic Cipher" LabelFrame below the "Action" LabelFrame
        self.cipher_frame = tk.LabelFrame(
            self.top_frame, 
            text="Monoalphabetic Cipher", 
            width=300, 
            height=180, 
            bg="#111111", 
            fg="#05cacf", 
            bd=0, 
            font=("Comic Sans MS", 12),
            highlightbackground="#05cacf",  # Border color
            highlightcolor="#05cacf",       # Border color when focused
            highlightthickness=2            # Border thickness
        )
        self.cipher_frame.place(x=340, y=400)  # Adjust the y-coordinate to place it below the action_frame

        # Adding the alphabet row (A-Z)
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            label = tk.Label(self.cipher_frame, text=letter, font=("Arial", 10), bg="#111111", fg="#05cacf")
            label.grid(row=0, column=i, padx=2, pady=5)  # Placing letters in the first row

        # Adding the "=" signs below each letter
        for i in range(26):
            equals_label = tk.Label(self.cipher_frame, text="=", font=("Arial", 10), bg="#111111", fg="#05cacf")
            equals_label.grid(row=1, column=i, padx=2, pady=5)  # Placing "=" in the second row

        # Adding the read-only fields below each "=" sign
        self.fields = []  # Store Entry widgets for later manipulation
        for i in range(26):
            field = tk.Entry(self.cipher_frame, width=2, state="normal", justify="center", bg="#111111", fg="#05cacf")
            field.grid(row=2, column=i, padx=2, pady=5)  # Placing entry fields in the third row
            self.fields.append(field)  # Add the Entry widget to the list


        # Adding the "Generate" button in row 3 and disabling it initially
        self.generate_button = tk.Button(self.cipher_frame, text="Generate Cipher",bg="#05cacf",fg="#111111",font=("Comic Sans MS", 12), command=self.generate_random_cipher, state="disabled")
        self.generate_button.grid(row=3, column=0, columnspan=13, pady=10)  # Span the button across half of the columns

        # Adding the "Reset" button in row 3 and disabling it initially
        self.reset_button = tk.Button(self.cipher_frame, text="Reset Cipher",bg="#05cacf",fg="#111111",font=("Comic Sans MS", 12), command=self.reset_cipher, state="disabled")
        self.reset_button.grid(row=3, column=13, columnspan=13, pady=10)  # Span the button across the other half of the columns

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------


























#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Main Function-------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
    
    def encryption_action(self):
        # Get the selected cipher type from the combobox
        selected_cipher = self.cipher_combobox.get()
        
        # Check which cipher is selected and perform its encryption
        if selected_cipher == "Caesar Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Caesar cipher encryption function
            self.encryption_caesar_cipher()

        elif selected_cipher == "Vigenère Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Vigenère cipher encryption function
            self.encryption_vigenere_cipher()

        elif selected_cipher == "One-Time Pad":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the One-Time Pad encryption function
            self.encryption_one_time_pad()

        elif selected_cipher == "Playfair Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Playfair cipher encryption function
            self.encryption_playfair_cipher()

        elif selected_cipher == "Monoalphabetic Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Monoalphabetic cipher encryption function
            self.encryption_monoalphabetic_cipher()

        elif selected_cipher == "Brute Force":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Brute Force encryption function
            self.encryption_brute_force()

        elif selected_cipher == "Reil Fence Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Rail Fence cipher encryption function
            self.encryption_reil_cipher()

        elif selected_cipher == "Transposition Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Perform an additional check for numerical input validity
            if self.numerical_check():  # Check if the numerical input is valid
                # Call the Transposition cipher encryption function
                self.encryption_transposition()
            else:
                # Display an error message if the numerical input is invalid
                self.output_textbox.insert(1.0, "Error: Invalid input in numerical fields.")

        elif selected_cipher == "Affine Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Affine cipher encryption function
            self.encryption_affine_cipher()

        else:
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Display an empty message if no valid cipher is selected
            self.output_textbox.insert(tk.END, " ")  # Handle cases where the selected cipher is not listed

    
    def decryption_action(self):
        # Get the selected cipher type from the combobox
        selected_cipher = self.cipher_combobox.get()

        # Check which cipher is selected and perform its corresponding decryption
        if selected_cipher == "Caesar Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Caesar cipher decryption function
            self.decryption_caesar_cipher()

        elif selected_cipher == "Brute Force":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Brute Force decryption function
            self.decryption_brute_force()

        elif selected_cipher == "Vigenère Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Vigenère cipher decryption function
            self.decryption_vigenere_cipher()

        elif selected_cipher == "One-Time Pad":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the One-Time Pad decryption function
            self.decryption_one_time_pad()

        elif selected_cipher == "Playfair Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Playfair cipher decryption function
            self.decryption_playfair_cipher()

        elif selected_cipher == "Monoalphabetic Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Monoalphabetic cipher decryption function
            self.decryption_monoalphabetic_cipher()

        elif selected_cipher == "Reil Fence Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Rail Fence cipher decryption function
            self.decryption_reil_cipher()

        elif selected_cipher == "Transposition Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Perform an additional check for numerical input validity
            if self.numerical_check():  # If the numerical input is valid
                # Call the Transposition cipher decryption function
                self.decryption_transposition()
            else:
                # Display an error message if the numerical input is invalid
                self.output_textbox.insert(1.0, "Error: Invalid input in numerical fields.")

        elif selected_cipher == "Affine Cipher":
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Call the Affine cipher decryption function
            self.decryption_affine_cipher()

        else:
            # Clear the output textbox
            self.output_textbox.delete(1.0, tk.END)
            # Insert an empty message if no valid cipher is selected
            self.output_textbox.insert(tk.END, " ")  # Handle cases where the selected cipher is not listed

         


    def numerical_check(self):
        """
        Validates the input in self.colseq_entry.
        Ensures:
            - No duplicate numbers in the input.
            - Length matches the value in self.key_entry.
            - No zeros in the input.
            - All digits in colseq are less than or equal to key_entry.
        """
        colseq = self.colseq_entry.get()
        key_length = self.key_entry.get()

        # Check if key_entry is a valid number
        if not key_length.isdigit():
            tk.messagebox.showerror("Error", "Key must be a number.")
            return False

        key_length = int(key_length)

        # Check if colseq contains only digits
        if not colseq.isdigit():
            tk.messagebox.showerror("Error", "Column Sequence must contain only numbers.")
            return False

        # Check if length of colseq matches key length
        if len(colseq) != key_length:
            tk.messagebox.showerror("Error", "Column Sequence length must match the key value.")
            return False

        # Check for duplicates and presence of '0'
        if len(set(colseq)) != len(colseq):
            tk.messagebox.showerror("Error", "Column Sequence must not contain duplicate numbers.")
            return False

        if '0' in colseq:
            tk.messagebox.showerror("Error", "Column Sequence must not contain the digit 0.")
            return False

        # Check if all digits in colseq are <= key_length
        if any(int(digit) > key_length for digit in colseq):
            tk.messagebox.showerror(
                "Error", 
                f"All digits in Column Sequence must be less than or equal to {key_length}."
            )
            return False

        # All checks passed
        tk.messagebox.showinfo("Success", "Column Sequence is valid.")
        return True


    

    

        
    # Function to generate random positions of the alphabet
    def generate_random_cipher(self):
        random_alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(random_alphabet)  # Shuffle the alphabet randomly
        for i, letter in enumerate(random_alphabet):
            self.fields[i].config(state="normal")  # Enable the field temporarily
            self.fields[i].delete(0, "end")  # Clear any existing value
            self.fields[i].insert(0, letter)  # Insert the random letter
            self.fields[i].config(state="readonly")  # Set the field back to readonly
    
    
    def check_on_cipher(self, event=None):
       
        selected_cipher = self.cipher_combobox.get()
        self.output_textbox.delete(1.0, tk.END)

        # Check the value of the selected cipher and handle accordingly
        if selected_cipher == "Caesar Cipher":
            self.key_entry.configure(state="normal")
            self.keyword_entry.configure(state="disabled")
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disabled")
            self.key_a_combobox.configure(state="disabled")
            self.key_b_combobox.configure(state="disabled")

        elif selected_cipher == "Vigenère Cipher":
            self.keyword_entry.configure(state="normal")
            self.key_entry.configure(state="disable")
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disabled")
            self.key_a_combobox.configure(state="disabled")
            self.key_b_combobox.configure(state="disabled")

        elif selected_cipher == "One-Time Pad":
            self.keyword_entry.configure(state="normal")
            self.key_entry.configure(state="disable")
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disabled")
            self.key_a_combobox.configure(state="disabled")
            self.key_b_combobox.configure(state="disabled")

            
        elif selected_cipher == "Playfair Cipher":
            self.keyword_entry.configure(state="normal")
            self.key_entry.configure(state="disable")
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disabled")
            self.key_a_combobox.configure(state="disabled")
            self.key_b_combobox.configure(state="disabled")

            
        elif selected_cipher == "Monoalphabetic Cipher":
            self.generate_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.keyword_entry.configure(state="disable")
            self.key_entry.configure(state="disable")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disabled")
            self.key_a_combobox.configure(state="disabled")
            self.key_b_combobox.configure(state="disabled")


        elif selected_cipher == "Brute Force":
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.keyword_entry.configure(state="disable")
            self.key_entry.configure(state="disable")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disabled")
            self.key_a_combobox.configure(state="disabled")
            self.key_b_combobox.configure(state="disabled")


        elif selected_cipher == "Reil Fence Cipher":
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.keyword_entry.configure(state="disable")
            self.key_entry.configure(state="disable")
            self.railrows_entry.config(state="normal")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disabled")
            self.key_a_combobox.configure(state="disabled")
            self.key_b_combobox.configure(state="disabled")

        
        elif selected_cipher == "Transposition Cipher":
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.keyword_entry.configure(state="disable")
            self.key_entry.configure(state="normal")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="normal")
            self.transposition_combo.configure(state="normal")
            self.key_a_combobox.configure(state="disabled")
            self.key_b_combobox.configure(state="disabled")


        elif selected_cipher == "Affine Cipher":
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.keyword_entry.configure(state="disable")
            self.key_entry.configure(state="disable")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disable")
            self.key_a_combobox.configure(state="normal")
            self.key_b_combobox.configure(state="normal")


        else:
            self.output_textbox.insert(tk.END, " ")
            self.generate_button.config(state="disable")
            self.reset_button.config(state="disable")
            self.keyword_entry.configure(state="disable")
            self.key_entry.configure(state="disable")
            self.railrows_entry.config(state="disable")
            self.colseq_entry.config(state="disable")
            self.transposition_combo.configure(state="disable")
            self.key_a_combobox.configure(state="disable")
            self.key_b_combobox.configure(state="disable")
    
    def reset_inputs(self):
        # Reset the combobox to the default value
        self.selected_cipher.set(self.cipher_names[0])
        self.keyword_entry.configure(state="normal")
        self.key_entry.configure(state="normal")
        self.generate_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.railrows_entry.config(state="normal")
        self.colseq_entry.config(state="normal")
        self.transposition_combo.configure(state="normal")

        # Clear the key entry field
        self.key_entry.delete(0, tk.END)
        self.keyword_entry.delete(0, tk.END)
        self.railrows_entry.delete(0, tk.END)

    # Function to reset the fields
    def reset_cipher(self):
        for field in self.fields:
            field.config(state="normal")  # Enable the field temporarily
            field.delete(0, "end")  # Clear any existing value
            field.config(state="readonly")  # Set the field back to readonly

    def generate_key_square(self, keyword):
        # Remove duplicates and add the rest of the alphabet
        keyword = keyword.upper().replace("J", "I")
        key_square = []
        used = set()

        for char in keyword:
            if char not in used and char.isalpha():
                key_square.append(char)
                used.add(char)

        for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            if char not in used:
                key_square.append(char)

        return [key_square[i:i + 5] for i in range(0, 25, 5)]

    def find_position(self, key_square, char):
        for row_idx, row in enumerate(key_square):
            if char in row:
                return row_idx, row.index(char)
        return None

    def prepare_text(self, text, filler="X"):
        text = text.upper().replace("J", "I")
        prepared = ""

        i = 0
        while i < len(text):
            if text[i].isalpha():
                if i + 1 < len(text) and text[i] == text[i + 1]:  # Check for duplicate consecutive letters
                    prepared += text[i] + filler
                else:
                    prepared += text[i]
            i += 1

        if len(prepared) % 2 != 0:  # Ensure length is even
            prepared += filler

        return prepared
    
    def generate_key(self,text, key):
        """
        Expands the key to match the length of the text.
        """
        key = key.upper()  # Normalize key to uppercase
        key = (key * (len(text) // len(key))) + key[:len(text) % len(key)]
        return key









































#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Cipher Function-----------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
    



#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Affine Cipher-------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

    def decryption_affine_cipher(self):
        ciphertext = self.input_textbox.get("1.0", "end-1c")
        key_a = int(self.key_a_combobox.get())
        key_b = int(self.key_b_combobox.get())
        
        # Ensure 'a' is coprime with 26 (for the cipher to work)
        if gcd(key_a, 26) != 1:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "Invalid key 'a', must be coprime with 26")
            return

        # Find the modular inverse of 'a' modulo 26
        a_inv = None
        for i in range(26):
            if (key_a * i) % 26 == 1:
                a_inv = i
                break
        
        if a_inv is None:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "No modular inverse for 'a'. Decryption impossible.")
            return
        
        plaintext = ""
        
        for char in ciphertext:
            if char.isalpha():  # Only process alphabetic characters
                shift = ord(char.lower()) - ord('a')
                decrypted_char = (a_inv * (shift - key_b)) % 26
                decrypted_char = chr(decrypted_char + ord('a'))
                if char.isupper():
                    decrypted_char = decrypted_char.upper()
                plaintext += decrypted_char
            else:
                plaintext += char  # Non-alphabetic characters are unchanged

        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", plaintext)

    
    def encryption_affine_cipher(self):
        plaintext = self.input_textbox.get("1.0", "end-1c")
        key_a = int(self.key_a_combobox.get())
        key_b = int(self.key_b_combobox.get())
        
        # Ensure 'a' is coprime with 26 (for the cipher to work)
        if gcd(key_a, 26) != 1:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "Invalid key 'a', must be coprime with 26")
            return
        
        ciphertext = ""
        
        for char in plaintext:
            if char.isalpha():  # Only process alphabetic characters
                shift = ord(char.lower()) - ord('a')
                encrypted_char = (key_a * shift + key_b) % 26
                encrypted_char = chr(encrypted_char + ord('a'))
                if char.isupper():
                    encrypted_char = encrypted_char.upper()
                ciphertext += encrypted_char
            else:
                ciphertext += char  # Non-alphabetic characters are unchanged

        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", ciphertext)

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Transposition Cipher------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

    def decryption_transposition(self):
        ciphertext = self.input_textbox.get("1.0", "end").strip()  # Retrieve ciphertext
        num_columns = int(self.key_entry.get().strip())  # Number of columns
        column_sequence = [int(x) - 1 for x in self.colseq_entry.get().strip()]  # Convert to 0-based index
        cipher_mode = self.transposition_combo.get().strip()  # Cipher mode: Row-wise or Column-wise

        # Validate input
        if len(column_sequence) != num_columns:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "Error: Column sequence length must match the number of columns.")
            return

        if cipher_mode not in ["Row-wise", "Column-wise"]:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "Error: Invalid transposition mode selected.")
            return

        # Calculate the number of rows
        num_rows = len(ciphertext) // num_columns

        if cipher_mode == "Row-wise":
            # Reconstruct the original grid with reversed column order
            reverse_sequence = [column_sequence.index(i) for i in range(num_columns)]
            rows = [ciphertext[i:i + num_columns] for i in range(0, len(ciphertext), num_columns)]
            decrypted_text = "".join(
                "".join(row[reverse_sequence[j]] for j in range(num_columns)) for row in rows
            )
        else:  # Column-wise
            # Reconstruct the grid column by column and reverse the column rearrangement
            cols = [ciphertext[i * num_rows:(i + 1) * num_rows] for i in range(num_columns)]
            reverse_sequence = [column_sequence.index(i) for i in range(num_columns)]
            reordered_cols = [cols[reverse_sequence[i]] for i in range(num_columns)]
            decrypted_text = "".join("".join(row) for row in zip(*reordered_cols))

        # Strip padding spaces and display the result
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", decrypted_text.strip())

    
    def encryption_transposition(self):
        plaintext = self.input_textbox.get("1.0", "end").strip().replace(" ", "")  # Retrieve plaintext and remove spaces
        num_columns = int(self.key_entry.get().strip())  # Number of columns
        column_sequence = [int(x) - 1 for x in self.colseq_entry.get().strip()]  # Convert to 0-based index
        cipher_mode = self.transposition_combo.get().strip()  # Cipher mode: Row-wise or Column-wise

        # Validate input
        if len(column_sequence) != num_columns:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "Error: Column sequence length must match the number of columns.")
            return

        if cipher_mode not in ["Row-wise", "Column-wise"]:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "Error: Invalid transposition mode selected.")
            return

        # Pad plaintext to fit the grid
        while len(plaintext) % num_columns != 0:
            plaintext += " "

        # Divide plaintext into rows
        rows = [plaintext[i:i + num_columns] for i in range(0, len(plaintext), num_columns)]

        # Perform transposition
        if cipher_mode == "Row-wise":
            # Rearrange columns in the specified order
            transposed_text = "".join(
                "".join(row[col] for col in column_sequence) for row in rows
            )
        else:  # Column-wise
            # Rearrange rows in the column-first order
            transposed_columns = ["".join(row[col] for row in rows) for col in column_sequence]
            transposed_text = "".join(transposed_columns)

        # Display the result
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", transposed_text)

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Reil Fence Cipher---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
  
    def decryption_reil_cipher(self):
        # Retrieve input text and number of rows
        cipher_text = self.input_textbox.get("1.0", "end").strip()  # Get encrypted text from the textbox
        num_rows = int(self.railrows_entry.get())  # Get the number of rows from entry

        # Validate inputs
        if not cipher_text or num_rows <= 1:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "Invalid input! Ensure text is not empty and rows > 1.")
            return

        # Determine the zigzag pattern
        rail = [['' for _ in range(len(cipher_text))] for _ in range(num_rows)]
        direction_down = None
        row, col = 0, 0

        # Mark the zigzag pattern
        for _ in range(len(cipher_text)):
            rail[row][col] = '*'
            col += 1
            if row == 0:
                direction_down = True
            elif row == num_rows - 1:
                direction_down = False
            row += 1 if direction_down else -1

        # Fill the rail with cipher text
        index = 0
        for i in range(num_rows):
            for j in range(len(cipher_text)):
                if rail[i][j] == '*' and index < len(cipher_text):
                    rail[i][j] = cipher_text[index]
                    index += 1

        # Read the zigzag pattern to reconstruct plaintext
        result = []
        row, col = 0, 0
        for _ in range(len(cipher_text)):
            result.append(rail[row][col])
            col += 1
            if row == 0:
                direction_down = True
            elif row == num_rows - 1:
                direction_down = False
            row += 1 if direction_down else -1

        # Display the result in the output textbox
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", ''.join(result))

    
    def encryption_reil_cipher(self):
        # Retrieve input text and number of rows
        plain_text = self.input_textbox.get("1.0", "end").strip()  # Get text from the textbox
        plain_text = plain_text.replace(" ", "")  # Remove all spaces from the text
        num_rows = int(self.railrows_entry.get())  # Get the number of rows from entry

        # Validate inputs
        if not plain_text or num_rows <= 1:
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", "Invalid input! Ensure text is not empty and rows > 1.")
            return

        # Initialize the rail fence
        rail = [['' for _ in range(len(plain_text))] for _ in range(num_rows)]

        # Create the zigzag pattern
        direction_down = False
        row, col = 0, 0
        for char in plain_text:
            rail[row][col] = char
            col += 1
            if row == 0 or row == num_rows - 1:
                direction_down = not direction_down
            row += 1 if direction_down else -1

        # Read the cipher text row by row
        cipher_text = ''
        for i in range(num_rows):
            for j in range(len(plain_text)):
                if rail[i][j] != '':
                    cipher_text += rail[i][j]

        # Display the result in the output textbox
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", cipher_text)

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Brute Force Cipher--------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
    
    def decryption_brute_force(self):
        encrypted_text = self.input_textbox.get("1.0", tk.END).strip()

        # Check if input is empty
        if not encrypted_text:
            self.output_textbox.insert(tk.END, "Error: No encrypted text provided.")
            return

        # Try all key values for Caesar Cipher (0 to -25)
        possible_decryptions = []
        for key in range(0, -26, -1):  # Key values from 0 to -25
            current_decryption = ""  # Store the result of each decryption attempt
            for char in encrypted_text:
                if char.isalpha():
                    offset = 65 if char.isupper() else 97
                    # Decrypt the character by shifting backward by the key
                    decrypted_char = chr((ord(char) - offset + key) % 26 + offset)
                    current_decryption += decrypted_char
                else:
                    current_decryption += char
            possible_decryptions.append(f"Key {key}: {current_decryption}\n")

        # Display the brute-force results
        self.output_textbox.insert(tk.END, "Brute Force Decryptions:\n")
        self.output_textbox.insert(tk.END, "".join(possible_decryptions))


    
    def encryption_brute_force(self):
        encrypted_text = self.input_textbox.get("1.0", tk.END).strip()

        # Check if input is empty
        if not encrypted_text:
            self.output_textbox.insert(tk.END, "Error: No encrypted text provided.")
            return

        # Try all key values for Caesar Cipher (0 to 25)
        possible_encryptions = []
        for key in range(26):
            current_encryption = ""  # Store the result of each encryption attempt
            for char in encrypted_text:
                if char.isalpha():
                    offset = 65 if char.isupper() else 97
                    # Encrypt the character by shifting forward by the key
                    encrypted_char = chr((ord(char) - offset + key) % 26 + offset)
                    current_encryption += encrypted_char
                else:
                    current_encryption += char
            possible_encryptions.append(f"Key {key}: {current_encryption}\n")

        # Display the brute-force results
        self.output_textbox.insert(tk.END, "Brute Force Encryptions:\n")
        self.output_textbox.insert(tk.END, "".join(possible_encryptions))

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Monoalphabetic Cipher-----------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

    def encryption_monoalphabetic_cipher(self):
        # Get the input text (plain text) from the input_textbox
        plaintext = self.input_textbox.get("1.0", "end").strip()

        # Create a dictionary mapping from 'A-Z' to the cipher alphabet (from the field)
        cipher_alphabet = [field.get() for field in self.fields]  # Get ciphered letters from the fields
        cipher_dict = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", cipher_alphabet))  # Map A-Z to shuffled ciphered letters

        # Encrypt the plaintext using the cipher dictionary
        cipher_text = ""
        for char in plaintext:
            if char.upper() in cipher_dict:
                ciphered_char = cipher_dict[char.upper()]
                # Maintain the original case of the letter
                if char.islower():
                    cipher_text += ciphered_char.lower()
                else:
                    cipher_text += ciphered_char
            else:
                cipher_text += char  # Non-alphabet characters remain unchanged

        # Display the cipher-text in the output_textbox
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", cipher_text)


    def decryption_monoalphabetic_cipher(self):
        # Get the input text (cipher-text) from the output_textbox
        ciphertext = self.input_textbox.get("1.0", "end").strip()

        # Create a dictionary mapping from the cipher alphabet back to 'A-Z'
        cipher_alphabet = [field.get() for field in self.fields]  # Get ciphered letters from the fields
        decrypt_dict = dict(zip(cipher_alphabet, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))  # Map shuffled letters back to A-Z

        # Decrypt the cipher-text using the decrypt dictionary
        decrypted_text = ""
        for char in ciphertext:
            if char.upper() in decrypt_dict:
                decrypted_char = decrypt_dict[char.upper()]
                # Maintain the original case of the letter
                if char.islower():
                    decrypted_text += decrypted_char.lower()
                else:
                    decrypted_text += decrypted_char
            else:
                decrypted_text += char  # Non-alphabet characters remain unchanged

        # Display the decrypted text in the output_textbox
        self.output_textbox.delete("1.0", "end")
        self.output_textbox.insert("1.0", decrypted_text)

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------


    
    
#---------------------------------------------------------------------------------------------------------------------------------------
#-------------PlayFair Cipher-----------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

    def encryption_playfair_cipher(self):
        # Get the plaintext input from the input textbox, removing leading/trailing whitespace
        plaintext = self.input_textbox.get("1.0", "end").strip()

        # Get the keyword from the keyword entry field, removing leading/trailing whitespace
        key = self.keyword_entry.get().strip()

        # Generate a 5x5 key square using the given key
        key_square = self.generate_key_square(key)

        # Prepare the plaintext for encryption (e.g., making it suitable for Playfair cipher rules)
        plaintext = self.prepare_text(plaintext)

        # Initialize an empty string to store the resulting ciphertext
        ciphertext = ""

        # Iterate over the plaintext in pairs of two characters
        for i in range(0, len(plaintext), 2):
            # Extract the current pair of characters
            a, b = plaintext[i], plaintext[i + 1]

            # Find the row and column of the first character in the key square
            row_a, col_a = self.find_position(key_square, a)

            # Find the row and column of the second character in the key square
            row_b, col_b = self.find_position(key_square, b)

            # If the characters are in the same row, replace each with the character to its right
            if row_a == row_b:  # Same row
                ciphertext += key_square[row_a][(col_a + 1) % 5]  # Wrap around to the beginning if at the end
                ciphertext += key_square[row_b][(col_b + 1) % 5]

            # If the characters are in the same column, replace each with the character below it
            elif col_a == col_b:  # Same column
                ciphertext += key_square[(row_a + 1) % 5][col_a]  # Wrap around to the top if at the bottom
                ciphertext += key_square[(row_b + 1) % 5][col_b]

            # If the characters form a rectangle, replace each with the character in the same row but opposite corner
            else:  # Rectangle
                ciphertext += key_square[row_a][col_b]
                ciphertext += key_square[row_b][col_a]

        # Clear the output textbox before displaying the result
        self.output_textbox.delete("1.0", "end")

        # Insert the ciphertext into the output textbox
        self.output_textbox.insert("1.0", ciphertext)

    def decryption_playfair_cipher(self):
        # Get the ciphertext input from the input textbox, removing leading/trailing whitespace
        ciphertext = self.input_textbox.get("1.0", "end").strip()

        # Get the keyword from the keyword entry field, removing leading/trailing whitespace
        key = self.keyword_entry.get().strip()

        # Generate a 5x5 key square using the given key
        key_square = self.generate_key_square(key)

        # Initialize an empty string to store the resulting plaintext
        plaintext = ""

        # Iterate over the ciphertext in pairs of two characters
        for i in range(0, len(ciphertext), 2):
            # Extract the current pair of characters
            a, b = ciphertext[i], ciphertext[i + 1]

            # Find the row and column of the first character in the key square
            row_a, col_a = self.find_position(key_square, a)

            # Find the row and column of the second character in the key square
            row_b, col_b = self.find_position(key_square, b)

            # If the characters are in the same row, replace each with the character to its left
            if row_a == row_b:  # Same row
                plaintext += key_square[row_a][(col_a - 1) % 5]  # Wrap around to the end if at the start
                plaintext += key_square[row_b][(col_b - 1) % 5]

            # If the characters are in the same column, replace each with the character above it
            elif col_a == col_b:  # Same column
                plaintext += key_square[(row_a - 1) % 5][col_a]  # Wrap around to the bottom if at the top
                plaintext += key_square[(row_b - 1) % 5][col_b]

            # If the characters form a rectangle, replace each with the character in the same row but opposite corner
            else:  # Rectangle
                plaintext += key_square[row_a][col_b]
                plaintext += key_square[row_b][col_a]

        # Clear the output textbox before displaying the result
        self.output_textbox.delete("1.0", "end")

        # Insert the plaintext into the output textbox
        self.output_textbox.insert("1.0", plaintext)

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------------------------------
#-------------One Time Pad Cipher-------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

    
    def encryption_one_time_pad(self):
        # Retrieve plaintext and key from the input fields
        plaintext = self.input_textbox.get("1.0", "end").strip().upper()  # Convert to uppercase
        key = self.keyword_entry.get().strip().upper()       # Convert to uppercase

        # Check if the plaintext and key lengths match
        if len(plaintext) != len(key):
            self.output_textbox.delete("1.0", "end")  # Clear the output
            self.output_textbox.insert("1.0", "Error: Plaintext and key must be the same length.")
            return

        # Initialize encrypted text
        encrypted_text = ""

        # Perform one-time pad encryption
        for p_char, k_char in zip(plaintext, key):
            # Convert characters to numbers (A=0, B=1, ..., Z=25)
            p_num = ord(p_char) - ord('A')
            k_num = ord(k_char) - ord('A')

            # Add numbers and take modulo 26
            encrypted_num = (p_num + k_num) % 26

            # Convert back to character
            encrypted_char = chr(encrypted_num + ord('A'))

            # Append to encrypted text
            encrypted_text += encrypted_char

        # Display the result in the output textbox
        self.output_textbox.delete("1.0", "end")  # Clear the output box
        self.output_textbox.insert("1.0", encrypted_text)



    def decryption_one_time_pad(self):
        # Retrieve ciphertext and key from the input fields
        ciphertext = self.input_textbox.get("1.0", "end").strip().upper()  # Convert to uppercase
        key = self.keyword_entry.get().strip().upper()  # Convert to uppercase

        # Check if the ciphertext and key lengths match
        if len(ciphertext) != len(key):
            self.output_textbox.delete("1.0", "end")  # Clear the output
            self.output_textbox.insert("1.0", "Error: Ciphertext and key must be the same length.")
            return

        # Initialize decrypted text
        decrypted_text = ""

        # Perform one-time pad decryption
        for c_char, k_char in zip(ciphertext, key):
            # Convert characters to numbers (A=0, B=1, ..., Z=25)
            c_num = ord(c_char) - ord('A')
            k_num = ord(k_char) - ord('A')

            # Subtract key from ciphertext and take modulo 26
            decrypted_num = (c_num - k_num) % 26

            # Convert back to character
            decrypted_char = chr(decrypted_num + ord('A'))

            # Append to decrypted text
            decrypted_text += decrypted_char

        # Display the result in the output textbox
        self.output_textbox.delete("1.0", "end")  # Clear the output box
        self.output_textbox.insert("1.0", decrypted_text)

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Vigenere Cipher-----------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

    def encryption_vigenere_cipher(self):
        plaintext = self.input_textbox.get("1.0", tk.END).strip()
        key = self.keyword_entry.get().strip()
        
        if not plaintext or not key:
            self.output_textbox.delete("1.0", tk.END)
            self.output_textbox.insert(tk.END, "Error: Plaintext or key cannot be empty.")
            return
        
        key = self.generate_key(plaintext, key)
        encrypted_text = ""
        
        for p, k in zip(plaintext, key):
            if p.isalpha():
                shift = (ord(p.upper()) + ord(k.upper())) % 26
                new_char = chr(shift + ord('A')) if p.isupper() else chr(shift + ord('a'))
                encrypted_text += new_char
            else:
                encrypted_text += p  # Keep non-alphabet characters unchanged
        
        self.output_textbox.delete("1.0", tk.END)  # Clear any existing content in the output textbox
        self.output_textbox.insert(tk.END, encrypted_text)  # Display the encrypted text

    def decryption_vigenere_cipher(self):
        # Get the ciphertext and key from their respective textboxes
        ciphertext = self.input_textbox.get("1.0", tk.END).strip()
        key = self.keyword_entry.get().strip()

        # Check for empty inputs and display an error if either is empty
        if not ciphertext or not key:
            self.output_textbox.delete("1.0", tk.END)  # Clear the output textbox
            self.output_textbox.insert("1.0", "Error: Ciphertext or key cannot be empty.")
            return

        # Generate the extended key to match the ciphertext length
        key = self.generate_key(ciphertext, key)
        decrypted_text = ""

        # Perform the decryption process
        for c, k in zip(ciphertext, key):
            if c.isalpha():
                shift = (ord(c.upper()) - ord(k.upper()) + 26) % 26
                new_char = chr(shift + ord('A')) if c.isupper() else chr(shift + ord('a'))
                decrypted_text += new_char
            else:
                decrypted_text += c  # Keep non-alphabet characters unchanged

        # Display the decrypted text in the output textbox
        self.output_textbox.delete("1.0", tk.END)  # Clear any existing text
        self.output_textbox.insert("1.0", decrypted_text)

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------


    
#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Caesar Cipher-------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
    
    def encryption_caesar_cipher(self):
        # Get the plain text input from the input_textbox
        plain_text = self.input_textbox.get("1.0", tk.END)  # Get all text from the beginning to the end

        # Remove any extra newline character at the end of the text (added by tk.END)
        plain_text = plain_text.strip()

        # Get the key from key_entry (ensure the key is an integer)
        try:
            key = int(self.key_entry.get())
        except ValueError:
            self.output_textbox.delete(1.0, "end")
            self.output_textbox.insert("end", "Invalid key. Please enter an integer.")
            return

        encrypted_text = ""

        # Iterate over each character in the plain text
        for char in plain_text:
            if char.isalpha():
                # Handle upper and lower case letters
                offset = 65 if char.isupper() else 97
                encrypted_char = chr((ord(char) - offset + key) % 26 + offset)
                encrypted_text += encrypted_char
            else:
                # Non-alphabetic characters remain unchanged
                encrypted_text += char

        # Display the encrypted text in output_textbox
        self.output_textbox.delete(1.0, "end")  # Clear previous output
        self.output_textbox.insert("end", encrypted_text)

    
    def decryption_caesar_cipher(self):
        # Get the encrypted text input from the input_textbox
        encrypted_text = self.input_textbox.get("1.0", tk.END)  # Get all text from the beginning to the end

        # Remove any extra newline character at the end of the text (added by tk.END)
        encrypted_text = encrypted_text.strip()

        # Get the key from key_entry (ensure the key is an integer)
        try:
            key = int(self.key_entry.get())
        except ValueError:
            self.output_textbox.delete(1.0, "end")
            self.output_textbox.insert("end", "Invalid key. Please enter an integer.")
            return

        decrypted_text = ""

        # Iterate over each character in the encrypted text
        for char in encrypted_text:
            if char.isalpha():
                # Handle upper and lower case letters
                offset = 65 if char.isupper() else 97
                decrypted_char = chr((ord(char) - offset - key) % 26 + offset)  # Subtract key for decryption
                decrypted_text += decrypted_char
            else:
                # Non-alphabetic characters remain unchanged
                decrypted_text += char

        # Display the decrypted text in output_textbox
        self.output_textbox.delete(1.0, "end")  # Clear previous output
        self.output_textbox.insert("end", decrypted_text)

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------------------------------
#-------------Hashing (SHA256 / MD5)----------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

    def hashing_SHA_256(self):
        # Retrieve input text
        plain_text = self.input_textbox.get("1.0", tk.END)

        # Generate SHA-256 hash
        sha256_hash = hashlib.sha256(plain_text.encode()).hexdigest()

        # Display the hash in the output textbox
        
        self.output_textbox.delete(1.0, "end")  # Clear any existing text
        self.output_textbox.insert("end", sha256_hash)  # Insert the hash value
   
    
    def hashing_MD5(self):
        # Retrieve input text
        plain_text = self.input_textbox.get("1.0", tk.END)

        # Generate MD5 hash
        md5_hash = hashlib.md5(plain_text.encode()).hexdigest()

        # Display the hash in the output textbox
        
        self.output_textbox.delete(1.0, "end")  # Clear any existing text
        self.output_textbox.insert("end", md5_hash)  # Insert the hash value

#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------
        


# Running the application
root = tk.Tk()
app = CipherInterface(root)
root.mainloop()