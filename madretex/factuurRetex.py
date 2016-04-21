#MadminToConscribo.py

#Standard Library imports
from math import copysign
import getpass
import os
import subprocess
import sys

#Madmin imports:
import verenigingNaamCoupler as vrn
import productNaamCoupler as prd

#Helper modules imports
from template import template


#Helper function definitions
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def parse_money(text):
    value = 0
    
    segments = text.split(',')
    if len(segments) > 2:
        return (False, 0)
        
    euros = 0
    cents = 0
    for i in range(0, len(segments[0])):
        if segments[0][i] < '0' or segments[0][i] > '9':
            return (False, 0)
        euros *= 10
        euros += ord(segments[0][i]) - ord('0')
    
    if len(segments) == 2:
        if len(segments[1]) > 2:
            return (False, 0)
        for i in range(0, len(segments[1])):
            if segments[1][i] < '0' or segments[1][i] > '9':
                return (False, 0)
            cents *= 10
            cents += ord(segments[1][i]) - ord('0')
    
        if len(segments[1]) == 1:
            cents *= 10;
    
    value = euros*100 + cents
    
    return (True, value)
    
def tex_escape(text):
    CHARS = {
        '&':  r'\&',
        '%':  r'\%', 
        '$':  r'\$', 
        '#':  r'\#', 
        '_':  r'\letterunderscore{}', 
        '{':  r'\letteropenbrace{}', 
        '}':  r'\letterclosebrace{}',
        '~':  r'\lettertilde{}', 
        '^':  r'\letterhat{}', 
        '\\': r'\letterbackslash{}',
    }

    return "".join([CHARS.get(char, char) for char in text])

def _moneyConvert(value):
        cents = value % 100
        value /= 100
        if cents < 10:
            return str(value)+ ",0" + str(cents)
        return str(value) + "," + str(cents)
        
def factuurRetex(factuur, budget):
    #process regels
    regels = ""
    totaal = 0
    indx = 0
    for regel in factuur['regels']:
        indx+=1
        if 'naam' in regel:
            naam = regel['naam']
        else:
            naam = prd.getProductNaam(regel['product_id'])
        regels += naam + " & " + str(regel['aantal']) + " & " 
        regels += _moneyConvert(regel['stukprijs']) + " & " + _moneyConvert(regel['totaalprijs']) + "\\\\\n"
        totaal += copysign(regel['totaalprijs'], regel['aantal'])

    info = {}
    _assoc = vrn.getVerenigingNaam(factuur['vereniging_id']).encode('utf-8')
    info['factuurregels'] = regels
    info['vereniging'] = _assoc
    info['factuurnummer'] = factuur['volgnummer']
    info['factuurdatum'] = factuur['factuurdatum']
    info['afnamedatum'] = factuur['leverdatum']
    info['totaal'] = totaal / 100.0
    if 'verantwoordelijke' in factuur:
        info['verantwoordelijke'] = tex_escape(factuur['verantwoordelijke'])
    else:
        info['verantwoordelijke'] = ""

    if 'saldo_basis_na' in factuur:
        info['borrelsaldo'] = budget/100.0
    else:
        info['borrelsaldo'] = 0.0
        
    budget += totaal

    if 'saldo_speciaal' in factuur:
        info['speciaalsaldo'] = ""
        info['speciaalsaldona'] = factuur['saldo_speciaal_na'] / 100.0
    else:
        info['speciaalsaldo'] = ""
        info['speciaalsaldona'] = 0.0
        
    clear()
    path = "/".join(sys.argv[0].split("/")[:-1])
    info['path'] = path
    texCode = template % info

    texFilename = path + "/" + "facturen/" + _assoc + "_" + str(info['factuurnummer']) + ".tex"
    auxFilename = path + "/" + _assoc + "_" + str(info['factuurnummer']) + ".aux"
    logFilename = path + "/" + _assoc + "_" + str(info['factuurnummer']) + ".log"
    pdfFilename = path + "/" + _assoc + "_" + str(info['factuurnummer']) + ".pdf"
    pdf2Filename = path + "/" + "facturen/" + _assoc + "_" + str(info['factuurnummer']) + ".pdf"
    
    texfile = open(texFilename, "w")
    texfile.write(texCode)
    texfile.close()

    if subprocess.check_call(["pdflatex", texFilename],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE) != 0:
        print "Was unable to compile PDF."
        sys.exit()
    else:
        print "Pdf produced"
        os.system("mv " + pdfFilename + " " + pdf2Filename)
        os.system("rm " + auxFilename)
        os.system("rm " + logFilename)
    
    return budget


