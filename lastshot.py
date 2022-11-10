#class responsible for displaying stats of the last shot
import tkinter as tk


last_shot_info = ("X", "Y", "Distance to goal", "Angle",'XG','Goal')
class LastShot(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.data = []

        frame = tk.LabelFrame(self,relief = 'groove',text='LAST SHOT DATA',padx=20,pady=20)
        frame.grid(row=0,column=0,ipadx=20)

        for row_num, name in enumerate(last_shot_info):
            desc = tk.Label(frame, text=f"{name}: ")
            desc.grid(row=row_num, column=0)
            result = tk.Label(frame, text="00.00")
            result.grid(row=row_num, column=1)
            self.data.append(result)

    # update the values when they change
    def update_values(self, new_data):
        for result_lbl, value in zip(self.data, new_data):
            result_lbl.config(text="{:05.2f}".format(value))