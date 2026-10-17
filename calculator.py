import ast
import math
import tkinter
import operator as arithmetic

button_values = [
    ["x²", "xʸ", "1/x", "⌫"],
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["3", "2", "1", "+"],
    ["0", ".", "√", "="],
    ["History", "", "", ""]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%", "⌫", "x²", "xʸ", "1/x", "History"]

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
window.configure(background=color_black)

frame = tkinter.Frame(window, background=color_black)
label = tkinter.Label(frame, text="0", font=("Arial", 40), background=color_black,
                      foreground=color_white, anchor="e", width=column_count * 3)
label.grid(row=0, column=0, columnspan=column_count, sticky="we")

A = "0"
operator = None
B = None
just_calculated = False
history = []
operator_buttons = {}
selected_operator = None
power_expression = None


def remove_zero_decimal(num):
    if abs(num) < 1e15 and num % 1 == 0:
        num = int(num)
    return str(num)


def evaluate_expression(expression):
    expression = expression.replace("×", "*").replace("÷", "/").replace("xʸ", "**")
    tree = ast.parse(expression, mode="eval")

    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = calculate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp):
            operations = {ast.Add: arithmetic.add, ast.Sub: arithmetic.sub, ast.Mult: arithmetic.mul,
                          ast.Div: arithmetic.truediv, ast.Pow: arithmetic.pow, ast.Mod: arithmetic.mod}
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("Invalid operation")
            left = calculate(node.left)
            right = calculate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Exponent is too large")
            return operation(left, right)
        raise ValueError("Invalid expression")

    result = calculate(tree)
    if not math.isfinite(result):
        raise ValueError("Invalid result")
    return result


def clear_all():
    global A, B, operator, just_calculated
    A = "0"
    operator = None
    B = None
    just_calculated = False


def show_error():
    global A, B, operator, just_calculated
    label["text"] = "Error"
    A = "0"
    operator = None
    B = None
    just_calculated = True


def history_window():
    history_page = tkinter.Toplevel(window)
    history_page.title("Calculation History")
    history_page.configure(background=color_black)
    tkinter.Label(history_page, text="History", font=("Arial", 18), background=color_black,
                  foreground=color_white).pack(padx=12, pady=(12, 4))
    items = history[-20:] if history else ["No calculations yet"]
    for item in reversed(items):
        tkinter.Label(history_page, text=item, font=("Arial", 13), background=color_black,
                      foreground=color_white, anchor="e").pack(fill="x", padx=12, pady=2)


def update_operator_buttons():
    for value, button in operator_buttons.items():
        if value == selected_operator:
            button.config(background="#CC7A00")
        else:
            button.config(background=color_orange)


