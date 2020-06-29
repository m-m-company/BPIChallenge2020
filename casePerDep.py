from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
from pandas import DataFrame
from matplotlib import pyplot as plt


def findNumberCases(df: DataFrame):
    mapCases = {}
    mapPercent = {}
    totalCases = df.groupby("(case)_id").ngroups
    for dep_id, group in df.groupby("(case)_Permit_OrganizationalEntity"):
        if dep_id != "UNKNOWN":
            dep_id = dep_id.split(" ")[2]
        cases = group.groupby("(case)_id").ngroups
        mapCases[dep_id] = cases
        percent = (cases / totalCases) * 100
        if percent >= 1:
            mapPercent[dep_id] = percent

    names = list(mapCases.keys())
    values = list(mapCases.values())
    fig, ax = plt.subplots()
    ax.bar(range(len(mapCases)), values, tick_label=names)
    plt.xticks(rotation=90)
    fig.tight_layout()
    plt.show()
    fig.savefig('output/casesPerDep.png')

    names = list(mapPercent.keys())
    values = list(mapPercent.values())
    plt.close(fig)
    fig, ax = plt.subplots()
    # this function create a pie chart
    ax.pie(values, labels=names, autopct='%1.1f%%')
    ax.axis('equal')
    plt.show()
    fig.savefig('output/pieCasesPerDep.png')


if __name__ == '__main__':
    internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsComplete.xes")
    dataFrame = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    findNumberCases(dataFrame)
