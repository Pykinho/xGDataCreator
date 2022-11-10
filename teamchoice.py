#class for choosing an attacking team

import tkinter as tk

class TeamChoice(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        #Add a labelframe
        frame = tk.LabelFrame(self,relief = 'groove',text='CHOOSE THE ATTACKING TEAM',padx=20,pady=20)
        frame.grid(row=0,column=0)

        #Add radio buttons to determine a team that took a shot:
        self.team = tk.StringVar()
        self.team.set('HOME')

        home_team = tk.Radiobutton(frame,text='HOME TEAM',variable=self.team,value='HOME',command=self.master.update_team)
        home_team.grid(row=1,column=0)
        away_team = tk.Radiobutton(frame,text='AWAY TEAM',variable=self.team,value='AWAY',command=self.master.update_team)
        away_team.grid(row=1,column=1)
