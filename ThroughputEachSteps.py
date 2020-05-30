from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
import pandas


def appendHashMap(hash_map: {}, df: pandas.DataFrame, s: str, concept_name: int, date_index: int):
    for case_id, group in df.groupby([s]):
        temp = []
        for row in group.itertuples():
            temp.append(row)
        for i in range(0, len(temp) - 1):
            if temp[i][concept_name] in hash_map:
                hash_map[temp[i][concept_name]].append(temp[i + 1][date_index] - temp[i][date_index])
            else:
                hash_map[temp[i][concept_name]] = []
                hash_map[temp[i][concept_name]].append(temp[i + 1][date_index] - temp[i][date_index])


def avgThr(values: []):
    sum = values[0]
    for i in range(1, len(values)):
        sum += values[i]
    return sum/len(values)


if __name__ == '__main__':
    hash_map = {}
    domesticLog = xes_import_factory.apply("./logs/DomesticDeclarationsFiltered.xes")
    domesticDF = converter.apply(domesticLog, None, converter.TO_DATA_FRAME)
    appendHashMap(hash_map, domesticDF, "(case)_id", 10, 2)
    internationalLog = xes_import_factory.apply("./logs/InternationalDeclarationsFiltered.xes")
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    appendHashMap(hash_map, internationalDF, "(case)_id", 23, 2)
    permitLog = xes_import_factory.apply("./logs/PermitLogFiltered.xes")
    permitDF = converter.apply(permitLog, None, converter.TO_DATA_FRAME)
    appendHashMap(hash_map, permitDF, "case:concept:name", 1, 4)
    prepaidTravelCostLog = xes_import_factory.apply("./logs/PrepaidTravelCostFiltered.xes")
    prepaidTravelCostDF = converter.apply(prepaidTravelCostLog, None, converter.TO_DATA_FRAME)
    appendHashMap(hash_map, prepaidTravelCostDF, "case:concept:name", 19, 2)
    requestForPaymentLog = xes_import_factory.apply("./logs/RequestForPaymentFiltered.xes")
    requestForPaymentDF = converter.apply(requestForPaymentLog, None, converter.TO_DATA_FRAME)
    appendHashMap(hash_map, requestForPaymentDF, "case:concept:name", 11, 2)
    out = open("output.txt", "w")
    for key in hash_map.keys():
        out.write(key + ":" + str(avgThr(hash_map[key])) + "\n")
    out.close()
