from gui_lib.container import Container
from gui_lib.label import Label
from gui_lib.listbox import Listbox
from factuurDetail import factuurDetail
from verenigingNaamCoupler import getVerenigingNaam
import curses

class factuurListItem(Label):
    def __init__(self, width, factuur, manager):
        self.manager = manager
        if 'vereniging_id' in factuur:
            super(factuurListItem, self).__init__(
                    width, 1,
                    getVerenigingNaam(factuur['vereniging_id']).encode('utf-8') +
                            " " + str(factuur['volgnummer']))
        else:
            super(factuurListItem, self).__init__(
                    width, 1,
                    factuur['leverancier'].encode('utf-8') + " " + str(factuur['volgnummer']))
        self.factuur = factuur

    def keyEvent(self, key):
        if key == ord('\n'):
            self.manager.push(factuurDetail(1,1,self.factuur, self.manager))

    def onFocus(self):
        self.setAttribute(curses.A_REVERSE)
        return True

    def offFocus(self):
        self.setAttribute(curses.A_NORMAL)

class factuurList(Container):
    def __init__(self, width, height, facturen, manager):
        super(factuurList, self).__init__(width, height)
        if 'vereniging_id' in facturen[0]:
            self.name = getVerenigingNaam(facturen[0]['vereniging_id']).encode('utf-8')
        else:
            self.name = "Leveranciers en overige"
        self.manager = manager
        self.header = Label(width, 1, self.name, curses.A_REVERSE)
        self.factuurListbox = Listbox(width, height-2)
        for factuur in reversed(facturen):
            self.factuurListbox.append(factuurListItem(width, factuur, manager))

        self.factuurListboxIndex = self.addChild(0,2, self.factuurListbox)
        self.headerIndex = self.addChild(0,0, self.header)

    def keyEvent(self, key):
        if key == curses.KEY_BACKSPACE:
            self.manager.pop()
        else:
            super(factuurList,self).keyEvent(key)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.header.resize(width, 1)
        self.factuurListbox.resize(width, height-2)
