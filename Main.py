from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
import pandas


def avgThr(df: pandas.DataFrame) -> float:
    gr = df.groupby(["(case)_id"])
    for case_id, group in gr:
        for i in range(0, group.shape[0] + 1):
            print(pandas.date_range())



if __name__ == '__main__':
    domesticLog = xes_import_factory.apply("./logs/DomesticDeclarationsFiltered.xes")
    internationalLog = xes_import_factory.apply("./logs/InternationalDeclarationsFiltered.xes")
    domesticDF = converter.apply(domesticLog, None, converter.TO_DATA_FRAME)
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    globalDF = domesticDF.append(internationalDF)
    averageThroughput = avgThr(domesticDF)
