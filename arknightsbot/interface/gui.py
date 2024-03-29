import os
import sys
import tkinter
import customtkinter

from arknightsbot.utils import material_dictionary
from arknightsbot.utils.logger import logger
from arknightsbot.utils.material_dictionary import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("650x500")
app.title("Arknights Bot")
app.resizable(False, False)

farm_queue = []


# Start Button
def start_button_event():
    if start_button.cget("text") == "Start":
        start_button.configure(text="Pause")
        print(farm_queue)
    else:
        start_button.configure(text="Start")


start_button = customtkinter.CTkButton(master=app,
                                       width=115,
                                       height=32,
                                       border_width=0,
                                       corner_radius=8,
                                       text="Start",
                                       command=start_button_event)
start_button.place(relx=0.87, rely=0.78, anchor=tkinter.CENTER)


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
stop_button.place(relx=0.87, rely=0.855, anchor=tkinter.CENTER)

# Label for log
log_background = customtkinter.CTkTextbox(master=app,
                                          width=470,
                                          height=10,
                                          state="disabled")
log_background.place(relx=0.037, rely=0.945, anchor=tkinter.W)

log_label = customtkinter.CTkLabel(master=log_background,
                                   text="Waiting to start farming")
log_label.place(relx=0.025, rely=0.5, anchor=tkinter.W)
# logger = Logger(__name__, log_label)

# Text box for info
info_textbox = customtkinter.CTkTextbox(master=app,
                                        width=118,
                                        height=310)
info_textbox.place(relx=0.78, rely=0.027, anchor=tkinter.NW)

info_textbox.insert("0.0", "Statistics")

# Checkbox for specifying sanity refill setting

switch_var = customtkinter.StringVar(value=False)

refill_switch = customtkinter.CTkSwitch(master=app,
                                        text="Refill Sanity",
                                        variable=switch_var,
                                        onvalue=True,
                                        offvalue=False)
refill_switch.place(relx=0.87, rely=0.70, anchor=tkinter.CENTER)

# Tab view for the different modes of farming


tabview = customtkinter.CTkTabview(master=app,
                                   width=470,
                                   height=450)
tabview.place(relx=0.4, rely=0.44, anchor=tkinter.CENTER)

tabview.add("Stage Repeat")
tabview.add("Material Farmer")
tabview.add("Manual Repeat")

tabview.set("Stage Repeat")

"""""""""Tab View: Stage Repeat"""""""""
info_stage_repeat = customtkinter.CTkTextbox(master=tabview.tab("Stage Repeat"),
                                             width=448,
                                             height=100,
                                             wrap="word")
info_stage_repeat.place(relx=0.01, rely=0.74, anchor=tkinter.NW)

info_stage_repeat.insert("0.0", "The Stage Repeat feature will simply repeat a given stage. All non-event story and "
                                "supply "
                                "stages are valid given they are unlocked.")
info_stage_repeat.configure(state="disabled")

stage_queue_label = customtkinter.CTkLabel(master=tabview.tab("Stage Repeat"),
                                           text="Stage Queue")
stage_queue_label.place(relx=0.73, rely=0.07, anchor=tkinter.W)


def clear_button_event():
    farm_queue.clear()
    stage_queue_textbox.delete("0.0", "end")
    mats_queue_textbox.delete("0.0", "end")
    logger.log("Cleared queue")


stage_clear_button = customtkinter.CTkButton(master=tabview.tab("Stage Repeat"),
                                             width=15,
                                             height=7,
                                             command=clear_button_event,
                                             text="Clear",
                                             font=('', 10))
stage_clear_button.place(relx=0.913, rely=0.06, anchor=tkinter.W)

stage_queue_textbox = customtkinter.CTkTextbox(master=tabview.tab("Stage Repeat"),
                                               width=118,
                                               height=248,
                                               wrap="word")
stage_queue_textbox.place(relx=0.73, rely=0.095, anchor=tkinter.NW)

stage_label = customtkinter.CTkLabel(master=tabview.tab("Stage Repeat"),
                                     text="Enter Stage")
stage_label.place(relx=0.05, rely=0.3, anchor=tkinter.W)

stage_entry = customtkinter.CTkEntry(master=tabview.tab("Stage Repeat"),
                                     width=170,
                                     height=29,
                                     placeholder_text="i.e. 1-7 or JT8-2")
stage_entry.place(relx=0.05, rely=0.35, anchor=tkinter.NW)

amount_label = customtkinter.CTkLabel(master=tabview.tab("Stage Repeat"),
                                      text="Repeats")
amount_label.place(relx=0.5, rely=0.3, anchor=tkinter.W)

amount_entry = customtkinter.CTkEntry(master=tabview.tab("Stage Repeat"),
                                      width=50,
                                      height=29)
amount_entry.place(relx=0.5, rely=0.35, anchor=tkinter.NW)


def stage_queue_button_event():
    stage = stage_entry.get()
    amount = int(amount_entry.get())
    if stage != "":
        farm_queue.append((stage, amount))
        logger.log("Added to queue")
        stage_queue_textbox.insert("end", f"{stage}: {amount}\n")
        mats_queue_textbox.insert("end", f"{stage}: {amount}\n")
    else:
        logger.log("Enter a stage")


