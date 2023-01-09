import sys
from zeissResultLib import CmmFileHandler

pd = "O:\\Measurement\\Results"
rd = "O:\\Measurement\\_resultDatabase"
fd = "c:\\temp\\results"

planid = ""
scanfiles = ""
runtime = ""
if __name__ == "__main__":

    for x, arg in enumerate(sys.argv):
        if "-f" in arg:
            planid = sys.argv[x + 1]

        if "-rt" in arg:
            runtime = sys.argv[x + 1]

        if "--scanfiles" in arg:
            scanfiles = sys.argv[x + 1]
     
    
    