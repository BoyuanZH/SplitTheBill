import pdfminer.high_level as pm
import re
from typing import List, Match
import os
import datetime

class Logger(object):
    def __init__(self, logPath, isActive=True):
        self.path = logPath
        self.isActive = isActive
    
    def log(self, msg: str) -> None:
        if self.isActive:
            print(msg)

LOG_PATH = os.path.abspath("Log/" + "log_{}.txt".format(datetime.datetime.now))
SAMPLE_PATH = os.path.abspath("Sample")
_logger = Logger(LOG_PATH, True)

class Configuration(object):
    def __init__(self):
        self.countOfDevicePattern = re.compile(r"^([1-9]*) Devices$", re.M)
        self.startPattern = re.compile(r"^Total$", re.M)
        self.endPattern = re.compile(r"^1. Access for iPhone 4G LTE w/ Visual Voicemail$", re.M)
        self.phonePattern = re.compile(r"^([0-9]{3}\.[0-9]{3}\.[0-9]{4})$", re.M)
        self.startPattern_individualFee = re.compile(r"^Total$", re.M)
        self.endPattern_individualFee = re.compile(r"^Total$", re.M)
        self.feePattern = re.compile(r"^\$[0-9]*\.[0-9]*$", re.M)
        self.totalFeePattern = re.compile(r"^Monthly charges$", re.M)
        self.dataUsagePattern = re.compile(r"^[0-9]*\.[0-9]*$", re.M)

class Bill(object):
    def __init(self, countOfDevice, devices, totalFee, dataFee, individualDataUsages, individualBaseFees):
        self.countOfDevice = countOfDevice
        self.devices = devices
        self.totalFee = totalFee
        self.dataFee = dataFee
        self.individualDataUsage = individualDataUsages
        self.individualBaseFees = individualBaseFees
        assert(self.isValid())
    
    def isValid(self):
        return (self.countOfDevice == len(self.individualBaseFees) == len(self.individualDataUsage))

    def toText(self):
        res = """
        Count = {}
        Devices = {}
        WifiFee = {}
        IndividualBaseFees = {}
        IndividualWifeUsages = {}
        Total Fee = {}
        """.format(self.countOfDevice,
                    self.devices,
                    self.dataFee,
                    self.individualBaseFees,
                    self.individualDataUsage,
                    self.totalFee)
        return res

class Parser(object):
    def _tryReadPdfAsText(self, filePath):
        text: str
        try:
            text = pm.extract_text(filePath)
            text = text.replace("\n\n", "\n")
        except Exception as ex:
            _logger.log("Error reading parsing PDF: {}".format(filePath))
            raise ex
        return text

    def __init__(self, filename: str, config: Configuration):
        self.config = config
        filePath = os.path.abspath("Sample/" + filename) # "ATT_188097522906_20190914.pdf")
        self.wholeText: str = self._tryReadPdfAsText(filePath)

    def extractInfo(self) -> Bill:
        bill = Bill()
        # get the count of device
        bill.countOfDevice: int = int(re.findall(self.config.countOfDevicePattern, self.wholeText)[0])

        # extract the useful text section
        startIndex: int = self.config.startPattern.search(self.wholeText).start()
        endIndex: int = self.config.endPattern.search(self.wholeText).end()
        text: str = self.wholeText[startIndex:endIndex]

        # get total wifi fee and individual baseFees
        bill.devices: List[str] = re.findall(self.config.phonePattern, text)
        a: List[Match[str]] = list(re.finditer(self.config.startPattern_individualFee, text))
        individualFeeSection: str = text[a[0].end():a[1].start()]
        individualFees: List[str] = re.findall(self.config.feePattern, individualFeeSection)
        bill.dataFee, bill.individualBaseFees = individualFees[0], individualFees[1:bill.countOfDevice + 1]

        # get total fee
        endIndex_TotalFee: int = self.config.totalFeePattern.search(text).start()
        totalFeeSection: str = text[:endIndex_TotalFee]
        fees: List[str] = re.findall(self.config.feePattern, totalFeeSection)
        bill.totalFee: str = fees[-1]

        # get individual data usage
        bill.individualDataUsage: List[str] = re.findall(self.config.dataUsagePattern, text)[:bill.countOfDevice]

        _logger.log(bill.toText())

        if bill.isValid():
            return bill
        else:
            _logger.log("Extraction invalid: num of devices don't match.")
            raise Exception("Invalid bill info extraction!")


if __name__ == "__main__":
    f = []
    for (dirpath, dirnames, filenames) in os.walk(SAMPLE_PATH):
        f.extend(filenames)
        break

    for filename in f:
        # filename = "ATT_188097522906_20190914.pdf"
        patternConfig = Configuration()
        parser = Parser(filename, patternConfig)
        bill: Bill = parser.extractInfo()
        print(bill.toText())