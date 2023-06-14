from tkinter import ttk


def initialize_styles():
    style = ttk.Style()
    style.theme_use('default')

    style.configure('Big.TButton', font=('Sans', 12))

    style.configure('Small.TButton', font=('Sans', 9))

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

    style.configure('Big.TLabel', font=('Sans', 11))

    style.configure('Blue.TCheckbutton')
    style.map('Blue.TCheckbutton',
              indicatorcolor=[('selected', 'black')])
