from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo, showerror
import os
import cv2
from functions import ImageFunctions
from cropImage import Crop

global img
global filename
global image_functions
global new_img
global img_count


def check_img_exists():

    global img
    try:
        if img is not None:
            return True
    except NameError:
        print("Please select an image first!")
        return False


# Functions
def select_file():
    filetypes = (('Image Files', '*.jpg; *.jpeg; *.png'), ('All files', '*.*'))
    global filename
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    # show image
    if filename != "":
        global img
        img = Image.open(filename)
        resized_image = img.resize((675, 450))
        img1 = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, anchor=NW, image=img1)
        canvas.image = img1
        showinfo(title='Selected File', message='Image loaded successfully!')
    global image_functions
    image_functions = ImageFunctions(filename)


def approve_func():

    if check_img_exists() is True:

        global img_count
        docname = filename.split('/')[len(filename.split('/')) - 1].split('.')[0]
        new_img.save("Uploads/" + docname + "_edited" + str(img_count) + ".jpg")
        showinfo(title='Success', message="Image successfully saved.")
        img_count += 1

    else:

        showerror(title="Error", message="Please load an image to save!")


def blurring_popup():

    if check_img_exists() is True:

        window = Toplevel()
        window.title("Blur/Deblur Image")
        window.geometry("250x150")

        window_label = Label(window, text="Please select the blurring type:")
        window_label.pack(anchor=W)

        var = StringVar()

        Radiobutton(window, text="Simple", variable=var, value="simple").pack(anchor=W)
        Radiobutton(window, text="Box", variable=var, value="box").pack(anchor=W)
        Radiobutton(window, text="Gaussian", variable=var, value="gaussian").pack(anchor=W)

        ok_button = Button(window, text="OK", bg="#8bfcf9", command=window.destroy)
        ok_button.pack(anchor='center')

        app.wait_window(window)
        blurred_img = image_functions.blur_Image(var.get())
        blurred = blurred_img.resize((675, 450))
        blurred = ImageTk.PhotoImage(blurred)
        canvas2.create_image(0, 0, anchor=NW, image=blurred)
        canvas2.image = blurred
        global new_img
        new_img = blurred_img

    else:
        showerror(title="Error", message="Please select an image first!")


def deblurring():

    if check_img_exists() is True:
        deblurred = image_functions.deblur_Image()
        deblurred = deblurred.resize((675, 450))
        sharpened = ImageTk.PhotoImage(deblurred)
        canvas2.create_image(0, 0, anchor=NW, image=sharpened)
        canvas2.image = sharpened
        global new_img
        new_img = deblurred

    else:
        showerror(title="Error", message="Please select an image first!")


def grayscale_img():

    if check_img_exists() is True:
        gray_img = img.convert("L")
        gray_img = gray_img.resize((675, 450))
        gray = ImageTk.PhotoImage(gray_img)
        canvas2.create_image(0, 0, anchor=NW, image=gray)
        canvas2.image = gray
        global new_img
        new_img = gray_img

    else:
        showerror(title="Error", message="Please select an image first!")


def adj_brightness():

    if check_img_exists() is True:
        window = Toplevel()
        window.title("Adjust Brightness")
        window.geometry("300x150")

        var = IntVar()

        factor_label = Label(window, text='Factor: ', font=('calibre', 10, 'bold'))
        factor_entry = Entry(window, textvariable=var, font=('calibre', 10, 'normal'))

        factor_label.grid(row=0, column=0, padx=20, pady=40)
        factor_entry.grid(row=0, column=1, pady=40, sticky="ew")

        ok_button = Button(window, text="OK", bg="#8bfcf9", command=window.destroy, width=15)
        ok_button.grid(row=1, column=0, columnspan=2)

        app.wait_window(window)
        bright_img = image_functions.adjust_brightness(var.get())
        bright_img = bright_img.resize((675, 450))
        bright = ImageTk.PhotoImage(bright_img)
        canvas2.create_image(0, 0, anchor=NW, image=bright)
        canvas2.image = bright
        global new_img
        new_img = bright_img

    else:
        showerror(title="Error", message="Please select an image first!")


