import tkinter as tk
import math
from tkinter import *

LARGE_FONT_STYLE = ("Arial", 40)
SMALL_FONT_STYLE = ("Arial", 16)
DIGIT_FONT_STYLE = ('Arial', 25, "bold")
DEFAULT_FONT_STYLE = ('Arial', 22)

DISPLAY_BG = "#252527"

BUTTON_BG = "#404040"
ACTIVE_BG = "#4f4f4f"

OP_BG = "#1f8c93"
OP_ACTIVE = "#42cdd7"

EQUALS_BG = "#125054"
EQUALS_ACTIVE = "#42cdd7"

BUTTON_COLOR = "white"
LABEL_COLOR = "white"


class Calculator:
    
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.geometry("375x600")
        self.window.resizable(0,0)
        self.window.title("Calculator")
        
        self.icon = PhotoImage(file="icon.png")
        self.window.iconphoto(True,self.icon)
        
        self.tot_exp = ""
        self.cur_exp = "0"
        
        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()
        
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        
        self.tot_label, self.label = self.create_display_labels()
        self.update_label()
        
        self.digits = {
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            0:(4,2), '.':(4,3)
        }
        
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=220, bg=DISPLAY_BG)
        frame.pack(expand=True, fill="both")
        return frame
    
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def create_display_labels(self):
        tot_label = tk.Label(self.display_frame, 
                             text=self.tot_exp, 
                             anchor=tk.E, 
                             bg=DISPLAY_BG, 
                             fg=LABEL_COLOR,
                             font=SMALL_FONT_STYLE)
        
        tot_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, 
                         text=self.tot_exp, 
                         anchor=tk.E, 
                         bg=DISPLAY_BG, 
                         fg=LABEL_COLOR,
                         font=LARGE_FONT_STYLE)
        
        label.pack(expand=True, fill="both")
        
        return tot_label,label

    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, 
                               text=str(digit),
                               bg=BUTTON_BG,
                               fg=BUTTON_COLOR,
                               activebackground=ACTIVE_BG,
                               font=DIGIT_FONT_STYLE,
                               borderwidth=0,
                               command= lambda x=digit: self.add_to_exp(x))
            button.grid(row=grid_value[0], 
                        column=grid_value[1], 
                        sticky=tk.NSEW)

    def create_operator_buttons(self):
        i=0
        for operator,symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, 
                               text=symbol, 
                               font=DEFAULT_FONT_STYLE,
                               bg=OP_BG,
                               fg=LABEL_COLOR,
                               activebackground=OP_ACTIVE,
                               borderwidth=0,
                               command= lambda x=operator: self.append_op(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_sign_button()
        self.create_back_button()
        self.create_sqrt_button()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, 
                               text="=", 
                               font=DEFAULT_FONT_STYLE,
                               bg=EQUALS_BG,
                               fg=LABEL_COLOR,
                               activebackground=EQUALS_ACTIVE,
                               borderwidth=0,
                               command= self.evaluate)
        button.grid(row=4, column=4, sticky=tk.NSEW)

    def create_sign_button(self):
        button = tk.Button(self.buttons_frame, 
                               text="+/-", 
                               font=DEFAULT_FONT_STYLE,
                               bg=BUTTON_BG,
                               fg=BUTTON_COLOR,
                               activebackground=ACTIVE_BG,
                               borderwidth=0,
                               command= self.sign_change)
        button.grid(row=4, column=1, sticky=tk.NSEW)

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, 
                               text="C", 
                               font=DEFAULT_FONT_STYLE,
                               bg=OP_BG,
                               fg=LABEL_COLOR,
                               activebackground=OP_ACTIVE,
                               borderwidth=0,
                               command= self.clear)
        
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def create_back_button(self):
        button = tk.Button(self.buttons_frame, 
                               text="\u232b", 
                               font=DEFAULT_FONT_STYLE,
                               bg=OP_BG,
                               activebackground=OP_ACTIVE,
                               fg=LABEL_COLOR,
                               borderwidth=0,
                               command= self.backspace)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, 
                               text="√x", 
                               font=DEFAULT_FONT_STYLE,
                               bg=OP_BG,
                               activebackground=OP_ACTIVE,
                               fg=LABEL_COLOR,
                               borderwidth=0,
                               command= self.sqrt)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def add_to_exp(self,value):
        if(self.cur_exp == ""):
            self.tot_exp = ""
            self.update_total_label()
        if "." in self.cur_exp and value == ".":
            self.label.config(text="Error")
        else:
            if self.cur_exp == "0" or "":
                if value == ".":
                    self.cur_exp = "0" + str(value)
                    self.update_label()
                else: 
                    self.cur_exp = str(value)
                    self.update_label()
            else: 
                self.cur_exp += str(value)
                self.update_label()
        
    def append_op(self, operator):
        for key in self.operations:
            if(self.tot_exp.endswith(key) and self.cur_exp == "0"):
                self.tot_exp = self.tot_exp[:-1] + operator
                self.update_total_label()
            
        if (self.cur_exp != "0" or self.tot_exp == "") and self.cur_exp != "Error":
            self.cur_exp += operator
            self.tot_exp += self.cur_exp
            self.cur_exp = ""
            self.update_label()
            self.update_total_label()

    def evaluate(self):
        self.tot_exp += self.cur_exp
        expr = self.tot_exp
        self.tot_exp += " = "
        self.update_total_label()
        try:
            self.cur_exp = str(eval(expr))
        except Exception as e:
            self.cur_exp = "Error"
            self.update_label()
            
        finally:
            if self.cur_exp == "Error":
                self.cur_exp = ""
            else:
                self.update_label()
                self.tot_exp = self.cur_exp               
                self.cur_exp = ""
                
    def sqrt(self):
        self.update_total_label()
        try:
            if self.cur_exp == "":
                self.cur_exp = str(math.sqrt(int(self.tot_exp)))
            else:    
                self.cur_exp = str(math.sqrt(int(self.cur_exp)))
            self.tot_exp = self.cur_exp
            self.update_label()
        except:
            self.label.config(text="Error")

    def sign_change(self):
        if(self.cur_exp.startswith("-")):
            self.cur_exp = self.cur_exp.replace("-","")
        else: self.cur_exp = "-" + self.cur_exp
        self.update_label()

    def backspace(self):
        self.cur_exp = self.cur_exp[:-1]
        self.update_label()

    def clear(self):
        self.cur_exp = ""
        self.tot_exp = ""
        self.update_label()
        self.update_total_label()

    def update_total_label(self):
        expression = self.tot_exp
        for operator,symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.tot_label.config(text=expression[:14])
        
    def update_label(self):
        if self.cur_exp == "":
            self.cur_exp = "0"
        if self.cur_exp.endswith(".0"):
            self.cur_exp = self.cur_exp.replace(".0","")
        self.label.config(text=self.cur_exp[:11])

    def run(self):
        self.window.mainloop()
        

if __name__ == "__main__":
    calc = Calculator()
    calc.run()