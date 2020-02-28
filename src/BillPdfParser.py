import pdfminer.high_level as pm
import re
from typing import List

countOfDevicePattern = re.compile(r"^([1-9]*) Devices$", re.M)
startPattern = re.compile(r"^Total$", re.M)
endPattern = re.compile(r"^1. Access for iPhone 4G LTE w/ Visual Voicemail$", re.M)
phonePattern = re.compile(r"^([0-9]{3}\.[0-9]{3}\.[0-9]{4})$", re.M)
startPattern_individualFee = re.compile(r"^Total$", re.M)
endPattern_individualFee = re.compile(r"^Total$", re.M)
feePattern = re.compile(r"^\$[0-9]*\.[0-9]*$", re.M)
totalFeePattern = re.compile(r"^Monthly charges$", re.M)
dataUsagePattern = re.compile(r"^[0-9]*\.[0-9]*$", re.M)

text: str = pm.extract_text('ATT_188097522906_20200214.pdf')
text = text.replace("\n\n", "\n")
countOfDevice: int = int(re.findall(countOfDevicePattern, text)[0])

startIndex: int = startPattern.search(text).start()
endIndex: int = endPattern.search(text).end()
text = text[startIndex:endIndex]

phones: List[str] = re.findall(phonePattern, text)
a: List = list(re.finditer(startPattern_individualFee, text))
individualFee: str = text[a[0].end():a[1].start()]
individualFees: List[str] = re.findall(feePattern, individualFee)
wifiFee, individualFees = individualFees[0], individualFees[1:]

endIndex_TotalFee: int = totalFeePattern.search(text).start()
totalFee: str = text[:endIndex_TotalFee]
fees: List[str] = re.findall(feePattern, totalFee)
totalFeeValue: str = fees[-1]

data: List[str] = re.findall(dataUsagePattern, text)[:countOfDevice]

print("\nCount = {},\nWifiFee = {},\nPhones = {},\nInividualFees = {},\nTotalFee = {},\nWifeDataUsages = {}".format(countOfDevice, wifiFee, phones, individualFees, totalFeeValue, data))