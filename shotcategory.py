import tkinter as tk

class ShotCategory(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        #Add a labelframe
        frame = tk.LabelFrame(self,relief = 'groove',text='CHOOSE THE CATEGORY OF THE SHOT',padx=20,pady=20)
        frame.grid(row=0,column=0)

        #Add radio buttons to determine a team that took a shot:
        self.category = tk.StringVar()
        self.category.set('OPEN PLAY')

        home_team = tk.Radiobutton(frame,text='OPEN PLAY',variable=self.category,value='OPEN PLAY',command=self.master.update_category)
        home_team.grid(row=0,column=0)
        away_team = tk.Radiobutton(frame,text='HEADER',variable=self.category,value='HEADER',command=self.master.update_category)
        away_team.grid(row=0,column=1)
        away_team = tk.Radiobutton(frame,text='FREE KICK',variable=self.category,value='FREE KICK',command=self.master.update_category)
        away_team.grid(row=1,column=0)
        away_team = tk.Radiobutton(frame,text='PENALTY KICK',variable=self.category,value='PENALTY KICK',command=self.master.update_category)
        away_team.grid(row=1,column=1)