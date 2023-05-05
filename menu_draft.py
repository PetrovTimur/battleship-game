import tkinter as tk

window = tk.Tk()
window.title("Battleship_menue")
# window["bg"] = "#355C7D"
# window["bg"] = "#406D96"
window["bg"] = "black"
frm_name = tk.Frame(window, relief=tk.GROOVE, pady=10, padx=10, bg="#406D96")
entry = tk.Entry(frm_name, fg="grey", bg="#A8D0DA")
entry.pack(fill=tk.BOTH, expand=True)
frm_single = tk.Frame(window, relief=tk.GROOVE, pady=0, padx=10, bg="#406D96")
frm_multi = tk.Frame(window, relief=tk.GROOVE, pady=10, padx=10, bg="#406D96")
btn_single = tk.Button(
    master=frm_single,
    text="single player",
    width=50,
    height=5,
    bg="#2F3A56",
    fg="yellow",
)
btn_single.pack(fill=tk.BOTH, expand=True)
btn_multi = tk.Button(
    master=frm_multi,
    text="multi player",
    width=50,
    height=5,
    bg="#2F3A56",
    fg="yellow",
)
btn_multi.pack(fill=tk.BOTH, expand=True)
frm_name.pack(fill=tk.BOTH, expand=True)
frm_single.pack(fill=tk.BOTH, expand=True)
frm_multi.pack(fill=tk.BOTH, expand=True)
entry.insert(0, '#your name')
# window.attributes('-fullscreen', True)
# window.bind("<Escape>")
window.mainloop()
