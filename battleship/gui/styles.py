from tkinter import ttk


class Style:
    def __init__(self):
        style = ttk.Style()
        style.theme_use('default')

        style.configure('Blue.TFrame', background='#406D96')

        style.configure('Blue.TButton', width=3)
        style.map('Blue.TButton',
                  background=[('hover', '!disabled', 'pink'),
                              ('!disabled', '#355C7D'),
                              ('disabled', '#26364a')])

        style.configure('Ship.TButton', width=3)
        style.map('Ship.TButton',
                  background=[('disabled', 'grey')])

        style.configure('Hit.TButton', width=3)
        style.map('Hit.TButton',
                  background=[('disabled', 'orange')])

        style.configure('Miss.TButton', width=3)
        style.map('Miss.TButton',
                  background=[('disabled', 'black')])

        style.configure('Sank.TButton', width=3)
        style.map('Sank.TButton',
                  background=[('disabled', 'red')])

        style.configure('Red.TLabel', background='red')

        style.configure('Blue.TCheckbutton')
        style.map('Blue.TCheckbutton',
                  indicatorcolor=[('selected', 'black')])
