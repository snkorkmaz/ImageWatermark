import os
import shutil
from tkinter import *
import time
from tkinter import filedialog, ttk
from tkinter.ttk import Style

import PIL
from PIL import Image, ImageTk, ImageFont, ImageDraw
from customtkinter import CTkButton

# ---------------------------- CONSTANTS ------------------------------- #

BEIGE = "#EADFB4"
LIGHT_BLUE = "#9BB0C1"
BLUE = "#51829B"
ORANGE = "#F6995C"
FONT_NAME = "Arial"

# Initialize global variables for canvases and image icons
original_image_canvas = None
watermarked_image_canvas = None
download_image_button = None
img_icon = None


# ---------------------------- FUNCTIONS ------------------------------- #

def upload_image(img):
    global image_file_path, original_image_canvas
    if image_file_path:
        # Open the image file
        image = Image.open(image_file_path)
        image = image.resize((300, 300), PIL.Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)

        # Display original image
        original_image_canvas.delete("all")
        original_image_canvas.create_image(0, 0, anchor='nw', image=img)
        original_image_canvas.img = img  # Store reference to the image
        original_image_canvas.update()  # Update canvas
        if download_image_button:
            download_image_button.destroy()


def choose_filepath(event):
    """
    Opens a file dialog to allow the user to choose a file path and returns the selected file path, or an empty string
    if no file is selected.
    """
    global image_file_path
    selected_filepath = filedialog.askopenfilename()
    if selected_filepath:
        file_path_entry_field.delete(0, END)  # Remove text from entry when new image will be selected
        file_path_entry_field.insert(0, selected_filepath)  # Fill in file path
        image_file_path = selected_filepath  # Store filepath in a global variable to enable other function to use it


