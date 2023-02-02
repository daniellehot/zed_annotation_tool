from tkinter import *
from tkinter import messagebox
import math

class AnnotationApp():
    def __init__(self):
        self.master = None
        self.initWindow()
        self.id = -1
        self.species = None
        #self.breakTheLoop = False
        self.cancelled = None

    def initWindow(self):
        self.master = Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.onClose)
        self.master.geometry("200x100")

        Label(self.master, text = "Fish").grid(row=0, column=0)
        Label(self.master, text = "ID").grid(row=1, column=0)

        self.menuSelection = StringVar(self.master)
        #self.menuSelection.set("cod") #TO SET A DEFAULT VALUE
        menu = OptionMenu(self.master, self.menuSelection, "cod", "haddock", "hake", "horse mackerel", "whiting", "saithe", "plaice", "lemon sole", "ling", "lubbe", "herring", "mackerel")
        menu.grid(row=0, column=1)
        
        self.idEntered = StringVar()
        text = Entry(self.master, textvariable=self.idEntered).grid(row=1, column= 1)
        button = Button(self.master, text = "OK", command=self.checkAnnotation).grid(row=2, column=1)
        #self.master.mainloop()

    def checkAnnotation(self):
        valid_ID = self.checkID(self.idEntered.get())
        valid_species = self.checkMenuSelection(self.menuSelection.get())
        if valid_ID and valid_species:
            self.id = self.idEntered.get()
            self.species = self.menuSelection.get()
    
    def checkID(self, str):
        try:
            if float(str).is_integer():
                _id = int(str)
                if _id < 0:
                    self.showErrorMsg("ID must be an int from 0 to 999")
                    return False
                else:
                    _digits = int(math.log10(_id))+1
                    if _digits > 3:
                        self.showErrorMsg("ID must be an int from 0 to 999")
                        return False
                    else:
                        return True
            else:
                self.showErrorMsg("ID must be an int from 0 to 999")
                return False
        except Exception as e:
            self.showErrorMsg("ID must be an int from 0 to 999")
            return False

    def checkMenuSelection(self, str):
        if len(str) == 0:
            self.showErrorMsg("Select a species")
            return False
        else:  
            return True

    def showErrorMsg(self, text):
        messagebox.showerror("Error", text)
    
    def onClose(self):
        #self.breakTheLoop = True
        self.cancelled = True
        #self.master.quit()
        
    """
    def updateGUI(self):
        self.master.update_idletasks()
        self.master.update()

    def quit(self):
        self.master.quit()

    def destroy(self):
        self.master.destroy()
    """

# https://gordonlesti.com/use-tkinter-without-mainloop/
if __name__ == "__main__":
    i = 0
    annotationWindow = AnnotationApp()
    while True:
        print(i, "Before tkinter loop")
        while not annotationWindow.breakTheLoop:
            annotationWindow.master.update()
            if annotationWindow.id != -1 and annotationWindow.species != None:
                print(annotationWindow.id)
                print(annotationWindow.species)
                annotationWindow.master.quit()
                annotationWindow.breakTheLoop = True 
        i = i + 1 
        print(i, "After tkinter loop")
        if i == 50:
            break
        