def adj_saturation():

    if check_img_exists() is True:
        window = Toplevel()
        window.title("Adjust Saturation")
        window.geometry("300x150")

        var = IntVar()

        factor_label = Label(window, text='Factor: ', font=('calibre', 10, 'bold'))
        factor_entry = Entry(window, textvariable=var, font=('calibre', 10, 'normal'))

        factor_label.grid(row=0, column=0, padx=20, pady=40)
        factor_entry.grid(row=0, column=1, pady=40, sticky="ew")

        ok_button = Button(window, text="OK", bg="#8bfcf9", command=window.destroy, width=15)
        ok_button.grid(row=1, column=0, columnspan=2)

        app.wait_window(window)
        sat_img = image_functions.adjust_saturation(var.get())
        sat_img = sat_img.resize((675, 450))
        sat = ImageTk.PhotoImage(sat_img)
        canvas2.create_image(0, 0, anchor=NW, image=sat)
        canvas2.image = sat
        global new_img
        new_img = sat_img

    else:
        showerror(title="Error", message="Please select an image first!")


def adj_contrast():

    if check_img_exists() is True:
        window = Toplevel()
        window.title("Adjust Contrast")
        window.geometry("300x150")

        var = IntVar()

        factor_label = Label(window, text='Factor: ', font=('calibre', 10, 'bold'))
        factor_entry = Entry(window, textvariable=var, font=('calibre', 10, 'normal'))

        factor_label.grid(row=0, column=0, padx=20, pady=40)
        factor_entry.grid(row=0, column=1, pady=40, sticky="ew")

        ok_button = Button(window, text="OK", bg="#8bfcf9", command=window.destroy, width=15)
        ok_button.grid(row=1, column=0, columnspan=2)

        app.wait_window(window)
        contrast_img = image_functions.adjust_contrast(var.get())
        contrast_img = contrast_img.resize((675, 450))
        cont = ImageTk.PhotoImage(contrast_img)
        canvas2.create_image(0, 0, anchor=NW, image=cont)
        canvas2.image = cont
        global new_img
        new_img = contrast_img

    else:
        showerror(title="Error", message="Please select an image first!")


def noise_popup():

    if check_img_exists() is True:
        window = Toplevel()
        window.title("Add Noise")
        window.geometry("300x150")

        window_label = Label(window, text="Please select the noise type:")
        window_label.pack(anchor=W)

        var = StringVar()

        Radiobutton(window, text="Gauss", variable=var, value="gauss").pack(anchor=W)
        Radiobutton(window, text="Speckle", variable=var, value="speckle").pack(anchor=W)
        ok_button = Button(window, text="OK", bg="#8bfcf9", command=window.destroy)
        ok_button.pack(anchor='center')

        app.wait_window(window)
        noised_img = image_functions.add_noise(var.get())
        pil_img = cv2.cvtColor(noised_img, cv2.COLOR_BGR2RGB)
        noisy = Image.fromarray(pil_img)
        noisy = noisy.resize((675, 450))
        noisy = ImageTk.PhotoImage(noisy)
        canvas2.create_image(0, 0, anchor=NW, image=noisy)
        canvas2.image = noisy
        global new_img
        new_img = noisy

    else:
        showerror(title="Error", message="Please select an image first!")


def edge_detection():

    if check_img_exists() is True:
        edges = image_functions.detect_edges()
        edges = edges.resize((675, 450))
        img_edges = ImageTk.PhotoImage(edges)
        canvas2.create_image(0, 0, anchor=NW, image=img_edges)
        canvas2.image = img_edges
        global new_img
        new_img = edges
    else:
        showerror(title="Error", message="Please select an image first!")


def color_reverse():

    if check_img_exists() is True:
        reversed_color = image_functions.reverse_color()
        reversed_color = reversed_color.resize((675, 450))
        reversed_img = ImageTk.PhotoImage(reversed_color)
        canvas2.create_image(0, 0, anchor=NW, image=reversed_img)
        canvas2.image = reversed_img
        global new_img
        new_img = reversed_color
    else:
        showerror(title="Error", message="Please select an image first!")


def mirror():

    if check_img_exists() is True:
        mirror_img = image_functions.mirror_image()
        mirror_img = mirror_img.resize((675, 450))
        mirrored = ImageTk.PhotoImage(mirror_img)
        canvas2.create_image(0, 0, anchor=NW, image=mirrored)
        canvas2.image = mirrored
        global new_img
        new_img = mirror_img
    else:
        showerror(title="Error", message="Please select an image first!")


