#class responsible for drawing a pitch and recording shots

import tkinter as tk
from shot import Shot
pitch_size = 7

class PitchShots(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.shots_locations = []
        self.team = 'HOME'
        self.category = 'OPEN PLAY'
        self.goal = False
        self.home_goals = 0
        self.away_goals = 0
        self.home_xg = 0.00
        self.away_xg = 0.00
        self.home_label = self.create_text(105*pitch_size/2-8*pitch_size,4*pitch_size, text='HOME ',fill="red", font=('Impact 30'))
        self.away_label = self.create_text(105*pitch_size/2+11*pitch_size,4*pitch_size, text='AWAY ',fill="blue", font=('Impact 30'))
        self.home_score = self.create_text(105*pitch_size/2-8*pitch_size,8*pitch_size, text='0 (0.0)',fill="red", font=('Impact ' + str(pitch_size*4)),tags='score',)
        self.away_score = self.create_text(105*pitch_size/2+11*pitch_size,8*pitch_size, text='0 (0.0)',fill="blue", font=('Impact ' + str(pitch_size*4)),tags='score')
        
        # Create the canvas and make it visible with pack()
        self.config(highlightthickness=1, highlightbackground="black")
        self.config(width=(105*pitch_size+2*pitch_size), height=(68*pitch_size+2*pitch_size), background="white")

        # record clicks on canvas only.
        self.bind("<Button-1>", self.click)

        self.create_pitch()

    # Function clear all data
    def reset_points(self):
        # reset data
        self.delete("shots")
        self.shots_locations.clear()
        self.home_goals = 0
        self.home_xg = 0.0
        self.away_goals = 0
        self.away_xg = 0.0

        #clear dataframe
        self.master.clear_shots()
        # update gui
        self.master.update_data(self.shots_locations)
        self.update_score()
        

    def undo(self):
        if len(self.shots_locations) > 0:
            
            #clear dataframe
            team = [shot.team for shot in self.shots_locations]
            self.master.undo_shots(team[-1])

            # delete the shot_location
            del self.shots_locations[-1]
            # delete the last element from the canvas
            self.delete(list(self.find_withtag("shots"))[-1])
            self.update_score()
            del team[-1]
            # update the gui text
            self.master.update_data(self.shots_locations)

    # Records click events and updates the screen
    def click(self, event):
        # create a new shot
        if self.category == 'PENALTY KICK':
            if self.team == 'HOME':
                self.shots_locations.append(Shot(self, 94*pitch_size+pitch_size, 34*pitch_size+pitch_size,self.team,self.goal))
            else:
                self.shots_locations.append(Shot(self, 11*pitch_size+pitch_size, 34*pitch_size+pitch_size,self.team,self.goal))
        else:
            self.shots_locations.append(Shot(self, event.x, event.y,self.team,self.goal))
        # update the gui
        self.master.update_data(self.shots_locations)
        self.update_score()

    #update a score on a canvas
    def update_score(self):
        self.delete('score')
        self.home_score = self.create_text(105*pitch_size/2-8*pitch_size,8*pitch_size, text=str(self.home_goals) + ' (' + str(round(self.home_xg,2)) + ')', fill="red", font=('Impact ' + str(pitch_size*4)),tags='score')
        self.away_score = self.create_text(105*pitch_size/2+11*pitch_size,8*pitch_size, text=str(self.away_goals)  + ' (' + str(round(self.away_xg,2)) + ')',fill = 'blue',font=('Impact ' + str(pitch_size*4)),tags='score')

    #drawing a pitch on a canvas
    def create_pitch(self):

        #outline and center line
        self.create_line([pitch_size,pitch_size,105*pitch_size+pitch_size,pitch_size],fill='black',width=1)
        self.create_line([pitch_size,pitch_size,pitch_size,68*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([pitch_size,68*pitch_size+pitch_size,105*pitch_size+pitch_size,68*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([105*pitch_size+pitch_size,pitch_size,105*pitch_size+pitch_size,68*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([(105*pitch_size/2+pitch_size),pitch_size,105*pitch_size/2+pitch_size,68*pitch_size+pitch_size],fill='black',width=1)

        #left penalty box
        self.create_line([16.5*pitch_size + pitch_size,14*pitch_size+pitch_size,16.5*pitch_size + pitch_size,54*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([pitch_size,14*pitch_size+pitch_size,16.5*pitch_size + pitch_size,14*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([pitch_size,54*pitch_size+pitch_size,16.5*pitch_size + pitch_size,54*pitch_size+pitch_size],fill='black',width=1)

        #right penalty box
        self.create_line([88.5*pitch_size+pitch_size,14*pitch_size+pitch_size,88.5*pitch_size+pitch_size,54*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([88.5*pitch_size+pitch_size,14*pitch_size+pitch_size,105*pitch_size+pitch_size,14*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([88.5*pitch_size+pitch_size,54*pitch_size+pitch_size,105*pitch_size+pitch_size,54*pitch_size+pitch_size],fill='black',width=1)

        #left 5 meter box
        self.create_line([5.5*pitch_size+pitch_size,25*pitch_size+pitch_size,5.5*pitch_size+pitch_size,43*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([pitch_size,25*pitch_size+pitch_size,5.5*pitch_size+pitch_size,25*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([pitch_size,43*pitch_size+pitch_size,5.5*pitch_size+pitch_size,43*pitch_size+pitch_size],fill='black',width=1)

        #right 5 meter box
        self.create_line([99.5*pitch_size+pitch_size,25*pitch_size+pitch_size,99.5*pitch_size+pitch_size,43*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([99.5*pitch_size+pitch_size,25*pitch_size+pitch_size,105*pitch_size+pitch_size,25*pitch_size+pitch_size],fill='black',width=1)
        self.create_line([99.5*pitch_size+pitch_size,43*pitch_size+pitch_size,105*pitch_size+pitch_size,43*pitch_size+pitch_size],fill='black',width=1)

        #left penalty spot
        self._create_circle(11*pitch_size+pitch_size,34*pitch_size+pitch_size,pitch_size/2,outline='black',fill='black')
        #right penalty spot
        self._create_circle(94*pitch_size+pitch_size,34*pitch_size+pitch_size,pitch_size/2,outline='black',fill='black')
        #pitch center circle
        self._create_circle(105*pitch_size/2+pitch_size,34*pitch_size+pitch_size,9.15*pitch_size,outline='black')
        #pitch center spot
        self._create_circle(105*pitch_size/2+pitch_size,34*pitch_size+pitch_size,pitch_size/2,outline='black',fill='black')

        #left arc
        self._create_circle_arc(16.5*pitch_size + pitch_size, 34*pitch_size+pitch_size, 3.65*pitch_size, outline="black", start=270, end=450)

        #right arc
        self._create_circle_arc(88.5*pitch_size+pitch_size, 34*pitch_size+pitch_size, 3.65*pitch_size, outline="black", start=90, end=270)

        #left goal
        self.create_line([pitch_size,30.5*pitch_size+pitch_size,pitch_size,37.82*pitch_size+pitch_size],fill='red',width=2)
        #right goal
        self.create_line([105*pitch_size+pitch_size,30.5*pitch_size+pitch_size,105*pitch_size+pitch_size,37.82*pitch_size+pitch_size],fill='blue',width=2)



    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def _create_circle_arc(self, x, y, r, **kwargs):
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            del kwargs["end"]
        return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
        


