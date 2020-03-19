from BillPdfParser import Bill

class Splitter(object):
    def __init__(self, bill: Bill):
        self.bill = bill
        self.bill.toValue()
        print(self.bill.toText())
    
    def split(self):
        totals = [0] * self.bill.countOfDevice
        assert(self.bill.isValid())

        # data extra fees
        dataExtraFees: List[float] = None
        totalData = self.bill.rollOverDataFromLastMonth + self.bill.totalData 
        extraData = sum(self.bill.individualDataUsages) - totalData

        if extraData > 0:
            dataAvg = totalData /self.bill.countOfDevice
            dataExtraUsages = [(i - dataAvg) if i > dataAvg else 0 for i in self.bill.individualDataUsages]
            dataExtraProportions = [i / sum(dataExtraUsages) for i in dataExtraUsages]
            dataExtraFees = [i * self.bill.dataExtraUnitFee * extraData for i in dataExtraProportions]
        else:
            dataExtraFees = [0 for i in range(self.bill.countOfDevice)]

        for i in range(self.bill.countOfDevice):
            totals[i] = self.bill.dataFee/self.bill.countOfDevice + dataExtraFees[i] + self.bill.individualBaseFees[i]

        assert((sum(totals) - self.bill.totalFee) < 1)
        return totals


if __name__ == "__main__":
    N = 8
    totalFee = 386.34
    monthly_unit = 23.50
    wifiTotalFee = 105.9
    wifi_extra_g = 0
    wifi_total = 0
    wifi = [2.0, 2.3, 1.2, 3.4, 0.2, 0.3, 0.2, 0.1]
    baseFee = [68.2, monthly_unit, monthly_unit, monthly_unit, 71.42, monthly_unit, monthly_unit, monthly_unit]

    bill = Bill(N, ['888.888.8888'] * N, totalFee, wifiTotalFee, wifi, baseFee, 0)
    splitter = Splitter(bill)
    res1_new = splitter.split()