def color_balance():

    if check_img_exists() is True:
        window = Toplevel()
        window.title("Change Color Balance")
        window.geometry("300x150")

        var = IntVar()

        value_label = Label(window, text='Value: ', font=('calibre', 10, 'bold'))
        value_entry = Entry(window, textvariable=var, font=('calibre', 10, 'normal'))

        value_label.grid(row=0, column=0, padx=20, pady=40)
        value_entry.grid(row=0, column=1, pady=40, sticky="ew")

        ok_button = Button(window, text="OK", bg="#8bfcf9", command=window.destroy, width=15)
        ok_button.grid(row=1, column=0, columnspan=2)

        app.wait_window(window)
        balanced_img = image_functions.change_color_balance(var.get())
        balanced_img = balanced_img.resize((675, 450))
        col_bal = ImageTk.PhotoImage(balanced_img)
        canvas2.create_image(0, 0, anchor=NW, image=col_bal)
        canvas2.image = col_bal
        global new_img
        new_img = balanced_img

    else:
        showerror(title="Error", message="Please select an image first!")


def cropping():

    if check_img_exists() is True:
        global filename
        to_be_cropped = Image.open(filename)
        crop_window = Toplevel()
        # showinfo(title="Information", message="Press 'Esc' to change the selected area")
        w = int(crop_window.winfo_screenwidth()*0.8)
        h = int(crop_window.winfo_screenheight()*0.8)
        c = Crop(crop_window, to_be_cropped, w, h, [])

        app.wait_window(crop_window)

        area_coords = c.__repr__()
        to_be_cropped = to_be_cropped.resize((w, h))
        to_be_cropped = to_be_cropped.crop((area_coords[0], area_coords[1], area_coords[2], area_coords[3]))
        cropped = ImageTk.PhotoImage(to_be_cropped)
        canvas2.create_image(0, 0, anchor=NW, image=cropped)
        canvas2.image = cropped
        global new_img
        new_img = to_be_cropped
    else:
        showerror(title="Error", message="Please select an image first!")


def flip():

    if check_img_exists() is True:
        window = Toplevel()
        window.title("Flip Image")
        window.geometry("250x150")

        window_label = Label(window, text="Please select the flip type:")
        window_label.pack(anchor=W)

        var = StringVar()

        Radiobutton(window, text="Horizontal", variable=var, value="horizontal").pack(anchor=W)
        Radiobutton(window, text="Vertical", variable=var, value="vertical").pack(anchor=W)
        Radiobutton(window, text="Clockwise", variable=var, value="clockwise").pack(anchor=W)
        Radiobutton(window, text="Anticlockwise", variable=var, value="anticlockwise").pack(anchor=W)

        ok_button = Button(window, text="OK", bg="#8bfcf9", command=window.destroy, width=15)
        ok_button.pack(anchor='center')

        app.wait_window(window)
        flipped_im = image_functions.flip_Image(var.get())
        if var.get() == "clockwise" or var.get() == "anticlockwise":
            new_width = (flipped_im.size[0] * canvas_height) // flipped_im.size[1]
            flipped_img = flipped_im.resize((new_width, 450))
            flipped = ImageTk.PhotoImage(flipped_img)
            canvas2.create_image(0, 0, anchor=NW, image=flipped)
            canvas2.image = flipped

        else:
            flipped_img = flipped_im.resize((675, 450))
            flipped = ImageTk.PhotoImage(flipped_img)
            canvas2.create_image(0, 0, anchor=NW, image=flipped)
            canvas2.image = flipped

        global new_img
        new_img = flipped_img

    else:
        showerror(title="Error", message="Please select an image first!")


def rotate():

    if check_img_exists() is True:
        window = Toplevel()
        window.title("Rotate Image")
        window.geometry("250x150")

        window_label = Label(window, text="Please select/enter the rotation degree:")
        window_label.grid(row=0, columnspan=3)

        var = IntVar()

        Radiobutton(window, text="90", variable=var, value=90).grid(row=1, column=1)
        Radiobutton(window, text="180", variable=var, value=180).grid(row=2, column=1)
        Radiobutton(window, text="270", variable=var, value=270).grid(row=3, column=1)
        Label(window, text="Or ..").grid(row=4, column=0)
        Entry(window, textvariable=var).grid(row=4, column=2)

        ok_button = Button(window, text="OK", bg="#8bfcf9", command=window.destroy, width=15)
        ok_button.grid(row=5, column=0, columnspan=3)

        app.wait_window(window)
        rotated_img = image_functions.rotate_Image(var.get())
        if var.get() == 180:
            rotated_img = rotated_img.resize((675, 450))
            rotated = ImageTk.PhotoImage(rotated_img)
            canvas2.create_image(0, 0, anchor=NW, image=rotated)
            canvas2.image = rotated
        elif var.get() == 90 or var.get() == 270:
            new_width = (rotated_img.size[0] * canvas_height) // rotated_img.size[1]
            rotated = rotated_img.resize((new_width, 450))
            rotated = ImageTk.PhotoImage(rotated)
            canvas2.create_image(0, 0, anchor=NW, image=rotated)
            canvas2.image = rotated
        else:
            new_width = (rotated_img.size[0] * canvas_height) // rotated_img.size[1]
            rotated_img = rotated_img.resize((new_width, 450))
            rotated = ImageTk.PhotoImage(rotated_img)
            canvas2.create_image(0, 0, anchor=NW, image=rotated)
            canvas2.image = rotated
        global new_img
        new_img = rotated_img

    else:
        showerror(title="Error", message="Please select an image first!")


