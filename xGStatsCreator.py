#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import pandas as pd
import os

from pitchshots import PitchShots
from lastshot import LastShot
from teamchoice import TeamChoice
from shotcategory import ShotCategory
from shoteffect import ShotEffect
from shotstable import ShotsTable
        
# GUI etc
class xGStatsCreator(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.shots_info = pd.DataFrame(columns=['Category','Team','X','Y','Distance','Angle','XG','Goal'])
        self.pitch_shots = PitchShots(self)
        self.pitch_shots.grid(row=0, column=1, rowspan=4,columnspan=2,pady=20)

        self.teams = TeamChoice(self)
        self.teams.grid(row=0,column=0,sticky='ew',padx=20,pady=20)

        self.shot_category = ShotCategory(self)
        self.shot_category.grid(row=1,column=0,sticky='ew',padx=20,pady=20)

        self.goal_effect = ShotEffect(self)
        self.goal_effect.grid(row=2,column=0,sticky='ew',padx=20,pady=20)

        self.stats = LastShot(self)
        self.stats.grid(row=0, column=3,sticky='ew',rowspan=3,padx=20,pady=20)

        self.home_shots_table = ShotsTable(self)
        self.home_shots_table.grid(row=4,column=1,sticky='ew',padx=20,pady=20)

        self.away_shots_table = ShotsTable(self)
        self.away_shots_table.grid(row=4,column=2,sticky='ew',padx=20,pady=20)

        self.rowconfigure(2, weight=1)

        self.undo = False

        # menu items
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Options", menu=filemenu)
        filemenu.add_command(label="Quit", command=self.quit,accelerator="Ctrl+Q")
        filemenu.add_command(label="Reset",command=self.pitch_shots.reset_points,accelerator="Ctrl+R")
        filemenu.add_command(label="Export Data", command=self.export_data,accelerator="Ctrl+E")
        filemenu.add_command(label="Undo", command=self.pitch_shots.undo,accelerator="Ctrl+Z")

        self.master.bind('Control-q',self.quit)
        self.master.bind('Control-r',self.pitch_shots.reset_points)
        self.master.bind('Control-e',self.export_data)
        self.master.bind('Control-z',self.pitch_shots.undo)

        # add menubar
        self.master.config(menu=menubar)


    def update_data(self, shots_locations):

        if not self.undo:
            xShot, yShot = [point.calcX for point in shots_locations], [point.calcY for point in shots_locations]

            if len(xShot)>0 and len(yShot)>0:
                lastShot = pd.DataFrame([{'Category':'','Team':'','X':xShot[-1],'Y':yShot[-1],'Distance':0.0,'Angle':0.0,'XG':0.0,'Goal':False}])
                self.shots_info = pd.concat([self.shots_info,lastShot],ignore_index=True)

            if self.shots_info.empty:
                self.stats.update_values([00.00, 00.00, 00.00, 00.00, 00.00])

            else:
            
                self.shots_info.Team.iloc[-1] = self.pitch_shots.team
                self.shots_info.Category.iloc[-1] = self.shot_category.category.get()
                self.shots_info.Goal.iloc[-1] = self.goal_effect.isGoal.get() 
                self.shots_info.Distance.iloc[-1] = np.sqrt(self.shots_info.X.iloc[-1]**2 + self.shots_info.Y.iloc[-1]**2)
                self.shots_info.Angle.iloc[-1] = np.arctan(7.32*self.shots_info.X.iloc[-1]/(self.shots_info.X.iloc[-1]**2+self.shots_info.Y.iloc[-1]**2 - (7.32/2)**2))
                self.shots_info.loc[(self.shots_info.Angle <=0) & (self.shots_info.Distance <= 3.66), 'Angle' ] += np.pi


                self.shots_info.loc[self.shots_info.Category == 'OPEN PLAY','XG'] = 1/(1+np.exp(1.2 - 1.7*self.shots_info.Angle.iloc[-1] + 
                                                                0.1*self.shots_info.Distance.iloc[-1]))
                self.shots_info.loc[self.shots_info.Category == 'HEADER','XG'] = 1/(1+np.exp(1.63 - 1.31*self.shots_info.Angle.iloc[-1] + 
                                                                0.14*self.shots_info.Distance.iloc[-1]))
                self.shots_info.loc[self.shots_info.Category == 'PENALTY KICK','XG'] = 0.76
                
                
                self.stats.update_values([self.shots_info.X.iloc[-1], self.shots_info.Y.iloc[-1], self.shots_info.Distance.iloc[-1], 
                                        self.shots_info.Angle.iloc[-1], self.shots_info.XG.iloc[-1],self.shots_info.Goal.iloc[-1]])

                
                if self.shots_info.Team.iloc[-1] == 'HOME':
                    self.home_shots_table.update_table(self.shots_info.Category.iloc[-1],
                        self.shots_info.Distance.iloc[-1], self.shots_info.Angle.iloc[-1], 
                        self.shots_info.XG.iloc[-1],self.shots_info.Goal.iloc[-1])
                else:
                    self.away_shots_table.update_table(self.shots_info.Category.iloc[-1],
                        self.shots_info.Distance.iloc[-1], self.shots_info.Angle.iloc[-1], 
                        self.shots_info.XG.iloc[-1],self.shots_info.Goal.iloc[-1])

                self.update_score()
                

        else:
            self.stats.update_values([self.shots_info.X.iloc[-1], self.shots_info.Y.iloc[-1], self.shots_info.Distance.iloc[-1], 
                                    self.shots_info.Angle.iloc[-1], self.shots_info.XG.iloc[-1],self.shots_info.Goal.iloc[-1]])
            self.undo = False
            
            
    def update_team(self):
        self.pitch_shots.team = self.teams.team.get()


    def update_category(self):
        self.pitch_shots.category = self.shot_category.category.get()


    def update_shoteffect(self):
        self.pitch_shots.goal = self.goal_effect.isGoal.get()


    def update_score(self):

        if self.shots_info.Team.iloc[-1] == 'HOME':
            self.pitch_shots.home_xg +=  self.shots_info.XG.iloc[-1]
            if self.shots_info.Goal.iloc[-1]:
                self.pitch_shots.home_goals += 1
        else:
            self.pitch_shots.away_xg +=  self.shots_info.XG.iloc[-1]
            if self.shots_info.Goal.iloc[-1]:
                self.pitch_shots.away_goals += 1


    def clear_shots(self):
        self.shots_info.drop(self.shots_info.index, inplace=True)
        self.away_shots_table.clear_all()
        self.home_shots_table.clear_all()


    def undo_shots(self,team):
        
        if team == 'HOME':
            self.home_shots_table.undo()
            self.pitch_shots.home_xg -= self.shots_info.XG.iloc[-1]
            if self.shots_info.Goal.iloc[-1]:
                self.pitch_shots.home_goals -= 1
        else:
            self.away_shots_table.undo()
            self.pitch_shots.away_xg -= self.shots_info.XG.iloc[-1]
            if self.shots_info.Goal.iloc[-1]:
                self.pitch_shots.away_goals -= 1
        
        self.shots_info.drop(self.shots_info.tail(1).index,inplace=True)
        self.undo = True


    def export_data(self):

        if self.shots_info.empty:
            messagebox.showerror('No Data','No data avalaible to export')
            return False

        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(),title='Save CSV', filetypes=(('CSV File','*.csv'),('All Files','*.*')))
        self.shots_info.to_csv(fln)       
        messagebox.showerror('Data Exported','Your data has been exported')

# main loop to run the program
def main():
    # create window
    root = tk.Tk()
    root.geometry("1500x800")  # arbitrary size
    root.title("xGStatsCreator")
    win = xGStatsCreator(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
