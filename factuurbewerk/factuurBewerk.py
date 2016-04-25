from factuurInfoBox import FactuurInfoBox
from factuurInputRegel import FactuurInputHeader
from factuurRegelList import FactuurRegelList
from gui_lib.container import Container
from gui_lib.label import Label
from gui_lib.button import Button
from gui_lib.core import unsetCursor
from client_lib.servercall import remote_call, ServerCallException

class FactuurBewerk(Container):
    def __init__(self, width, height, factuur, manager):
        super(FactuurBewerk, self).__init__(width, height)

        self.factuurInfoBox = FactuurInfoBox(1,1, factuur)
        self.factuurListHeader = FactuurInputHeader(1,1)
        self.factuurRegelList = FactuurRegelList(1,1)
        self.statusLine = Label(1,1,"")
        self.submitButton = Button(1,1,self.sendEdit,"Submit")

        self.factuurListHeaderIdx = self.addChild(0,0, self.factuurListHeader)
        self.statusLineIdx = self.addChild(0,0,self.statusLine)
        self.submitButtonIdx = self.addChild(0,0,self.submitButton)
        self.factuurInfoBoxIdx = self.addChild(0,0, self.factuurInfoBox)
        self.factuurRegelListIdx = self.addChild(0,0,self.factuurRegelList)

        self.factuur = factuur
        self.manager = manager

        self.resize(width, height)

    def resize(self, width, height):
        self.width = width
        self.height = height

        vOffset = 0

        self.factuurInfoBox.resize(width, 1)
        self.setChildPos(self.factuurInfoBoxIdx, 0, 0)
        vOffset += self.factuurInfoBox.size()[1]

        self.factuurListHeader.resize(width, 1)
        self.setChildPos(self.factuurListHeaderIdx, 0, vOffset)
        vOffset += 1

        self.factuurRegelList.resize(width, height - vOffset-1)
        self.setChildPos(self.factuurRegelListIdx, 0, vOffset)
        vOffset = height-1

        self.submitButton.resize(min(width, 6), 1)
        self.setChildPos(self.submitButtonIdx, 1, vOffset)
        self.statusLine.resize(width-min(width, 8), 1)
        self.setChildPos(self.statusLineIdx, min(width, 8), vOffset)


    def sendEdit(self):
        result = self.generateRegels()

        if not result[0]:
            self.statusLine.setText(result[2])
            return

        if not result[1]:
            self.statusLine.setText("Insufficient input given")
            return

        try:
            data = {}
            data["factuur_id"] = factuur["id"]
            data["regels"] = result[2]
            submitResult = remote_call('/factuur/bewerk', jsondata = data)
        except ServerCallException:
            self.statusLine.setText("Kon geen verbinding maken met server.")
            return

        if 'error' in submitResult:
            self.statusLine.setText(submitResult['error'].encode('utf-8'))
            return

        self.statusLine.setText("")
        unsetCursor()
        self.manager.pop()

        self.resize(self.width, self.height)

    def generateRegels(self):

        result = self.factuurRegelList.generateFactuurRegels(self.factuur['type'] == 'inkoop')

        if not result[0] or not result[1]:
            return result

        return (True, True, result[2])
