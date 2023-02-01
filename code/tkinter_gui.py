from tkinter import *
from tkinter import messagebox

"""
master = Tk()
master.geometry("200x100")
Label(master, text = "Fish").grid(row=0)
Label(master, text = "ID").grid(row=1, column=0)


menu_selection = StringVar(master)
menu_selection.set("cod") # default value
menu = OptionMenu(master, menu_selection, "cod", "haddock", "hake", "horse mackerel", "whiting", "saithe", "plaice", "lemon sole", "ling", "lubbe", "herring", "mackerel")
menu.grid(row=0, column=1)
#menu.pack()

button = Button(master, text = "OK", command=checkAnnotation).grid(row=2, column=1)

textEntered = StringVar()
text = Entry(master, textvariable=textEntered).grid(row=1, column= 1)

master.mainloop()
"""

class AnnotationApp():
    def __init__(self):
        self.master = None
        self.initWindow()

    def initWindow(self):
        self.master = Tk()
        self.master.geometry("200x100")

        Label(self.master, text = "Fish").grid(row=0, column=0)
        Label(self.master, text = "ID").grid(row=1, column=0)

        self.menu_selection = StringVar(self.master)
        #self.menu_selection.set("cod") #TO SET A DEFAULT VALUE
        menu = OptionMenu(self.master, self.menu_selection, "cod", "haddock", "hake", "horse mackerel", "whiting", "saithe", "plaice", "lemon sole", "ling", "lubbe", "herring", "mackerel")
        menu.grid(row=0, column=1)
        
        self.IDEntered = StringVar()
        text = Entry(self.master, textvariable=self.IDEntered).grid(row=1, column= 1)
        button = Button(self.master, text = "OK", command=self.checkAnnotation).grid(row=2, column=1)

        self.master.mainloop()

    #TODO Add check for 3 digits and menu_selection
    #TODO Add destroy call based on IF 
    #TODO Check if we can run this without mainloop https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
    def checkAnnotation(self):
        print(self.menu_selection.get())
        try:
            if float(self.IDEntered.get()).is_integer():
                _id = int(self.IDEntered.get())
                if _id < 0:
                    self.showErrorMsg("ID cannot be negative value")
                else:
                    print(type(_id))
                    print(_id)
            else:
                self.showErrorMsg("ID cannot be float")
                #self.warning()
        except Exception as e:
            #print(e)
            self.showErrorMsg(e)
            #self.warning()

        self.master.destroy()

    def showErrorMsg(self, text):
        messagebox.showerror("Error", text)

    def quit(self):
        self.master.quit()

    def destroy(self):
        self.master.destroy()

annotationWindow = AnnotationApp()
#print(annotationWindow.menu_selection.get())
#print(annotationWindow.IDEntered.get())