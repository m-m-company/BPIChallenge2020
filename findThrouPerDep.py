from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
from pandas import DataFrame
from matplotlib import pyplot as plt, patches as pt, lines as l
from math import sqrt


def findAvgCostPerDep(df: DataFrame):
    map = {}
    variantMap = {}
    count = 0
    average = 0
    for _, group in df.groupby("(case)_id"):
        k = group.iloc[0]["(case)_Permit_OrganizationalEntity"]
        if k != "UNKNOWN":
            k = k.split(" ")[2]
            value = (group.tail(1)["time:timestamp"].iloc[0] - group.iloc[0]["time:timestamp"]).days
            average += value
            count += 1
            if k in map.keys():
                map[k] = (map[k][0] + value, map[k][1] + 1)
            else:
                map[k] = (value, 1)
    average = average/count
    for _, group in df.groupby("(case)_id"):
        k = group.iloc[0]["(case)_Permit_OrganizationalEntity"]
        if k != "UNKNOWN":
            k = k.split(" ")[2]
            value = ((group.tail(1)["time:timestamp"].iloc[0] - group.iloc[0]["time:timestamp"]).days - average)**2
            if k in variantMap.keys():
                variantMap[k] = (map[k][0] + value, map[k][1] + 1)
            else:
                variantMap[k] = (value, 1)
    for key in variantMap.keys():
        variantMap[key] = sqrt(variantMap[key][0]/variantMap[key][1])
    for key in map.keys():
        map[key] = map[key][0]/map[key][1]

    names = list(map.keys())
    values = list(map.values())
    average = [average for _ in range(len(values))]

    variantNames = list(variantMap.keys())
    variantValues = list(variantMap.values())

    fig, ax = plt.subplots()
    ax.bar(range(len(map)), values, tick_label=names)
    ax.plot(range(len(map)), average, color='red', linestyle='dashed')
    plt.xticks(rotation=90)
    bluePatch = pt.Patch(color="blue", label="average throughput per dep")
    redLine = l.Line2D([], [], color="red", linestyle="dashed", label="total average")
    plt.legend(handles=[bluePatch, redLine])
    fig.tight_layout()
    plt.savefig('throughputPerDepartment.png')

    plt.close(fig)
    fig2, ax2 = plt.subplots()
    ax2.bar(range(len(variantMap)), variantValues, tick_label=variantNames)
    plt.xticks(rotation=90)
    bluePatch = pt.Patch(color="blue", label="mean squared error per dep")
    plt.legend(handles=[bluePatch])
    fig2.tight_layout()
    plt.savefig('meanSquaredErrorThroughput.png')


if __name__ == '__main__':
    internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsComplete.xes")
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    findAvgCostPerDep(internationalDF)
