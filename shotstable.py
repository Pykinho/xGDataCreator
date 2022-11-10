import tkinter as tk
from tkinter import ttk

class ShotsTable(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.count = 0
        self.trees = []

        frame = tk.LabelFrame(self,relief = 'groove',text='CHOOSE AN ATTACKING TEAM',padx=20,pady=20)
        frame.grid(row=0,column=0)

        shotsTree = ttk.Treeview(self)

        #define columns
        shotsTree['columns'] = ('Category','Distance','Angle','XG','Goal')

        #Format columns
        shotsTree.column('#0',width=0,stretch='no')
        shotsTree.column('Category',anchor = 'center',width=100,minwidth=25)
        shotsTree.column('Distance',anchor = 'center',width=60,minwidth=25)
        shotsTree.column('Angle',anchor='center',width=60,minwidth=25)
        shotsTree.column('XG',anchor='center',width=60,minwidth=25)
        shotsTree.column('Goal',anchor='center',width=60,minwidth=25)

        #Create Headings
        shotsTree.heading('#0',text='',anchor='w')
        shotsTree.heading('Category',text='Category',anchor='w')
        shotsTree.heading('Distance',text='Distance',anchor='center')
        shotsTree.heading('Angle',text='Angle',anchor='w')
        shotsTree.heading('XG',text='XG',anchor='w')
        shotsTree.heading('Goal',text='Goal',anchor='w')

        shotsTree.grid(row=0,column=0)

        self.trees.append(shotsTree)

        #vertical scrollbar
        scrollbar = ttk.Scrollbar(self,orient='vertical',command=shotsTree.yview)
        shotsTree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        #Add data
    def update_table(self,category,distance,angle,xg,goal):
        self.trees[0].insert(parent='',index='0',iid=self.count,text='',
            values=(category,round(distance,2),round(angle,2),round(xg,2),goal))
        self.count += 1

    def clear_all(self):
        for item in self.trees[0].get_children():
            self.trees[0].delete(item)
    
    def undo(self):
        if len(self.trees[0].get_children())>0:
            item = self.trees[0].get_children()[0]
            self.trees[0].delete(item)
            self.count -= 1