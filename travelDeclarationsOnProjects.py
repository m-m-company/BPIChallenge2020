from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log import converter as converter
from pandas import DataFrame


def countDeclarationsOnProject(df: DataFrame, s: str):
    count = 0
    for case_id, group in df.groupby(s):
        if group.iloc[0]["T:ProjectNumber"] != "UNKNOWN":
            count += 1
    print("Total = " + str(count))


if __name__ == '__main__':
    permitLog = xes_import_factory.apply("logs/PermitLogFiltered.xes")
    permitDF = converter.apply(permitLog, None, converter.TO_DATA_FRAME)
    countDeclarationsOnProject(permitDF, "case:concept:name", 1)
