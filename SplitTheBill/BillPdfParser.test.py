import unittest
from BillPdfParser import *


SAMPLE_PATH = os.path.abspath("Sample")
SAMPLE_TXT_PATH = os.path.abspath("Sample/Text")

if __name__ == "__main__":
    f = []
    for (dirpath, dirnames, filenames) in os.walk(SAMPLE_PATH):
        f.extend(filenames)
        break

    for filename in f:
        # filename = "ATT_188097522906_20190914.pdf"
        patternConfig = Configuration()

        parser = Parser(filename, patternConfig)

        with  open(SAMPLE_TXT_PATH + "/" + filename + ".txt", "w") as txtFile:
            txtFile.write(parser.wholeText)

        bill: Bill = parser.extractInfo()
        print(bill.toText())