import os
import datetime
import sys, traceback
import zeissResultLib as zrl
import json
import pprint


results = []
chrData = []
fetData = []
hdrData = []
dialogData = []
pd = ""
rd = ""
fd = ""
planid = ""
scanfiles = ""

# -pd option: folder for dialog.xml file which is at the moment still in the results folder, but will be switch to the new folder structure
# -fd option: where Calypso exports its result files (chr.txt, fet.txt, hdr.txt)

if __name__ == "__main__":

    for x, arg in enumerate(sys.argv):
        if "-fd" in arg:
            fd = sys.argv[x+1]
            filelist = os.listdir(fd)
            if len(filelist) < 3:
                print("result files not found. Please enable result files")
                input()
                exit()

            for file in filelist:
                if "chr" in file:
                    chrData = zrl.loadCHR(fd+file)
                if "fet" in file:
                    fetData = zrl.loadFET(fd+file)
                if "hdr" in file:
                    hdrData = zrl.loadHDR(fd+file)

        if "-pd" in arg:
            pd = sys.argv[x+1]

        if "-rd" in arg:
            rd = sys.argv[x+1]
                    
        if "-f" in arg:
            planid = sys.argv[x+1]

        if "--scanfiles" in arg:
            scanfiles = sys.argv[x+1]

    try:
        dialogPath = os.path.abspath("\\".join([pd, planid, "dialog.xml"]))
        dialogData = zrl.loadDialog(dialogPath)
        dialogData.update(hdrData)

        now = datetime.datetime.now()
        print("start converting")

        sNo = dialogData.get("serialNo", "false")

        if sNo=="true":
            resultFile = planid+"_"+hdrData["partnb"]+".cmm"
        else:
            msn = dialogData.get("MSN")
            if msn:
                resultFile = planid+"_"+msn+".cmm"
            else:
                resultFile = planid+".cmm"
        path = rd + planid
        if not os.path.exists(path):
            os.makedirs(path)
        resultFile = "\\".join([path, resultFile])

        if os.path.isfile(resultFile):
            temp=''
            print("open:" + resultFile)
            file = open(resultFile, 'r')
            temp = json.load(file)
            temp[0].update({"date": now.strftime("%Y%m%d"), "time": now.strftime("%H:%M:%S"), "headerData": dialogData})
            temp[0]['chrData'] = zrl.updateEntry(temp[0]['chrData'], chrData)
            temp[0]['fetData'] = zrl.updateEntry(temp[0]['fetData'], fetData)
            newRes = {}
            newRes["resultID"] = len(temp)
            newRes["date"] = now.strftime("%Y%m%d")
            newRes["time"] = now.strftime("%H:%M:%S")
            newRes["headerData"] = update(dialogData)
            newRes["chrData"] = chrData
            temp.append(newRes)
            with open(resultFile, 'w') as file:
                json.dump(temp, file, indent=2)

        else:
            results.append({"resultID":0,"date": now.strftime("%Y%m%d"), "time": now.strftime("%H:%M:%S"),"headerData": dialogData,"chrData": chrData, "fetData": fetData})
            results.append({"resultID":1,"date": now.strftime("%Y%m%d"), "time": now.strftime("%H:%M:%S"),"headerData": dialogData,"chrData": chrData})
            with open(resultFile, 'w') as file:
                json.dump(results, file, indent=2)

    except:
        input("error")

