from gui_lib.container import Container
from gui_lib.label import Label
from gui_lib.listbox import Listbox
from client_lib.servercall import remote_call
from factuurList import factuurList
import curses

class verenigingListItem(Label):
    def __init__(self, width, vereniging_info, manager):
        self.manager = manager
        super(verenigingListItem,self).__init__(width, 1, vereniging_info[1].encode('utf-8'))
        self.vereniging_info = vereniging_info
    
    def keyEvent(self, key):
        if key == ord('\n'):
            self.manager.push(factuurList(1,1,
                remote_call('/factuur/vereniging',[('vereniging_id', self.vereniging_info[0])]),
                remote_call('/budget/vereniging',[('vereniging_id', self.vereniging_info[0])])[0]['current'],
                self.manager))
        
    def onFocus(self):
        self.setAttribute(curses.A_REVERSE)
        return True
    
    def offFocus(self):
        self.setAttribute(curses.A_NORMAL)


class verenigingList(Container):
    def __init__(self, width, height, vereniging_list, manager):
        super(verenigingList, self).__init__(width, height)
        self.manager = manager
        self.header = Label(width, 1, "Madmin ReTeX", curses.A_REVERSE)
        self.listbox = Listbox(width, height - 2)
        for vereniging_info in vereniging_list:
            self.listbox.append(verenigingListItem(width,vereniging_info,manager))
        self.headerId = self.addChild(0,0, self.header)
        self.listboxId = self.addChild(0,2,self.listbox)
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.header.resize(width, 1)
        self.listbox.resize(width, height-2)
