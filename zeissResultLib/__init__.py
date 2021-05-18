import os
import json
import time
import datetime as dt
from dateutil import tz
from lxml import etree as ET
from uuid import uuid1

class CmmFileHandler:
    headerData = {}
    setupData = {}
    chrData = {}
    fetData = {}
    hdrData = {}
    currentCmmFile = []
    zeissResultFileFolder = ""
    cmmResultFileFolder = ""
    planid = ""
    
    def __init__(self, zeissResultFileFolder, cmmResultFileFolder, planid, xmlResultFileFolder):
        self.planid = planid
        self.cmmResultFileFolder = cmmResultFileFolder
        self.zeissResultFileFolder = zeissResultFileFolder
        
        self.loadDialog()
        if self.headerData.get('operation') != "Setup":
            self.loadZeissTableFiles()
            self.saveCMM()


    def loadDialog(self):
        dialogPath = "\\".join([self.cmmResultFileFolder, self.planid, "dialog.json"])
        if os.path.isfile(dialogPath):
            with open(dialogPath, 'r') as f:
                print(f'[loading "{dialogPath}"] ', end="")
                temp = json.load(f)
                self.headerData.update(temp['Dialog'])
                self.setupData.update(temp['Setup'])
                print("Done")

        else:
            raise FileNotFoundError(f'"{dialogPath}" not found')

    def loadZeissTableFiles(self):
       
        zeissResultFiles = os.listdir(self.zeissResultFileFolder)
        if len(zeissResultFiles) < 3:
            
            raise FileNotFoundError("zeiss table files not found")

        for file in zeissResultFiles:
            if "chr" in file:
                print(f'[loading "{file}"] ', end="")
                self.chrData = self.loadCHR("\\".join([self.zeissResultFileFolder, file]))
                print("Done")
            if "fet" in file:
                print(f'[loading "{file}"] ', end="")
                self.fetData = self.loadFET("\\".join([self.zeissResultFileFolder, file]))
                print("Done")
            if "hdr" in file:
                print(f'[loading "{file}"] ', end="")
                self.hdrData = self.loadHDR("\\".join([self.zeissResultFileFolder, file]))
                self.headerData.update(self.hdrData)
                print("Done")


    def loadCHR(self, filename):
        if os.path.isfile(filename) and "chr" in filename:
            file = open(filename, 'r')
            fileContent = []
            temp = []

            for line in file:
                fileContent.append(line.split('\t'))

            for x,items in enumerate(fileContent[1:-1]):
                if len(items) > 1:
                    temp.append(dict(seq=x, idType=items[4], i_id=items[2], act=float(items[5]), nom=float(items[6]),
                                     utol=float(items[7]), ltol=float(items[8]), f_id=items[12], group=items[23],
                                     groups=';'.join(items[36:]).strip()))

            return temp
        else:
            return []


    def loadFET(self, filename):
        if os.path.isfile(filename) and "fet" in filename:
            file = open(filename, 'r')
            fetData = []
            fileContent = []
            for line in file:
                fileContent.append(line.split('\t'))
            for x,items in enumerate(fileContent[1:-1]):
                if len(items) > 1:
                    fetData.append(
                        dict(seq=x, idType=items[4], id=items[2], sigma=items[26], minDev=items[27], maxDev=items[28],
                            form=items[29], actx=items[8], acty=items[9], actz=items[10], acti=items[11],
                            actj=items[12], actk=items[13], nomx=items[36], nomy=items[37], nomz=items[38],
                            nomi=items[39], nomj=items[40], nomk=items[41], act_diameter=items[14],
                            act_diameter2=items[15], act_a1=items[16], act_a2=items[17], act_angle=items[18], 
                            act_apexAngle=items[19], nom_diameter=items[42], nom_diameter2=items[43], 
                            nom_a1=items[44], nom_a2=items[45], nom_angle=items[46], nom_apexAngle=items[47], alignment=items[34],
                            ioSign=items[24])
                    )
            return fetData
        else:
            return []

    
    def loadHDR(self, filename):
        if os.path.isfile(filename) and "hdr" in filename:
            file = open(filename, 'r')
            hdrData = []
            fileContent = []
            for line in file:
                fileContent.append(line.split('\t'))
            items = fileContent[1]
            hdrData = dict(dmeid=items[7], devicegroup=items[8], dmesn=items[9], controllertyp=items[10], dmeswi=items[11], dmeswv=items[12], partnb=items[1])
            return hdrData
        else:
            return []


    def loadCMM(self, filename):
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                temp = json.load(f)
            return temp


    def saveCMM(self):

        fileIndex = self.setupData.get("fileIndex", "MSN")
        print(f'[File Index is "{fileIndex}"]')
        self.resultFile = "\\".join([self.cmmResultFileFolder, self.planid, self.planid + "_" + self.headerData.get(fileIndex) + ".cmm"])
       
		
        now = dt.datetime.now()
        if os.path.isfile(self.resultFile):
            print(f'[loading "{self.resultFile}"] ', end="")
            self.currentCmmFile = self.loadCMM(self.resultFile)
            print("Done")
            print(f'[writing "{self.resultFile}"] ', end="")
            
            self.currentCmmFile[0].update(self.headerData)
            self.currentCmmFile[0]['chrData'] = self.updateEntry(self.currentCmmFile[0]['chrData'], self.chrData, "i_id")
            self.currentCmmFile[0]['fetData'] = self.updateEntry(self.currentCmmFile[0]['fetData'], self.fetData, "id")

            temp = {}
            temp['resultID'] = len(self.currentCmmFile)
            temp["date"] = now.strftime("%Y%m%d")
            temp["time"] = now.strftime("%H:%M:%S")
            temp.update(self.headerData)
            temp['endRun'] = time.time()
            temp['chrData'] = self.chrData
            temp['fetData'] = self.fetData
            self.currentCmmFile.append(temp)
            with open(self.resultFile, 'w') as f:
                json.dump(self.currentCmmFile, f, indent=2)
            
            with open(self.cmmResultFileFolder+'\\export\\'+ str(uuid1()) + '.json', 'w') as f:
                temp['runtime'] =  time.time() - self.headerData['startRun']
                temp['datetime'] = dt.datetime.now().isoformat()
                json.dump(temp, f)
            print("Done")

        else:
            print(f'[writing "{self.resultFile}"] ', end="")
            temp = {'resultID': 0, "date": now.strftime("%Y%m%d"), "time": now.strftime("%H:%M:%S")}
            temp.update(self.headerData)
            temp['endRun'] = time.time()
            temp['chrData'] = self.chrData
            temp['fetData'] = self.fetData
            self.currentCmmFile.append(temp)
            
            temp = {'resultID': 1, "date": now.strftime("%Y%m%d"), "time": now.strftime("%H:%M:%S")}
            temp.update(self.headerData)
            temp['endRun'] = time.time()
            temp['chrData'] = self.chrData
            temp['fetData'] = self.fetData
            self.currentCmmFile.append(temp)
            
            with open(self.resultFile, 'w') as f:
                json.dump(self.currentCmmFile, f, indent=2)
            
            with open(self.cmmResultFileFolder+'\\export\\'+ str(uuid1()) + '.json', 'w') as f:
                temp['runtime'] =  time.time() - self.headerData['startRun']
                temp['datetime'] = dt.datetime.now().isoformat()
                json.dump(temp, f)
            print("Done")

    def writeLog(self, filepath):
        pass

    def updateEntry(self, entry, data, id):
        for new_item in data:
            found = False
            for x, item in enumerate(entry):
                if item.get(id) == new_item.get(id):
                    entry[x].update(new_item)
                    found = True                    
            if found == False:
                entry.append(new_item)
                
        return entry



