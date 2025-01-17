from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
from pandas import DataFrame
from matplotlib import pyplot as plt, patches as pt, lines as l
from math import sqrt


def findAvgThrouPerDep(df: DataFrame):
    map = {}  # dictionary that contains as key the department and as value the average throughput
    variantMap = {}  # same dictionary as map, but we use it to compute the variance
    count = 0
    average = 0
    for _, group in df.groupby("(case)_id"):  # for used to compute the throughput
        k = group.iloc[0]["(case)_Permit_OrganizationalEntity"]
        if k != "UNKNOWN":
            k = k.split(" ")[2]
            value = (group.tail(1)["time:timestamp"].iloc[0] - group.iloc[0]["time:timestamp"]).days
            average += value
            count += 1
            # a values is composed initially by a  pair representing the local sum of throughput and the count of cases
            # after the for we iterate once again on the map to calculate the average
            if k in map.keys():
                map[k] = (map[k][0] + value, map[k][1] + 1)
            else:
                map[k] = (value, 1)
    average = average / count
    for _, group in df.groupby("(case)_id"): # for used to compute the variance
        k = group.iloc[0]["(case)_Permit_OrganizationalEntity"]
        if k != "UNKNOWN":
            k = k.split(" ")[2]
            value = ((group.tail(1)["time:timestamp"].iloc[0] - group.iloc[0]["time:timestamp"]).days - average) ** 2
            if k in variantMap.keys():
                variantMap[k] = (map[k][0] + value, map[k][1] + 1)
            else:
                variantMap[k] = (value, 1)
    for key in variantMap.keys():
        variantMap[key] = sqrt(variantMap[key][0] / variantMap[key][1])
    for key in map.keys():
        map[key] = map[key][0] / map[key][1]

    names = list(map.keys())
    values = list(map.values())
    average = [average for _ in range(len(values))]

    variantNames = list(variantMap.keys())
    variantValues = list(variantMap.values())

    fig, ax = plt.subplots()
    # function used to create the plot
    ax.bar(range(len(map)), values, tick_label=names)
    # function used to create the red line representing the average
    ax.plot(range(len(map)), average, color='red', linestyle='dashed')
    # rotate the x labels
    plt.xticks(rotation=90)
    # create a legend
    bluePatch = pt.Patch(color="blue", label="average throughput per dep")
    redLine = l.Line2D([], [], color="red", linestyle="dashed", label="total average")
    # adding a legend
    plt.legend(handles=[bluePatch, redLine])
    fig.tight_layout()
    # saving the figure
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
    # load the log
    internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsComplete.xes")
    # convert the log to a pandas data frame
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    findAvgThrouPerDep(internationalDF)