def add_watermark(img):
    # Get watermark text
    watermark_text = watermark_entry_field.get()

    # Get image and image size
    original_image = Image.open(image_file_path)
    width, height = original_image.size

    # Define the watermark font, color, and position
    font = ImageFont.truetype("static/assets/fonts/Newretrostyle3d-ygjm.ttf", 100)
    fill_color = (203, 201, 201)
    position = (width // 2 - 50, height // 2 - 50)

    # Draw the text
    drawing = ImageDraw.Draw(original_image)
    drawing.text(xy=position, text=watermark_text, font=font, fill=fill_color)

    # Convert the image to RGBA mode and save image
    original_image = original_image.convert("RGB")
    original_image.save("./output/watermarked_image.jpg")

    # Load the watermarked image
    """This step is necessary because to display the image, we need to resize it, and we do not want to chang the size 
    of the real image"""
    watermarked_image = Image.open("./output/watermarked_image.jpg")
    displayed_image = watermarked_image.convert("RGBA")  # Convert the image to RGBA mode
    displayed_image = displayed_image.resize((300, 300), Image.LANCZOS)  # Resize the image for display
    displayed_watermark_img = ImageTk.PhotoImage(displayed_image)  # Convert image to a Tkinter-compatible format

    # Display watermarked image
    watermarked_image_canvas.delete("all")  # Clear the canvas
    watermarked_image_canvas.create_image(0, 0, anchor='nw', image=displayed_watermark_img)  # store img in canvas
    watermarked_image_canvas.img = displayed_watermark_img  # Store reference to the image (Garbage Collection)
    watermarked_image_canvas.update()  # Update canvas

    # Keep a reference to the image to prevent garbage collection
    watermarked_image_canvas.displayed_watermark_img = displayed_watermark_img

    # DOWNLOAD IMAGE BUTTON
    download_image_button = CTkButton(window, command=download_image, text="Download Image")
    download_image_button.configure(text_color="white", fg_color=ORANGE, bg_color=BEIGE, hover_color=LIGHT_BLUE,
                                    corner_radius=50, width=220,
                                    font=(FONT_NAME, 15, "bold"))
    download_image_button.grid(row=2, column=2, pady=10)

    # Clear Entry Fields
    file_path_entry_field.delete(0, END)
    watermark_entry_field.delete(0, END)


def download_image():
    filename = os.path.basename("./output/watermarked_image.jpg") # Get filename from image path
    destination_dir = os.path.join(os.path.expanduser('~'), 'Downloads') # specify destination directory
    destination_file_path = os.path.join(destination_dir, filename) # Construct the destination file path
    shutil.copy2("./output/watermarked_image.jpg", destination_file_path) # Copy image to folder

    if download_image_button:
        download_image_button.destroy()

    download_successful_label = Label(text=f"Image downloaded to: Downloads", fg="white", bg=ORANGE, font=(FONT_NAME, 8))
    download_successful_label.grid(row=2, column=2)


# ---------------------------- UI SETUP ------------------------------- #

# CREATE A WINDOW
window = Tk()
window.title("Image Watermark")
window.geometry("900x800")
window.config(padx=25, pady=25, bg=BEIGE)

# CREATE CUSTOM STYLE FOR ENTRY WIDGET
style = Style()
style.configure('Custom.TEntry', bordercolor=BLUE, borderwidth=3, relief='solid', fieldbackground='white',
                foreground="black", padding=5, focuscolor=LIGHT_BLUE)

# CREATE HEADER LABEL
heading = Label(text="Add Watermark To Your Image", fg=BLUE, bg=BEIGE, font=(FONT_NAME, 35, "bold"))
heading.grid(column=1, row=0, columnspan=4, pady=50)

# CREATE IMAGE ICON
image_icon = Image.open("static/assets/img/img_icon.png")
image_icon = image_icon.resize((300, 300), PIL.Image.Resampling.LANCZOS)
img_icon = ImageTk.PhotoImage(image_icon)

# CREATE CANVAS TO DISPLAY img_icon AND ORIGINAL IMAGE
original_image_canvas = Canvas(window, width=300, height=300, bg=BEIGE, highlightthickness=0)
original_image_canvas.create_image(0, 0, anchor='nw', image=img_icon)
original_image_canvas.grid(column=1, row=1, pady=50)

# CREATE CANVAS TO DISPLAY img_icon AND WATERMARKED IMAGE
watermarked_image_canvas = Canvas(window, width=300, height=300, bg=BEIGE, highlightthickness=0)
watermarked_image_canvas.create_image(0, 0, anchor='nw', image=img_icon)
watermarked_image_canvas.grid(column=2, row=1, pady=50)

# CREATE ENTRY FIELD FOR CHOOSING THE FILE PATH
file_path_entry_field = ttk.Entry(window, width=50, style='Custom.TEntry')
file_path_entry_field.grid(row=3, column=1, padx=10, pady=10)

# BIND upload_image FUNCTION TO ENTRY FIELD
file_path_entry_field.bind("<Button-1>", choose_filepath)

# UPLOAD BUTTON
image_upload_button = CTkButton(window, command=lambda: upload_image(img_icon), text="Upload")
image_upload_button.configure(text_color="white", fg_color=BLUE, bg_color=BEIGE, hover_color=LIGHT_BLUE,
                              corner_radius=50, width=220,
                              font=(FONT_NAME, 15, "bold"))
image_upload_button.grid(row=3, column=2)

# CREATE ENTRY FIELD FOR WATERMARK TEXT
watermark_entry_field = ttk.Entry(window, width=50, style='Custom.TEntry')
watermark_entry_field.grid(row=4, column=1, padx=10, pady=10)

# ADD WATERMARK BUTTON
add_watermark_button = CTkButton(window, command=lambda: add_watermark(img_icon), text="Add Watermark")
add_watermark_button.configure(text_color="white", fg_color=BLUE, bg_color=BEIGE, hover_color=LIGHT_BLUE,
                               corner_radius=50, width=220,
                               font=(FONT_NAME, 15, "bold"))
add_watermark_button.grid(row=4, column=2)

window.mainloop()
