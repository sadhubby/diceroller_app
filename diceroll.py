from playsound import playsound
import tkinter
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import threading 

values = []
stat_values = {}

root = tkinter.Tk()
root.geometry('450x650')
root.resizable(False, False)
root.title('4d6')

# Frame to hold the header and the main content
header_frame = tkinter.Frame(root)
header_frame.pack(side="top", fill="both", expand=True)

# Header at the top
header_label = tkinter.Label(header_frame, text="4d6 Dice Roller", font="Helvetica 20 bold", pady=20)
header_label.pack()

# Main frame to hold the dice images
main_frame = tkinter.Frame(header_frame)
main_frame.pack(expand=True)

# Dictionary mapping images to integer values
d6 = {'images/side1.png': 1, 'images/side2.png': 2, 'images/side3.png': 3, 'images/side4.png': 4, 'images/side5.png': 5, 'images/side6.png': 6}
dice_sides = list(d6.keys())

# Load the question mark image
ques_image = Image.open("images/ques.png")
ques_image = ques_image.resize((90, 90))
ques_image = ImageTk.PhotoImage(ques_image)

# Create labels for each dice image and place them in the grid
label1 = tkinter.Label(main_frame, image=ques_image)
label1.image = ques_image   
label1.grid(row=0, column=0, padx=10, pady=15)

label2 = tkinter.Label(main_frame, image=ques_image)
label2.image = ques_image   
label2.grid(row=0, column=1, padx=10, pady=15)

label3 = tkinter.Label(main_frame, image=ques_image)
label3.image = ques_image   
label3.grid(row=0, column=2, padx=10, pady=15)

label4 = tkinter.Label(main_frame, image=ques_image)
label4.image = ques_image   
label4.grid(row=0, column=3, padx=10, pady=15)

def play():
    playsound('sound/diceroll.mp3') 

def animate_dice(label, dice_side, count, final_callback):
    if count > 0:
        dice_image = Image.open(dice_side)
        dice_image = dice_image.resize((90, 90))
        dice_image = ImageTk.PhotoImage(dice_image)
        label.configure(image=dice_image)
        label.image = dice_image
        next_side = random.choice(dice_sides)
        root.after(20, animate_dice, label, next_side, count-1, final_callback)
    else:
        final_image_file = random.choice(dice_sides)
        final_image = Image.open(final_image_file)
        final_image = final_image.resize((90, 90))
        final_image = ImageTk.PhotoImage(final_image)
        label.configure(image=final_image)
        label.image = final_image
        values.append(d6[final_image_file])
        if final_callback:
            final_callback()

def d6_roll():
    # clear the previous values
    values.clear()

    #callback function to update the labels after all dice have stopped rolling
    def update_results():
        number_label.configure(text=f"Roll results: {values}")
        sum_of_values.configure(text="Sum: " + str(drop_lowest(values)))

    # animate each dice label, chaining the final callback to the last dice animation
    animate_dice(label1, random.choice(dice_sides), 10, lambda: animate_dice(label2, random.choice(dice_sides), 10, lambda: animate_dice(label3, random.choice(dice_sides), 10, lambda: animate_dice(label4, random.choice(dice_sides), 10, update_results))))

def drop_lowest(values):
    if not values:  # handle the case where values might be empty
        return 0
    values_copy = values[:]
    min_value = min(values_copy)
    values_copy.remove(min_value)
    return sum(values_copy)

# Combobox 

def display_selection():
    values_copy = values[:]
    if not values_copy:
        messagebox.showerror(
            message=f"No stats rolled. Please roll first",
            title="Error"
        )
        return
    min_value = min(values_copy)
    values_copy.remove(min_value)
    selection_get=combo.get()
    sum_of_values = sum(values_copy)

    messagebox.showinfo(
        message=f"The selected value is: {selection_get} with {sum_of_values}",
        title = "Selection"
    )
    stat_values[selection_get] = sum_of_values
    
    current_values = list(combo['values'])

    current_values.remove(selection_get)

    combo['values'] = current_values

    combo.set("")

# messagebox if no more choices for combo, show all stat roll key-value pair
def message_done():

    dict_string = "\n".join([f"{key}: {value}" for key, value in stat_values.items()])
    messagebox.showinfo("Stat Values", dict_string)
    root.quit()

    messagebox.showinfo(message = "Thank you for using the app.",
                        title="Thank you"            
    )

def reset():
    values = []
    stat_values = {}
    combo['values'] = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
    combo.pack()
    
    messagebox.showinfo(message = "Values has been reset",
                        title="Reset"            
    )


# display
number_label = tkinter.Label(root, text="", font="Helvetica 12")
number_label.pack()

sum_of_values = tkinter.Label(root, text="", font="Helvetica 12")
sum_of_values.pack()

combo = ttk.Combobox(
    state='readonly',
    values=['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
)
combo.pack()


blank_label = tkinter.Label(root, text="")
blank_label.pack()

button_select = ttk.Button(text = "Choose Stat", command = display_selection)
button_select.pack()

done_button = ttk.Button(text="Done", command = message_done)
done_button.pack()

button = tkinter.Button(root, text="Roll 4D6", fg='blue', command=lambda: [d6_roll(), threading.Thread(target=play, daemon=True).start()])
button.pack(expand=True)

#button to reset
reset_button = ttk.Button(text = "Reset", command = reset)
reset_button.pack()

root.mainloop()