def loadDialog(filename):
    if os.path.isfile(filename) and "dialog" in filename:
        tree = ET.parse(filename)
        root = tree.getroot()
        dialog = root.find("dialog")
        dialogEntries = {}
        for dia in dialog.iter():
            dialogEntries.update({dia.tag:dia.text})
        del dialogEntries['dialog']

        return dialogEntries
    else:
        print("dialog file not found: " + filename)
        input()
        exit()

def loadFET(filename):
    if os.path.isfile(filename) and "fet" in filename:
        file = open(filename, 'r')
        fetData = []
        fileContent = []
        for line in file:
            fileContent.append(line.split('\t'))
        for x,items in enumerate(fileContent[1:-1]):
            if len(items) > 1:
                fetData.append(
                    dict(seq=x, idType=items[4], id=items[2], sigma=items[26], minDev=items[27], maxDev=items[28],
                         form=items[29], actx=items[8], acty=items[9], actz=items[10], acti=items[11],
                         actj=items[12], actk=items[13], nomx=items[36], nomy=items[37], nomz=items[38],
                         nomi=items[39], nomj=items[40], nomk=items[41], act_diameter=items[14],
                         act_diameter2=items[15], act_a1=items[16], act_a2=items[17], act_angle=items[18], 
                         act_apexAngle=items[19], nom_diameter=items[42], nom_diameter2=items[43], 
                         nom_a1=items[44], nom_a2=items[45], nom_angle=items[46], nom_apexAngle=items[47], alignment=items[34]
                         )
                )
        return fetData
    else:
        return []

def loadCHR(filename):
    if os.path.isfile(filename) and "chr" in filename:
        file = open(filename, 'r')
        fileContent = []
        temp = []

        for line in file:
            fileContent.append(line.split('\t'))

        for x,items in enumerate(fileContent[1:-1]):
            if len(items) > 1:
                temp.append(dict(seq=x, idType=items[4], i_id=items[2], act=items[5], nom=items[6], utol=items[7],ltol=items[8], f_id=items[12],group=items[23]))
        return temp
    else:
        return []


def loadHDR(filename):
    if os.path.isfile(filename) and "hdr" in filename:
        file = open(filename, 'r')
        hdrData = []
        fileContent = []
        for line in file:
            fileContent.append(line.split('\t'))
        items = fileContent[1]
        hdrData = dict(dmeid=items[7], devicegroup=items[8], dmesn=items[9], controllertyp=items[10], dmeswi=items[11], dmeswv=items[12], partnb=items[1])
        return hdrData
    else:
        return None

def updateEntry(entry, data):
    for new_item in data:
        found = False
        for x, item in enumerate(entry):
            if item.get('i_id') == new_item.get('i_id'):
                entry[x].update(new_item)
                found = True
            if item.get('id') == new_item.get('id'):
                entry[x].update(new_item)
                found = True
                
        if found == False:
            entry.append(new_item)
            
    return entry


def loadScanFiles(filenames):
    pass



