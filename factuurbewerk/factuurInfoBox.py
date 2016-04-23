from gui_lib.container import Container
from gui_lib.label import Label
from gui_lib.fill import Fill
from verenigingNaamCoupler import getVerenigingNaam
from math import copysign
import curses

class FactuurInfoBox(Container):
    def __init__(self, width, height, factuur):
        super(FactuurInfoBox, self).__init__(width, height)

        #Associated data object
        self.factuur = factuur

        #Layout settings
        self.labelWidth = 19
        self.minValueWidth = 20

        if 'vereniging_id' in factuur:
            self.otherPartyLabel = Label(0,1,"Vereniging:")
            self.otherPartyValue = Label(0,1,getVerenigingNaam(factuur['vereniging_id']).encode('utf-8'))
        else:
            self.otherPartyLabel = Label(0,1,"Leverancier:")
            self.otherPartyValue = Label(0,1,factuur['leverancier'].encode('utf-8'))
        self.volgnummerLabel = Label(0,1,"Volgnummer:")
        self.volgnummerValue = Label(0,1,str(factuur['volgnummer']))

        self.factuurDatumLabel = Label(0,1,"Factuurdatum:")
        self.factuurDatumValue = Label(0,1,factuur['factuurdatum'].encode('utf-8'))
        self.leverDatumLabel = Label(0,1, "Leverdatum:")
        self.leverDatumValue = Label(0,1,factuur['leverdatum'].encode('utf-8'))

        self.separatorFill = Fill(0,0,'|')
        self.separatorFillIdx = self.addChild(0,0,self.separatorFill)

        self.hasVerantwoordelijke = False
        if 'verantwoordelijke' in factuur:
            self.hasVerantwoordelijke = True
            self.verantwoordelijkeLabel = Label(0,1,"Verantwoordelijke:")
            self.verantwoordelijkeValue = Label(0,1,factuur['verantwoordelijke'].encode('utf-8'))

        self.otherPartyLabelIdx = self.addChild(0,0,self.otherPartyLabel)
        self.otherPartyValueIdx = self.addChild(0,0,self.otherPartyValue)
        self.volgnummerLabelIdx = self.addChild(0,0,self.volgnummerLabel)
        self.volgnummerValueIdx = self.addChild(0,0,self.volgnummerValue)
        self.factuurDatumLabelIdx = self.addChild(0,0,self.factuurDatumLabel)
        self.factuurDatumValueIdx = self.addChild(0,0,self.factuurDatumValue)
        self.leverDatumLabelIdx = self.addChild(0,0,self.leverDatumLabel)
        self.leverDatumValueIdx = self.addChild(0,0,self.leverDatumValue)
        if self.hasVerantwoordelijke:
            self.verantwoordelijkeLabelIdx = self.addChild(0,0,self.verantwoordelijkeLabel)
            self.verantwoordelijkeValueIdx = self.addChild(0,0,self.verantwoordelijkeValue)

        self.resize(width, 0)

    def resize(self, width, height):
        #ignore height, we determine that ourselves
        self.width = width

        if (self.width - 1)/2 - self.labelWidth >= self.minValueWidth:
            #two column layout
            colWidth = (self.width-1)/2
            colOffset = colWidth+1
            valueWidth = max(0, colWidth-self.labelWidth)

            self.separatorFill.resize(1,2)
            self.setChildPos(self.separatorFillIdx, colWidth,0)

            self.otherPartyLabel.resize(self.labelWidth,1)
            self.setChildPos(self.otherPartyLabelIdx,0,0)
            self.otherPartyValue.resize(valueWidth, 1)
            self.setChildPos(self.otherPartyValueIdx,self.labelWidth,0)

            self.volgnummerLabel.resize(self.labelWidth,1)
            self.setChildPos(self.volgnummerLabelIdx,0,1)
            self.volgnummerValue.resize(valueWidth, 1)
            self.setChildPos(self.volgnummerValueIdx,self.labelWidth,1)

            self.factuurDatumLabel.resize(self.labelWidth,1)
            self.setChildPos(self.factuurDatumLabelIdx, colOffset,0)
            self.factuurDatumValue.resize(valueWidth,1)
            self.setChildPos(self.factuurDatumValueIdx, colOffset + self.labelWidth,0)

            self.leverDatumLabel.resize(self.labelWidth,1)
            self.setChildPos(self.leverDatumLabelIdx, colOffset,1)
            self.leverDatumValue.resize(self.labelWidth,1)
            self.setChildPos(self.leverDatumValueIdx, colOffset + self.labelWidth, 1)

            if self.hasVerantwoordelijke:
                self.height = 3
                self.verantwoordelijkeLabel.resize(self.labelWidth,1)
                self.setChildPos(self.verantwoordelijkeLabelIdx, 0, 2)
                self.verantwoordelijkeValue.resize(width-self.labelWidth,1)
                self.setChildPos(self.verantwoordelijkeValueIdx, self.labelWidth, 2)
            else:
                self.height = 2
        else:
            #one column layout
            valueWidth = max(0, width-self.labelWidth)

            self.separatorFill.resize(0,0)
            self.setChildPos(self.separatorFillIdx, 0,0)

            self.otherPartyLabel.resize(self.labelWidth, 1)
            self.setChildPos(self.otherPartyLabelIdx,0,0)
            self.otherPartyValue.resize(valueWidth, 1)
            self.setChildPos(self.otherPartyValueIdx,self.labelWidth,0)

            self.volgnummerLabel.resize(self.labelWidth, 1)
            self.setChildPos(self.volgnummerLabelIdx,0,1)
            self.volgnummerValue.resize(valueWidth, 1)
            self.setChildPos(self.volgnummerValueIdx,self.labelWidth,1)

            self.factuurDatumLabel.resize(self.labelWidth, 1)
            self.setChildPos(self.factuurDatumLabelIdx,0,2)
            self.factuurDatumValue.resize(valueWidth, 1)
            self.setChildPos(self.factuurDatumValueIdx,self.labelWidth,2)

            self.leverDatumLabel.resize(self.labelWidth,1)
            self.setChildPos(self.leverDatumLabelIdx,0,3)
            self.leverDatumValue.resize(valueWidth,1)
            self.setChildPos(self.leverDatumValueIdx,self.labelWidth,3)

            if self.hasVerantwoordelijke:
                self.height = 5
                self.verantwoordelijkeLabel.resize(self.labelWidth, 1)
                self.setChildPos(self.verantwoordelijkeLabelIdx,0,4)
                self.verantwoordelijkeValue.resize(valueWidth,1)
                self.setChildPos(self.verantwoordelijkeValueIdx,self.labelWidth,4)
            else:
                self.height = 4
