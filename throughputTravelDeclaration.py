from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
import pandas


def avgThr(df: pandas.DataFrame) -> float:
    sums = []
    for case_id, group in df.groupby(["(case)_id"]):
        temp = []
        for row in group.itertuples():
            temp.append(row._2)
        if len(temp) > 1:
            sum = temp[1] - temp[0]
            for i in range(1, len(temp) - 1):
                sum += temp[i + 1] - temp[i]
            sums.append(sum)
    average = sums[0]
    for i in range(1, len(sums)):
        average = average + sums[i]
    return average / len(sums)


if __name__ == '__main__':
    domesticLog = xes_import_factory.apply("logs/DomesticDeclarationsFiltered.xes")
    internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsFiltered.xes")
    domesticDF = converter.apply(domesticLog, None, converter.TO_DATA_FRAME)
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    globalDF = domesticDF.append(internationalDF)
    print("domesticDeclaration throughput = ", avgThr(domesticDF))
    print("internationalDeclaration throughput = ", avgThr(internationalDF))
    print("domesticDeclaration + internationalDeclaration throughput = ", avgThr(globalDF))
