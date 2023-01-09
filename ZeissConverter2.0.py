import sys
from zeissResultLib import CmmFileHandler

pd = "O:\\Measurement\\Results"
rd = "O:\\Measurement\\_resultDatabase"
fd = "c:\\temp\\results"

inspDir = ""
planid = ""
scanfiles = ""

if __name__ == "__main__":

    for x, arg in enumerate(sys.argv):
        if "-f" in arg:
            planid = sys.argv[x + 1]

        if "--inspdir" in arg:
            inspDir = sys.argv[x + 1]

        if "--scanfiles" in arg:
            scanfiles = sys.argv[x + 1]
    try:
        CmmFileHandler(zeissResultFileFolder=fd, cmmResultFileFolder=rd, planid=planid, inspDir=inspDir)
    except FileNotFoundError as e:
        print(e)
        input("")
    except:
        print("")
        print("Unexpected error:", sys.exc_info()[0])
        input("")
