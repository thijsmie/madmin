from gui_lib.container import Container
from gui_lib.label import Label
from gui_lib.listbox import Listbox
from factuurList import factuurList
from verenigingNaamCoupler import getVerenigingNaam
import curses

class factuurOverigeListItem(Label):
    def __init__(self, width, name, facturen, manager):
        self.manager = manager
        super(factuurOverigeListItem, self).__init__(
                width, 1,
                name)
        self.facturen = facturen

    def keyEvent(self, key):
        if key == ord('\n'):
            self.manager.push(factuurList(1,1,
                    self.facturen,
                    self.manager))

    def onFocus(self):
        self.setAttribute(curses.A_REVERSE)
        return True

    def offFocus(self):
        self.setAttribute(curses.A_NORMAL)

class factuurOverigeList(Container):
    def __init__(self, width, height, facturen, manager):
        super(factuurOverigeList, self).__init__(width, height)
        self.manager = manager
        self.header = Label(width, 1, "Leveranciers en overige", curses.A_REVERSE)
        self.factuurOverigeListbox = Listbox(width, height-2)
        self.groups = {}
        self.ordering = []
        for factuur in reversed(facturen):
            if factuur["leverancier"] not in self.groups.keys():
                self.groups[factuur["leverancier"]] = []
                self.ordering.append(factuur["leverancier"])
            self.groups[factuur["leverancier"]].append(factuur)
        for key in self.ordering:
            self.factuurOverigeListbox.append(factuurOverigeListItem(width, str(key), self.groups[key][::-1], manager))

        self.factuurOverigeListboxIndex = self.addChild(0,2, self.factuurOverigeListbox)
        self.headerIndex = self.addChild(0,0, self.header)

    def keyEvent(self, key):
        if key == curses.KEY_BACKSPACE:
            self.manager.pop()
        else:
            super(factuurOverigeList,self).keyEvent(key)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.header.resize(width, 1)
        self.factuurOverigeListbox.resize(width, height-2)
