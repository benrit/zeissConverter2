import os, sys
from zeissResultLib import CmmFileHandler

pd = "O:\\Measurement\\Results"
rd = "O:\\Measurement\\_resultDatabase"
fd = "c:\\temp\\results"

planid = ""
scanfiles = ""

if __name__ == "__main__":

    for x, arg in enumerate(sys.argv):
        if "-f" in arg:
            planid = sys.argv[x+1]

        if "--scanfiles" in arg:
            scanfiles = sys.argv[x+1]
    try:
        CmmFileHandler(zeissResultFileFolder=fd, cmmResultFileFolder=rd, planid=planid, xmlResultFileFolder=pd)
    except ValueError:
        print(ValueError)
        input("error")
