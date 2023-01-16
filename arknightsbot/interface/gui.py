import sys
import tkinter
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("650x500")
app.title("Arknights Bot")
app.resizable(False, False)


# Start Button

def start_button_event():
    if start_button.cget("text") == "Start":
        start_button.configure(text="Pause")
    else:
        start_button.configure(text="Start")


start_button = customtkinter.CTkButton(master=app,
                                       width=115,
                                       height=32,
                                       border_width=0,
                                       corner_radius=8,
                                       text="Start",
                                       command=start_button_event)
start_button.place(relx=0.87, rely=0.77, anchor=tkinter.CENTER)


# Stop Button

def stop_button_event():
    sys.exit()


stop_button = customtkinter.CTkButton(master=app,
                                      width=115,
                                      height=32,
                                      border_width=0,
                                      corner_radius=8,
                                      text="Stop",
                                      command=stop_button_event)
stop_button.place(relx=0.87, rely=0.85, anchor=tkinter.CENTER)

# Text box for log
log_textbox = customtkinter.CTkTextbox(master=app,
                                       width=600,
                                       height=15)
log_textbox.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

log_textbox.insert("0.0", "Logs go here")  # insert at line 0 character 0

# Text box for info
info_textbox = customtkinter.CTkTextbox(master=app,
                                        width=118,
                                        height=310)
info_textbox.place(relx=0.78, rely=0.027, anchor=tkinter.NW)

info_textbox.insert("0.0", "Info goes here")

# Checkbox for specifying sanity refill setting

check_var = customtkinter.StringVar()


def checkbox_event():
    print("checkbox toggled, current value:", check_var.get())


checkbox = customtkinter.CTkCheckBox(master=app,
                                     text="Refill Sanity",
                                     command=checkbox_event,
                                     variable=check_var,
                                     hover=True,
                                     checkbox_width=17,
                                     checkbox_height=17,
                                     border_width=1,
                                     onvalue="on",
                                     offvalue="off")
checkbox.place(relx=0.87, rely=0.70, anchor=tkinter.CENTER)

# Tab view for the different modes of farming


tabview = customtkinter.CTkTabview(master=app,
                                   width=470,
                                   height=450)
tabview.place(relx=0.4, rely=0.44, anchor=tkinter.CENTER)

tabview.add("Stage Repeat")
tabview.add("Material Farmer")
tabview.add("Manual Repeat")
tabview.set("Stage Repeat")

# Tab View: Stage Repeat
info_stage_repeat = customtkinter.CTkTextbox(master=tabview.tab("Stage Repeat"),
                                             width=300,
                                             height=100)
info_stage_repeat.place(relx=0.01, rely=0.74, anchor=tkinter.NW)

info_stage_repeat.insert("0.0", "Info about stage repeat usage goes here")

# Tab View: Material Farmer

info_material_farmer = customtkinter.CTkTextbox(master=tabview.tab("Material Farmer"),
                                                width=300,
                                                height=100)
info_material_farmer.place(relx=0.01, rely=0.74, anchor=tkinter.NW)

info_material_farmer.insert("0.0", "Info about material farmer usage goes here")

# Tab View: Manual Repeat

info_manual_repeat = customtkinter.CTkTextbox(master=tabview.tab("Manual Repeat"),
                                              width=300,
                                              height=100)
info_manual_repeat.place(relx=0.01, rely=0.74, anchor=tkinter.NW)

info_manual_repeat.insert("0.0", "Info about manual repeat usage goes here")

app.mainloop()
