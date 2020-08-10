import os
from lxml import etree as ET
from datetime import datetime
import json


class zeissContainer(object):
    m_data = {}

    def loadFET(self, filename):
        """
            loadFET(filename) loads zeiss table file _fet.txt and converts it to json
        """
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
            self.m_data.update({'fetData': fetData})


    def loadCHR(self, filename):
        """
            loadCHR(filename) loads zeiss table file _chr.txt and converts it to json
        """
        if os.path.isfile(filename) and "chr" in filename:
            file = open(filename, 'r')
            chrData = []
            fileContent = []
            for line in file:
                fileContent.append(line.split('\t'))
            for x,items in enumerate(fileContent[1:-1]):
                if len(items) > 1:
                    chrData.append(dict(seq=x, idType=items[4], i_id=items[2], act=items[5], nom=items[6], utol=items[7],ltol=items[8], f_id=items[12],group=items[23]))
        
            self.m_data.update({'chrData': chrData})


    def loadHDR(self, filename):
        """
            loadHDR(filename) loads zeiss table file _hdr.txt and converts it to json
        """        
        if os.path.isfile(filename) and "hdr" in filename:
            file = open(filename, 'r')
            hdrData = []
            fileContent = []
            for line in file:
                fileContent.append(line.split('\t'))
            items = fileContent[1]
            hdrData = dict(dmeid=items[7], devicegroup=items[8], dmesn=items[9], controllertyp=items[10], dmeswi=items[11], dmeswv=items[12], partnb=items[1])
            self.m_data.update(hdrData)


    def loadDialog(self, filename):
        """
            loadDialog(file) loads Dialog.xml file
        """
        print(f'loading: ${filename}')
        if os.path.isfile(filename) and "dialog" in filename:
            tree = ET.parse(filename)
            root = tree.getroot()
            dialog = root.find("dialog")
            dialogEntries = {}
            for dia in dialog.iter():
                dialogEntries.update({dia.tag:dia.text})
            del dialogEntries['dialog']
            dialogEntries['endtime'] = datetime.now().isoformat()
            print(dialogEntries)
            self.m_data.update(dialogEntries)