queue_button = customtkinter.CTkButton(master=tabview.tab("Stage Repeat"),
                                       width=115,
                                       height=32,
                                       border_width=0,
                                       corner_radius=8,
                                       text="Queue Stage",
                                       command=stage_queue_button_event)
queue_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

"""""""""Tab View: Material Farmer"""""

info_material_farmer = customtkinter.CTkTextbox(master=tabview.tab("Material Farmer"),
                                                width=448,
                                                height=100,
                                                wrap="word")
info_material_farmer.place(relx=0.01, rely=0.74, anchor=tkinter.NW)

info_material_farmer.insert("0.0", "The Material Farmer will translate any selected Tier 4 or higher material into "
                                   "its Tier 3 equivalents. It will then farm the most efficient stages for the "
                                   "materials. \nEntering large amounts of high tier materials is not recommended as "
                                   "the bot does not account for materials you already have.")
info_material_farmer.configure(state="disabled")

mats_queue_label = customtkinter.CTkLabel(master=tabview.tab("Material Farmer"),
                                          text="Stage Queue")
mats_queue_label.place(relx=0.73, rely=0.07, anchor=tkinter.W)

mats_clear_button = customtkinter.CTkButton(master=tabview.tab("Material Farmer"),
                                            width=15,
                                            height=7,
                                            command=clear_button_event,
                                            text="Clear",
                                            font=('', 10))
mats_clear_button.place(relx=0.913, rely=0.06, anchor=tkinter.W)

mats_queue_textbox = customtkinter.CTkTextbox(master=tabview.tab("Material Farmer"),
                                              width=118,
                                              height=248,
                                              wrap="word")
mats_queue_textbox.place(relx=0.73, rely=0.095, anchor=tkinter.NW)

material_combobox = customtkinter.CTkComboBox(master=tabview.tab("Material Farmer"),
                                              width=170,
                                              values=material_dictionary.materials_list)
material_combobox.place(relx=0.05, rely=0.35, anchor=tkinter.NW)
material_combobox.set(value="Choose Material")

material_label = customtkinter.CTkLabel(master=tabview.tab("Material Farmer"),
                                        text="Material")
material_label.place(relx=0.05, rely=0.3, anchor=tkinter.W)

mat_amount_label = customtkinter.CTkLabel(master=tabview.tab("Material Farmer"),
                                          text="Amount")
mat_amount_label.place(relx=0.5, rely=0.3, anchor=tkinter.W)

mat_amount_entry = customtkinter.CTkEntry(master=tabview.tab("Material Farmer"),
                                          width=50,
                                          height=29)
mat_amount_entry.place(relx=0.5, rely=0.35, anchor=tkinter.NW)


def mat_queue_button_event():
    material = material_combobox.get().lower()
    amount = int(mat_amount_entry.get())
    if material != "Choose Material":
        stages = optimal_stage_for_material(calculate_material_equivalency(material, amount))
        farm_queue.append(stages)
        stage_queue_textbox.insert("end", f"{amount} {material_combobox.get()}\n")
        mats_queue_textbox.insert("end", f"{amount} {material_combobox.get()}\n")
        for stage, number in stages:
            stage_queue_textbox.insert("end", f"     {stage}: {number}\n")
            mats_queue_textbox.insert("end", f"     {stage}: {number}\n")
        logger.log("Added to queue")
    else:
        logger.log("Select a material")


mat_queue_button = customtkinter.CTkButton(master=tabview.tab("Material Farmer"),
                                           width=115,
                                           height=32,
                                           border_width=0,
                                           corner_radius=8,
                                           text="Queue Material",
                                           command=mat_queue_button_event)
mat_queue_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

"""""""""Tab View: Manual Repeat"""""""""
info_manual_repeat = customtkinter.CTkTextbox(master=tabview.tab("Manual Repeat"),
                                              width=448,
                                              height=100,
                                              wrap="word")
info_manual_repeat.place(relx=0.01, rely=0.74, anchor=tkinter.NW)
info_manual_repeat.insert("0.0", "Manual Repeat is intended for use on event stages or other unlisted stages. \n\n To "
                                 "start it, tap on stage that you would like to repeat (so that the autodeploy toggle "
                                 "is visible) and hit start in the bot interface.")
info_manual_repeat.configure(state="disabled")

manual_amount_label = customtkinter.CTkLabel(master=tabview.tab("Manual Repeat"),
                                             text="Repeats")
manual_amount_label.place(relx=0.5, rely=0.3, anchor=tkinter.W)

manual_amount_entry = customtkinter.CTkEntry(master=tabview.tab("Manual Repeat"),
                                             width=50,
                                             height=29)
manual_amount_entry.place(relx=0.5, rely=0.35, anchor=tkinter.NW)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
image_path = os.path.join(parent_dir, 'detection', 'reference_images', 'gui', 'gui_manual_repeat.png')
image = tkinter.PhotoImage(file=image_path)

image_label = tkinter.Label(master=tabview.tab("Manual Repeat"),
                            image=image)
image_label.place(relx=0.01, rely=0.4, anchor=tkinter.W)

app.mainloop()
