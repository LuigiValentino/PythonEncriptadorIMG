import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import base64
from PIL import Image, ImageTk
import io

def is_base64(s):
    try:
        s_bytes = s.encode('utf-8') if isinstance(s, str) else s
        return base64.b64encode(base64.b64decode(s_bytes)) == s_bytes
    except Exception:
        return False

def encode_image_to_string(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        messagebox.showerror("Error", f"Failed to encode the image: {e}")
        return None

def decode_string_to_image(encoded_string, output_path):
    try:
        if is_base64(encoded_string):
            image_data = base64.b64decode(encoded_string)
            with open(output_path, "wb") as output_file:
                output_file.write(image_data)
            messagebox.showinfo("Success", f"Image saved as {output_path}")
        else:
            messagebox.showerror("Error", "The provided text is not a valid Base64 string.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode the image: {e}")

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        encoded_string = encode_image_to_string(file_path)
        if encoded_string:
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, encoded_string)
            show_image(file_path)

def load_encoded_text():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as text_file:
                encoded_string = text_file.read()
                text_box.delete(1.0, tk.END)
                text_box.insert(tk.END, encoded_string)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the encoded text: {e}")

def save_encoded_text():
    encoded_string = text_box.get(1.0, tk.END).strip()
    if encoded_string:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as text_file:
                    text_file.write(encoded_string)
                messagebox.showinfo("Success", f"Encoded text saved as {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the encoded text: {e}")
    else:
        messagebox.showwarning("Warning", "No encoded string found in the text box!")

def save_decoded_image():
    encoded_string = text_box.get(1.0, tk.END).strip()
    if encoded_string:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            decode_string_to_image(encoded_string, file_path)
    else:
        messagebox.showwarning("Warning", "No encoded string found in the text box!")

def copy_to_clipboard():
    root.clipboard_clear() 
    root.clipboard_append(text_box.get(1.0, tk.END))  
    messagebox.showinfo("Copied", "Texto copiado al portapapeles.")

def show_image(image_path, max_size=(200, 200)):
    try:
        image = Image.open(image_path)
        image.thumbnail(max_size, Image.LANCZOS) 
        image_tk = ImageTk.PhotoImage(image)
        image_label.config(image=image_tk)
        image_label.image = image_tk
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load the image: {e}")

root = ThemedTk(theme="equilux")
root.title("Encriptador de Imágenes")
root.geometry("500x550")
root.configure(bg='#2C2F33')  

title_label = ttk.Label(root, text="Encriptador y Desencriptador de Imágenes", font=("Helvetica", 16, "bold"), background='#2C2F33', foreground='white')
title_label.pack(pady=20)

main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.pack(fill=tk.BOTH, expand=True)

encryption_frame = ttk.Labelframe(main_frame, text="Encriptar Imagen", padding="10 10 10 10")
encryption_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

browse_button = ttk.Button(encryption_frame, text="Cargar Imagen", command=browse_image)
browse_button.grid(row=0, column=0, padx=5, pady=5)

save_text_button = ttk.Button(encryption_frame, text="Guardar Texto Encriptado", command=save_encoded_text)
save_text_button.grid(row=1, column=0, padx=5, pady=5)

decryption_frame = ttk.Labelframe(main_frame, text="Desencriptar Texto", padding="10 10 10 10")
decryption_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

load_text_button = ttk.Button(decryption_frame, text="Cargar Texto Encriptado", command=load_encoded_text)
load_text_button.grid(row=0, column=0, padx=5, pady=5)

save_button = ttk.Button(decryption_frame, text="Guardar Imagen Desencriptada", command=save_decoded_image)
save_button.grid(row=1, column=0, padx=5, pady=5)

text_box = tk.Text(main_frame, wrap="word", height=7, width=50, bg='#444', fg='white', insertbackground='white')
text_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

copy_button = ttk.Button(main_frame, text="Copiar", command=copy_to_clipboard)
copy_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

image_label = ttk.Label(main_frame)
image_label.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
