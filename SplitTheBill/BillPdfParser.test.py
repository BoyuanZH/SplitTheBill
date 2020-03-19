import unittest
from BillPdfParser import *
from Splitter import *


SAMPLE_PATH = os.path.abspath("../Sample")
SAMPLE_TXT_PATH = os.path.abspath("../Sample/Text")

if __name__ == "__main__":
    f = []
    for (dirpath, dirnames, filenames) in os.walk(SAMPLE_PATH):
        f.extend(filenames)
        break
    print(SAMPLE_PATH)
    print(f)

    for filename in f:
        # filename = "ATT_188097522906_20190914.pdf"
        patternConfig = Configuration()

        parser = Parser("{}\\{}".format(SAMPLE_PATH, filename), patternConfig)

        with  open("{}\\{}.txt".format(SAMPLE_TXT_PATH, filename) , "w") as txtFile:
            txtFile.write(parser.wholeText)

        bill: Bill = parser.extractInfo()
        print(bill.toText())

        # split the bill
        splitter = Splitter(bill)
        totals = splitter.split()
        print(totals)