# Create window object
app = Tk()
app.title('Image Editor')
app.state('zoomed')
app['bg'] = '#cce5ff'

# Tabs
tabControl = ttk.Notebook(app)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
style = ttk.Style()
style.configure('.', background="#cce5ff")

tabControl.add(tab1, text='About the Project')
tabControl.add(tab2, text='Image Edit')
tabControl.pack(expand=1, fill="both")

label_head = Label(tab1, text=" Welcome to Image Editor.. ", bg="#cce5ff",
                   font=('Comic Sans MS', 18))
label_head.pack()

label_info = Label(tab1,
                   text=" This image editor was developed by Ece Omurtay and Berfin Dinler together. \n"
                        "With this editor, you can apply any filter you want to any picture you want.\n\n"
                        "HOW TO USE?\n"
                        "- You can load the image you want to edit from the 'File' in the menu bar or with the 'Upload' button on the filter page. \n"
                        "- After uploading the photo, you can apply the filter you want from the menu bar.\n"
                        "- You can save the edited photo from 'File' in the menu bar or with the 'Save' button on the filter page.\n\n"
                        "Application Tip : You can apply as many filters as you want to a photo.\n"
                        "Crop Tip : Press 'Esc' to change the selected area. ",
                   bd=1,
                   font=('Comic Sans MS', 18),
                   bg="#cce5ff",
                   width=600,
                   height=400)
label_info.pack()

canvas_width, canvas_height = 675, 450

# Buttons
upload_button = Button(tab2, text='Upload Photo', command=select_file, width=12, fg="black", bg="white")
upload_button.grid(row=0, column=0, pady=20)

save_button = Button(tab2, text='Save Photo', command=approve_func, width=12, fg="black", bg="white")
save_button.grid(row=0, column=1, pady=20)

# Boxes
canvas = Canvas(tab2, width=canvas_width, height=canvas_height, bg='#80bbff', highlightthickness=1, borderwidth=0)
canvas.grid(row=1, column=0, padx=5, pady=80)

canvas2 = Canvas(tab2, width=canvas_width, height=canvas_height, bg='#80bbff', highlightthickness=1, borderwidth=0)
canvas2.grid(row=1, column=1, pady=80)

# MENU BAR
menu_bar = Menu(app)
app.config(menu=menu_bar)
# FILE MENU
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Load Image', command=select_file)
file_menu.add_command(label='Save Image', command=select_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=app.quit)
# EDIT MENU
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Edit', menu=edit_menu)

# Blur/Deblur menu
blur_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_cascade(label='Blur/Deblur Image', menu=blur_menu)
blur_menu.add_command(label='Blur Image', command=blurring_popup)
blur_menu.add_command(label='Deblur Image', command=deblurring)

edit_menu.add_command(label='Grayscale Image', command=grayscale_img)
edit_menu.add_command(label='Crop Image', command=cropping)
edit_menu.add_command(label='Flip Image', command=flip)
edit_menu.add_command(label='Mirror Image', command=mirror)
edit_menu.add_command(label='Rotate Image', command=rotate)
edit_menu.add_command(label='Reverse the color', command=color_reverse)
edit_menu.add_command(label='Change color balance', command=color_balance)

# Adjust functions menu
adjust_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_cascade(label='Adjust ...', menu=adjust_menu)
adjust_menu.add_command(label='Brightness', command=adj_brightness)
adjust_menu.add_command(label='Contrast', command=adj_contrast)
adjust_menu.add_command(label='Saturation', command=adj_saturation)

edit_menu.add_command(label='Add noise', command=noise_popup)
edit_menu.add_command(label='Detect edges', command=edge_detection)

# Create folder
if not os.path.exists('Uploads'):
    os.makedirs('Uploads')

img_count = 1
# Start program
app.mainloop()
