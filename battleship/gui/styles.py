from tkinter import ttk


def initialize_styles():
    style = ttk.Style()
    style.theme_use('default')

    style.configure('Empty.TButton', width=3)
    style.map('Empty.TButton',
              background=[('hover', '!disabled', 'grey'),
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

    style.configure('Blue.TButton')
    style.map('Blue.TButton',
              background=[('hover', '#6fa8dc'),
                          ('!hover', '#9fc5e8')])

    style.configure('Big.Blue.TButton', font=('Sans', 12))
    style.configure('Small.Blue.TButton', font=('Sans', 9))

    style.configure('Blue.TFrame', background='#cfe2f3')
    style.configure('Bluer.TFrame', background='#9fc5e8')

    style.configure('Bluer.TLabel', background='#9fc5e8')

    style.configure('Blue.TLabel', background='#cfe2f3')
    style.configure('Big.Blue.TLabel', font=('Sans', 11))

    style.configure('Blue.TMenubutton')
    style.map('Blue.TMenubutton',
              background=[('hover', '#6fa8dc'),
                          ('!hover', '#cfe2f3')])

    style.configure('Bluer.TCheckbutton')
    style.map('Bluer.TCheckbutton',
              indicatorcolor=[('selected', 'black')])
