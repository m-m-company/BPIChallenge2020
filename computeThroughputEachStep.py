import sys

import pandas
from pm4py.objects.conversion.log import converter as converter
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from matplotlib import pyplot as pl, patches as pt
from matplotlib import lines as l


# Here whe have the hash_map that will contain a pair of <ActivityName, ListOfTimestamps> so in another function we
# can compute the average for each ActivityName.
def appendToHashMap(hash_map: {}, df: pandas.DataFrame, row_identifier: str, concept_index: int, date_index: int):
    for case_id, group in df.groupby([row_identifier]):
        temp = []
        for row in group.itertuples():
            temp.append(row)
        for i in range(0, len(temp) - 1):
            if temp[i][concept_index] in hash_map:
                hash_map[temp[i][concept_index]].append(temp[i + 1][date_index] - temp[i][date_index])
            else:
                hash_map[temp[i][concept_index]] = []
                hash_map[temp[i][concept_index]].append(temp[i + 1][date_index] - temp[i][date_index])


def avgThr(values: []):
    sum = values[0]
    for i in range(1, len(values)):
        sum += values[i]
    return sum / len(values)


if __name__ == '__main__':
    # we run this script with command line just for simplify the execution
    indexMap = {"DomesticDeclarationsFiltered.xes": ("(case)_id", 10, 2),
                "InternationalDeclarationsComplete.xes": ("(case)_id", 23, 2),
                "PermitLogFiltered.xes": ("case:concept:name", 1, 4),
                "PrepaidTravelCostFiltered.xes": ("case:concept:name", 19, 2),
                "RequestForPaymentFiltered.xes": ("case:concept:name", 11, 2)
                }
    hash_map = {}
    parameter = sys.argv
    if "-all" in parameter:
        domesticLog = xes_import_factory.apply("logs/DomesticDeclarationsFiltered.xes")
        domesticDF = converter.apply(domesticLog, None, converter.TO_DATA_FRAME)
        appendToHashMap(hash_map, domesticDF, "(case)_id", 10, 2)
        internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsComplete.xes")
        internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
        appendToHashMap(hash_map, internationalDF, "(case)_id", 23, 2)
        permitLog = xes_import_factory.apply("logs/PermitLogFiltered.xes")
        permitDF = converter.apply(permitLog, None, converter.TO_DATA_FRAME)
        appendToHashMap(hash_map, permitDF, "case:concept:name", 1, 4)
        prepaidTravelCostLog = xes_import_factory.apply("logs/PrepaidTravelCostFiltered.xes")
        prepaidTravelCostDF = converter.apply(prepaidTravelCostLog, None, converter.TO_DATA_FRAME)
        appendToHashMap(hash_map, prepaidTravelCostDF, "case:concept:name", 19, 2)
        requestForPaymentLog = xes_import_factory.apply("logs/RequestForPaymentFiltered.xes")
        requestForPaymentDF = converter.apply(requestForPaymentLog, None, converter.TO_DATA_FRAME)
        appendToHashMap(hash_map, requestForPaymentDF, "case:concept:name", 11, 2)
    else:
        for i in range(1, len(parameter)):
            log = xes_import_factory.apply("./logs/" + parameter[i])
            df = converter.apply(log, None, converter.TO_DATA_FRAME)
            appendToHashMap(hash_map, df, indexMap[parameter[i]][0], indexMap[parameter[i]][1], indexMap[parameter[i]][2])
    out = open("output/throughput" + parameter[1] + ".txt", "w")
    normalizedValue = []
    for key in hash_map.keys():
        avg = avgThr(hash_map[key])
        out.write(key + ":" + str(avg) + "\n")
        normalizedValue.append(avg.days)

    avg = 0
    for a in normalizedValue:
        avg += a
    avg = avg / len(normalizedValue)
    avg = [avg for _ in range(len(normalizedValue))]
    bluePatch = pt.Patch(color="blue", label="Mean throughput in days")
    redLine = l.Line2D([], [], color="red", linestyle="dashed", label="total average")

    names = list(hash_map.keys())
    fig, ax = pl.subplots()
    fig.set_size_inches(10, 10)
    pl.legend(handles=[bluePatch, redLine])
    ax.barh(range(len(hash_map)), normalizedValue, tick_label=names)
    ax.plot(avg, range(len(hash_map)), color='red', linestyle='dashed')
    fig.tight_layout()
    fig.savefig("RequestBottle.png", dpi=fig.dpi)
    fig.show()
    out.close()
