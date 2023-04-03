import tkinter as tk
        
window = tk.Tk()
window.title("Battleship_field")
WIDTH = 1200/3
HEIGHT = 900/3
UNIT = WIDTH // 16
#window.geometry(f'{WIDTH}x{HEIGHT}+200+100')
#window["bg"] = "#355C7D"
#window["bg"] = "#406D96"
window["bg"] = "#406D96"
frame_1 = tk.Frame(master=window, bg='#406D96', width=12*UNIT, height = UNIT)
frame_2 = tk.Frame(master=window,bg='#406D96', width=12*UNIT, height = 5*UNIT)

frame_1.pack(side='top', fill='both', expand=True)
frame_11 = tk.Frame(master=frame_1, bg='#406D96', width=5*UNIT, height = 1*UNIT)
frame_12 = tk.Frame(master=frame_1, bg='#406D96', width=5*UNIT, height = 1*UNIT)
frame_11.pack(side='left', fill='both', padx = 1*UNIT, pady = 1*UNIT)
frame_12.pack(side='top', fill='both', padx = 1*UNIT, pady = 1*UNIT)

frame_2.pack(side='top', fill='both', expand=True)
frame_21 = tk.Frame(master=frame_2, bg='black', width=5*UNIT, height = 5*UNIT)
frame_22 = tk.Frame(master=frame_2, bg='black', width=5*UNIT, height = 5*UNIT)
frame_21.pack(side='left', fill='both', expand=True, padx = 1*UNIT, pady = 1*UNIT)
frame_22.pack(side='left', fill='both', expand=True, padx = 1*UNIT, pady = 1*UNIT)

label_1 = tk.Label(master = frame_11, text = 'Fleet of the glorious username1', fg='yellow', bg='#355C7D')
label_1.pack(side='left', fill='both', expand=True, padx = 1*UNIT, pady = 1*UNIT)

label_2 = tk.Label(master = frame_12, text = 'Fleet of the inglorious username2', fg='yellow', bg='#355C7D')
label_2.pack(side='left', fill='both', expand=True, padx = 1*UNIT, pady = 1*UNIT)

my_cells = [[tk.Button(master=frame_21, text='', fg='yellow', bg='#355C7D') for i in range(10)] for j in range(10)]
enemy_cells = [[tk.Button(master=frame_22, text='', fg='yellow', bg='#355C7D') for i in range(10)] for j in range(10)]
for i in range(10):
    frame_21.grid_columnconfigure(index=i, weight=1, minsize=UNIT//4)
    frame_21.grid_rowconfigure(index=i, weight=1, minsize=UNIT//4)
    frame_22.grid_columnconfigure(index=i, weight=1, minsize=UNIT//4)
    frame_22.grid_rowconfigure(index=i, weight=1, minsize=UNIT//4)
    for j in range(10):
        my_cells[i][j].grid(row=j, column=i, sticky='nesw')
        enemy_cells[i][j].grid(row=j, column=i, sticky='nesw')
#for i in range(4):
    #my_cells[0][i].configure(text='X', fg = 'red')
    #my_cells[2][i].configure(text='O', fg = '#00EC00')
    #enemy_cells[0][i].configure(text='X', fg = '#00EC00')
    #enemy_cells[2][i].configure(text='O', fg = 'red')
#window.attributes('-fullscreen', True)
#window.bind("<Escape>")
window.mainloop()
