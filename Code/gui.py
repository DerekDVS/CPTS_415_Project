import tkinter as tk
from tkinter import *
from Code import parser

class GUI:
    def __init__(self, dbm):
        self.dbm = dbm
        

        self.root = tk.Tk()
        self.root.title("Co-Purchasing Analytics Engine")

    def Create_Page(self):
        reset_button = tk.Button(self.root, text="Reset Database (Warning Very Time Consuming)", command=self.dbm.reset_data)
        reset_button.grid(row=0, column=0)
        
        parse_button = tk.Button(self.root, text="Reset Parsed Data (Warning Very Time Consuming)", command=parser.run_parser)
        parse_button.grid(row=1, column=0)

        c1 = tk.Label(self.root, text="Query Options")
        c1.grid(row=2, column=0)

        c1 = tk.Label(self.root, text="Operation")
        c1.grid(row=2, column=1)

        c1 = tk.Label(self.root, text="Value")
        c1.grid(row=3, column=0)

        l2 = tk.Label(self.root, text="Id")
        l2.grid(row=4, column=0)
        l3 = tk.Label(self.root, text="ASIN")
        l3.grid(row=5, column=0)
        l4 = tk.Label(self.root, text="title")
        l4.grid(row=6, column=0)
        l5 = tk.Label(self.root, text="group")
        l5.grid(row=7, column=0)
        l6 = tk.Label(self.root, text="salesrank")
        l6.grid(row=8, column=0)


        button = tk.Button(self.root, text="Search", command=self.button_click)
        button.grid(row=9, column=0)


    def Create_Operator(self, col_i, row_i):
        operator_var = tk.StringVar()
        operator_var.set(">=")

        operator_dropdown = tk.OptionMenu(self.root, operator_var, ">", ">=", "=", "<", "<=")
        operator_dropdown.grid(row=row_i, column=col_i)
        return operator_var


    def Create_Table(self, lst):
        
        # find total number of rows and
        # columns in list
        total_rows = len(lst)
        total_columns = len(lst[0])

        
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                 
                self.e = tk.Entry(self.root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                 
                self.e.grid(row=i+7, column=j)
                self.e.insert(END, lst[i][j])
 
    def button_click(self):
        print("Click")

    def Run(self):
        self.root.mainloop()