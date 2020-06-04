from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
from pandas import DataFrame


def computeRejected(df: DataFrame, s: str, concept_name: int, rejected_case: []):
    globalRejected = 0
    neverApproved = 0
    for case_id, group in df.groupby(s):
        localRejected = 0
        localSubmitted = 0
        for row in group.itertuples():
            if row[concept_name] in rejected_case:
                #globalRejected += 1
                localRejected += 1
            if row[concept_name] == "Declaration SUBMITTED by EMPLOYEE":
                localSubmitted += 1
        if localRejected > 0:
            globalRejected += 1
        if localSubmitted <= localRejected:
            neverApproved += 1
    print("Travel declarations rejected = " + str(globalRejected) + "\n")
    print("Travel declarations never approved = " + str(neverApproved) + "\n")


if __name__ == '__main__':
    domesticLog = xes_import_factory.apply("logs/DomesticDeclarationsFiltered.xes")
    domesticDF = converter.apply(domesticLog, None, converter.TO_DATA_FRAME)
    rejectedCase = ["Declaration REJECTED by ADMINISTRATION", "Declaration REJECTED by BUDGET OWNER",
                    "Declaration REJECTED by SUPERVISOR"]
    print("Domestic declarations:\n")
    computeRejected(domesticDF, "(case)_id", 10, rejectedCase)
    print("\n")
    internationalLog = xes_import_factory.apply("logs/InternationalDeclarationsFiltered.xes")
    internationalDF = converter.apply(internationalLog, None, converter.TO_DATA_FRAME)
    rejectedCase = ["Declaration REJECTED by ADMINISTRATION", "Declaration REJECTED by BUDGET OWNER",
                    "Declaration REJECTED by SUPERVISOR", "Declaration REJECTED by DIRECTOR"]
    print("International declarations:\n")
    computeRejected(internationalDF, "(case)_id", 23, rejectedCase)
