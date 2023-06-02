from tkinter import ttk


class Style:
    def __init__(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Blue.TFrame', background='#406D96')
        style.configure('Blue.TButton', width=3, background='#355C7D')
        style.configure('Ship.TButton', width=3)
        style.configure('Hit.TButton', width=3)
        style.configure('Miss.TButton', width=3)
        style.configure('Sank.TButton', width=3)
        style.configure('Red.TLabel', background='red')
        style.map('Blue.TButton', background=[('!pressed', 'disabled', '#26364a'), ('hover', 'pink')])
        style.map('Ship.TButton', background=[('disabled', 'grey')])
        style.map('Hit.TButton', background=[('disabled', 'orange')])
        style.map('Sank.TButton', background=[('disabled', 'red')])
        style.map('Miss.TButton', background=[('disabled', 'black')])