def button_clicked(value):
    global A, B, operator, just_calculated, selected_operator, power_expression

    if value == "History":
        history_window()
        return
    if value == "AC":
        clear_all()
        label["text"] = "0"
        power_expression = None
        selected_operator = None
        update_operator_buttons()
        return
    if value == "⌫":
        if label["text"] == "Error":
            clear_all()
            label["text"] = "0"
        else:
            label["text"] = label["text"][:-1] or "0"
            if label["text"] in ("-", "("):
                label["text"] = "0"
            just_calculated = False
        return
    if value == "=":
        expression = label["text"]
        try:
            if power_expression is not None:
                expression = power_expression + "xʸ" + label["text"]
            result = evaluate_expression(expression)
            answer = remove_zero_decimal(result)
            history.append(expression + " = " + answer)
            label["text"] = answer
            power_expression = None
            clear_all()
            A = answer
            just_calculated = True
            selected_operator = None
            update_operator_buttons()
        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
            show_error()
            power_expression = None
            selected_operator = None
            update_operator_buttons()
        return

    if value in ("√", "x²", "1/x"):
        try:
            number = float(label["text"])
            if value == "√":
                result = math.sqrt(number)
            elif value == "x²":
                result = number ** 2
            else:
                result = 1 / number
            if not math.isfinite(result):
                raise ValueError("Invalid result")
            label["text"] = remove_zero_decimal(result)
            just_calculated = True
        except (ValueError, ZeroDivisionError, OverflowError):
            show_error()
        return

    if value == "%":
        try:
            label["text"] = remove_zero_decimal(float(label["text"]) / 100)
            just_calculated = True
        except (ValueError, OverflowError):
            show_error()
        return

    if value == "+/-":
        if label["text"] != "Error":
            if label["text"].startswith("-"):
                label["text"] = label["text"][1:]
            else:
                label["text"] = "-" + label["text"]
        just_calculated = False
        return

    if value in ("+", "-", "×", "÷", "xʸ"):
        if value == "xʸ":
            if label["text"] == "Error":
                label["text"] = "0"
            if power_expression is not None:
                try:
                    label["text"] = remove_zero_decimal(evaluate_expression(power_expression + "xʸ" + label["text"]))
                except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
                    show_error()
                    power_expression = None
                    return
            power_expression = label["text"]
            just_calculated = False
            selected_operator = value
            update_operator_buttons()
            return

        if power_expression is not None:
            try:
                label["text"] = remove_zero_decimal(evaluate_expression(power_expression + "xʸ" + label["text"]))
                power_expression = None
            except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
                show_error()
                power_expression = None
                return
        if label["text"] == "Error":
            label["text"] = "0"
        if just_calculated:
            just_calculated = False
        if label["text"][-1:] in ("+", "-", "×", "÷"):
            if value == "-":
                label["text"] += value
            elif label["text"][-1:] == "-" and len(label["text"]) > 1 and label["text"][-2] in ("+", "-", "×", "÷"):
                label["text"] = label["text"][:-2] + value
            else:
                label["text"] = label["text"][:-1] + value
        elif label["text"].endswith("xʸ"):
            label["text"] = label["text"][:-2] + value
        elif label["text"].endswith("."):
            label["text"] = label["text"][:-1] + value
        elif label["text"] == "0" and value == "-":
            label["text"] = "-"
        else:
            label["text"] += value
        selected_operator = value
        update_operator_buttons()
        return

    if value == ".":
        if power_expression is not None and label["text"] == power_expression:
            label["text"] = "0"
            just_calculated = False
        if just_calculated or label["text"] == "Error":
            label["text"] = "0"
            just_calculated = False
        current_number = label["text"].replace("×", "|").replace("÷", "|").replace("+", "|").replace("xʸ", "|")
        current_number = current_number.split("|")[-1]
        if "." not in current_number:
            label["text"] += "0." if current_number in ("", "-") else "."
        return

    if value in "0123456789":
        if power_expression is not None and not just_calculated:
            if label["text"] == power_expression or label["text"] == "0":
                label["text"] = "0"
        if label["text"] == "Error" or just_calculated:
            label["text"] = "0"
            just_calculated = False
        if label["text"] == "0":
            label["text"] = value
        elif label["text"] == "-":
            label["text"] += value
        else:
            label["text"] += value


for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        if not value:
            continue
        button = tkinter.Button(frame, text=value, font=("Arial", 20), width=5, height=2,
                                command=lambda value=value: button_clicked(value), relief="flat", bd=0,
                                activeforeground=color_white, activebackground=color_dark_gray,
                                highlightthickness=0, takefocus=False)
        if value in right_symbols:
            button.config(foreground=color_white, background=color_orange,
                          activebackground="#CC7A00")
            operator_buttons[value] = button
        elif value in top_symbols or value == "History":
            button.config(foreground=color_black, background=color_light_gray,
                          activeforeground=color_black, activebackground="#BDBDBB")
        else:
            button.config(foreground=color_white, background=color_dark_gray,
                          activebackground="#686868")
        button.grid(row=row + 1, column=column, padx=4, pady=4, sticky="nsew")

frame.pack()


def key_pressed(event):
    key_map = {"Return": "=", "KP_Enter": "=", "BackSpace": "⌫", "Escape": "AC",
               "KP_Add": "+", "KP_Subtract": "-", "KP_Multiply": "×", "KP_Divide": "÷", "KP_Decimal": "."}
    if event.keysym in key_map:
        button_clicked(key_map[event.keysym])
    elif event.char in "0123456789.+-*/%":
        button_clicked({"*": "×", "/": "÷"}.get(event.char, event.char))
    elif event.char == "^":
        button_clicked("xʸ")
    return "break"


window.bind("<Key>", key_pressed)
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
window.mainloop()
