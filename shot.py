#class responsible for creating shot points

pitch_size = 7

class Shot:

    def __init__(self, canvas, x, y, team, goal):

        self.x = x
        self.y = y
        
        self.team = team
        self.goal = goal

        if self.team == 'HOME':
            self.current_colour = 'Red'

            self.calcX = (105*pitch_size+2*pitch_size - self.x-pitch_size)/pitch_size
            self.calcY = abs(self.y-(34*pitch_size+pitch_size))/pitch_size
      
        else:
            self.current_colour = 'Blue'
            self.calcX = (self.x-pitch_size)/pitch_size
            self.calcY = abs(self.y-(34*pitch_size+pitch_size))/pitch_size

        if self.goal == True:
            self.point = canvas.create_rectangle(x-5,y-5,x+5,y+5,fill=self.current_colour,tags="shots")
        else:    
            self.point = canvas._create_circle(x,y,5,fill=self.current_colour,tags="shots")
        
    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)