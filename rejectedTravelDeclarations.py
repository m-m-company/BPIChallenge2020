from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
from matplotlib import pyplot as plt
from pandas import DataFrame
import numpy as np


def computeRejected(df: DataFrame, s: str, concept_name: int, rejected_case: []):
    mapRejected = {}
    mapNeverApproved = {}
    mapTotalCases = {}
    for dep_id, dep in df.groupby("(case)_Permit_OrganizationalEntity"):
        if dep_id != "UNKNOWN":
            dep_id = dep_id.split(" ")[2]
            globalRejected = 0
            neverApproved = 0
            mapTotalCases[dep_id] = dep.groupby(s).ngroups
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
            mapRejected[dep_id] = globalRejected
            mapNeverApproved[dep_id] = neverApproved

    labels = list(mapRejected.keys())
    totalCases = list(mapTotalCases.values())
    rejected = list(mapRejected.values())
    neverApproved = list(mapNeverApproved.values())

    x = np.arange(len(labels))
    width = 0.30

    fig, ax = plt.subplots()
    # the result will be a bar chart with three rects
    rects1 = ax.bar(x, totalCases, width, label='Total cases')
    rects2 = ax.bar(x - width, rejected, width, label='Rejected cases')
    rects3 = ax.bar(x + width, neverApproved, width, label='Never approved cases')

    ax.set_ylabel('Cases')
    ax.set_title('Cases per department')
    ax.set_xticks(x)
    plt.xticks(rotation=90)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()
    fig.savefig("output/dataForDep.png")


if __name__ == '__main__':
    internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsFiltered.xes")
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    rejectedCase = ["Declaration REJECTED by ADMINISTRATION", "Declaration REJECTED by BUDGET OWNER",
                    "Declaration REJECTED by SUPERVISOR", "Declaration REJECTED by DIRECTOR"]
    computeRejected(internationalDF, "(case)_id", 23, rejectedCase)
