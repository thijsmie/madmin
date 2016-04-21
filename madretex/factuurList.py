from gui_lib.container import Container
from gui_lib.label import Label
from gui_lib.listbox import Listbox
from verenigingNaamCoupler import getVerenigingNaam
from factuurRetex import factuurRetex
import curses


class factuurListItem(Label):
    def __init__(self, width, factuur, manager, number, ppointer):
        self.manager = manager
        super(factuurListItem, self).__init__(
            width, 1, 
            getVerenigingNaam(factuur['vereniging_id']).encode('utf-8') +
                " " + str(factuur['volgnummer']))
        self.factuur = factuur
        self.number = number
        self.ppointer = ppointer
        self.final = False
    
    def keyEvent(self, key):
        if key == ord('\n'):
            for i in range(self.number, 0, -1):
                self.ppointer.budget = factuurRetex(self.ppointer.facturen[i], self.ppointer.budget)
            
                
    def onFocus(self):
        self.setAttribute(curses.A_REVERSE)
        return True
    
    def offFocus(self):
        self.setAttribute(curses.A_NORMAL)

class factuurList(Container):
    def __init__(self, width, height, facturen, budget, manager):
        super(factuurList, self).__init__(width, height)
        self.manager = manager
        self.factuurListbox = Listbox(width, height)
        self.facturen = facturen[::-1]
        self.budget = budget
        for a in range(len(self.facturen)):
            self.factuurListbox.append(factuurListItem(width, self.facturen[a], manager, a, self))
        
        self.factuurListboxIndex = self.addChild(0,0, self.factuurListbox)
    
    def keyEvent(self, key):
        if key == curses.KEY_BACKSPACE:
            self.manager.pop()
        else:
            super(factuurList,self).keyEvent(key)
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.factuurListbox.resize(width, height)
