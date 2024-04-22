from tkinter import *
import time
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk, ImageFont, ImageDraw

# ---------------------------- CONSTANTS ------------------------------- #

BEIGE = "#EADFB4"
LIGHT_BLUE = "#9BB0C1"
BLUE = "#51829B"
ORANGE = "#F6995C"
FONT_NAME = "Arial"


# ---------------------------- FUNCTIONS ------------------------------- #

def upload_image():
    global image_file_path
    if image_file_path:
        # Open the image file
        image = Image.open(image_file_path)
        image = image.resize((200, 200), PIL.Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)

        # Create a canvas to display the image
        canvas = Canvas(window, width=image.width, height=image.height, bg=BEIGE, highlightthickness=0)
        canvas.create_image(0, 0, anchor='nw', image=img)

        # Keep a reference to the image to prevent garbage collection
        canvas.image = img
        canvas.grid(column=1, row=1)


def choose_filepath(event):
    """
    Opens a file dialog to allow the user to choose a file path and returns the selected file path, or an empty string
    if no file is selected.
    """
    global image_file_path
    selected_filepath = filedialog.askopenfilename()
    if selected_filepath:
        entry_field.delete(0, END)
        entry_field.insert(0, selected_filepath)
        image_file_path = selected_filepath


def add_watermark():
    # Get watermark text
    watermark_text = watermark_entry_field.get()

    # Get image and image size
    original_image = Image.open(image_file_path)
    width, height = original_image.size

    # Define the watermark font, color, and position
    font = ImageFont.truetype("static/assets/fonts/Newretrostyle3d-ygjm.ttf", 50)
    fill_color = (203, 201, 201)
    position = (width // 2 - 50, height // 2 - 50)

    # Draw the text
    drawing = ImageDraw.Draw(original_image)
    drawing.text(xy=position, text=watermark_text, font=font, fill=fill_color)

    # Convert the image to RGBA mode
    original_image = original_image.convert("RGB")

    original_image.save("./output/watermarked_image.jpg")

    watermarked_image = Image.open("./output/watermarked_image.jpg")

    # Convert the image to RGBA mode
    displayed_image = watermarked_image.convert("RGBA")

    # Resize the image for display
    displayed_image = displayed_image.resize((200, 200), Image.LANCZOS)

    # Convert the resized image to a Tkinter-compatible format
    displayed_watermark_img = ImageTk.PhotoImage(displayed_image)

    # Create a canvas to display the image
    canvas = Canvas(window, width=300, height=300, bg=BEIGE, highlightthickness=0)
    canvas.create_image(0, 0, anchor='nw', image=displayed_watermark_img)
    canvas.grid(column=2, row=1)

    # Keep a reference to the image to prevent garbage collection
    canvas.displayed_watermark_img = displayed_watermark_img


# ---------------------------- UI SETUP ------------------------------- #

# CREATE A WINDOW
window = Tk()
window.title("Image Watermark")
window.config(padx=50, pady=50, bg=BEIGE)

# CREATE HEADER LABEL
heading = Label(text="Add Watermark To Your Image", fg=BLUE, bg=BEIGE, font=(FONT_NAME, 35, "bold"))
heading.grid(column=1, row=0, columnspan=4, pady=50)

# CREATE ENTRY FIELD FOR CHOOSING THE FILE PATH
entry_field = Entry(window, width=50)
entry_field.grid(row=2, column=1, padx=10, pady=10)

# Bind the upload_image function to the entry field
entry_field.bind("<Button-1>", choose_filepath)

# UPLOAD BUTTON
image_upload_button = Button(window, command=upload_image, text="Upload")
image_upload_button.grid(column=2, row=2)

# CREATE ENTRY FIELD FOR WATERMARK TEXT
watermark_entry_field = Entry(window, width=50)
watermark_entry_field.grid(row=3, column=1, padx=10, pady=10)

# ADD WATERMARK BUTTON
add_watermark_button = Button(window, command=add_watermark, text="Add Watermark")
add_watermark_button.grid(column=2, row=3)

window.mainloop()