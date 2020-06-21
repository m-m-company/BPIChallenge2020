from distutils.log import Log

from pandas._libs.tslibs.timestamps import Timestamp
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
from pandas import DataFrame


def avgThr(df: DataFrame, trip: bool = False) -> float:
    sums = []
    for case_id, group in df.groupby(["(case)_id"]):
        time1 = group.iloc[0]["time:timestamp"]
        tail = group.tail(1)["time:timestamp"].iloc[0]
        if trip:
            startTrip = group.loc[group["concept:name"] == "Start trip"].iloc[0]["time:timestamp"]
            endTrip = group.loc[group["concept:name"] == "End trip"].iloc[0]["time:timestamp"]
            tripTime = endTrip - startTrip
            sums.append(tail - time1 - tripTime)
        else:
            sums.append(tail - time1)
    average = sums[0]
    for i in range(1, len(sums)):
        average = average + sums[i]
    return average / len(sums)


if __name__ == '__main__':
    domesticLog = xes_import_factory.apply("logs/DomesticDeclarationsFiltered.xes")
    internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsComplete.xes")
    internationalLogFiltered = xes_import_factory.apply("logs/InternationalDeclarationsFiltered.xes")
    domesticDF = converter.apply(domesticLog, None, converter.TO_DATA_FRAME)
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    internationalDFFiltered = converter.apply(internationalLogFiltered, None, converter.TO_DATA_FRAME)
    globalDF = domesticDF.append(internationalDFFiltered)
    print("domesticDeclaration throughput = ", avgThr(domesticDF))
    print("internationalDeclaration throughput = ", avgThr(internationalDF, True))
    print("internationalDeclarationFiltered throughput = ", avgThr(internationalDFFiltered))
    print("domesticDeclaration + internationalDeclaration throughput = ", avgThr(globalDF))
