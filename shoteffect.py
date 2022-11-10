import tkinter as tk

class ShotEffect(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.isGoal = tk.BooleanVar()
        self.isGoal.set(False)

        #Add a labelframe
        frame = tk.LabelFrame(self,relief = 'groove',text='SHOT EFFECT',padx=20,pady=20)
        frame.grid(row=0,column=0)
        no_goal = tk.Radiobutton(frame,text='NO GOAL',variable=self.isGoal,value=False,command=self.master.update_shoteffect)
        no_goal.grid(row=1,column=0)
        goal = tk.Radiobutton(frame,text='GOAL',variable=self.isGoal,value=True,command=self.master.update_shoteffect)
        goal.grid(row=1,column=1)