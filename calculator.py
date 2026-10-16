import tkinter

button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["3", "2", "1", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]


row_count = len(button_values)
column_count = len(button_values[0])

color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

window = tkinter.Tk()
window.title("Calculator")
window.resizable(False, False)

frame = tkinter.Frame(window)
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_black, foreground=color_white)

label.grid(row=0, column=0)
frame.pack()

window.mainloop()