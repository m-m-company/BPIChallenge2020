from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
from matplotlib import pyplot as plt, patches as pt, lines as l
from pandas import DataFrame


def computeRejected(df: DataFrame, s: str, concept_name: int, rejected_case: []):
    mapRejected = {}
    mapPieRejected = {}
    mapNeverApproved = {}
    mapPieNeverApproved = {}
    totalRejected = 0
    totalNeverApproved = 0
    for dep_id, dep in df.groupby("(case)_Permit_OrganizationalEntity"):
        if dep_id != "UNKNOWN":
            dep_id = dep_id.split(" ")[2]
            globalRejected = 0
            neverApproved = 0
            for case_id, group in dep.groupby(s):
                localRejected = 0
                localSubmitted = 0
                for row in group.itertuples():
                    if row[concept_name] in rejected_case:
                        localRejected += 1
                    if row[concept_name] == "Declaration SUBMITTED by EMPLOYEE":
                        localSubmitted += 1
                if localRejected > 0:
                    globalRejected += 1
                if localSubmitted <= localRejected:
                    neverApproved += 1
            totalRejected += globalRejected
            totalNeverApproved += neverApproved
            mapRejected[dep_id] = globalRejected
            mapNeverApproved[dep_id] = neverApproved

    names = list(mapRejected.keys())
    for k in names:
        if (mapRejected[k]/totalRejected) * 100 >= 1:
            mapPieRejected[k] = (mapRejected[k]/totalRejected) * 100
        if (mapNeverApproved[k]/totalNeverApproved) * 100 >= 1:
            mapPieNeverApproved[k] = (mapNeverApproved[k]/totalNeverApproved) * 100
    values = list(mapRejected.values())

    fig, ax = plt.subplots()
    ax.bar(range(len(mapRejected)), values, tick_label=names)
    plt.xticks(rotation=90)
    fig.tight_layout()
    plt.show()
    fig.savefig('rejectedPerDepartment.png')

    names = list(mapNeverApproved.keys())
    values = list(mapNeverApproved.values())

    plt.close(fig)
    fig, ax = plt.subplots()
    ax.bar(range(len(mapNeverApproved)), values, tick_label=names)
    plt.xticks(rotation=90)
    fig.tight_layout()
    plt.show()
    fig.savefig('neverApprovedPerDepartment.png')

    names = list(mapPieRejected.keys())
    values = list(mapPieRejected.values())
    plt.close(fig)
    fig, ax = plt.subplots()
    ax.pie(values, labels=names, autopct='%1.1f%%')
    ax.axis('equal')
    plt.show()
    fig.savefig('pieRejectedDep.png')

    names = list(mapPieNeverApproved.keys())
    values = list(mapPieNeverApproved.values())
    plt.close(fig)
    fig, ax = plt.subplots()
    ax.pie(values, labels=names, autopct='%1.1f%%')
    ax.axis('equal')
    plt.show()
    fig.savefig('pieNeverApprovedDep.png')


if __name__ == '__main__':
    # domesticLog = xes_import_factory.apply("logs/DomesticDeclarationsFiltered.xes")
    # domesticDF = converter.apply(domesticLog, None, converter.TO_DATA_FRAME)
    # rejectedCase = ["Declaration REJECTED by ADMINISTRATION", "Declaration REJECTED by BUDGET OWNER",
    #                "Declaration REJECTED by SUPERVISOR"]
    # print("Domestic declarations:\n")
    # computeRejected(domesticDF, "(case)_id", 10, rejectedCase)
    # print("\n")
    internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsFiltered.xes")
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    rejectedCase = ["Declaration REJECTED by ADMINISTRATION", "Declaration REJECTED by BUDGET OWNER",
                    "Declaration REJECTED by SUPERVISOR", "Declaration REJECTED by DIRECTOR"]
    computeRejected(internationalDF, "(case)_id", 23, rejectedCase)
