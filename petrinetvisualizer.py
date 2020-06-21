from pm4py.algo.discovery.inductive import algorithm as heuristics_miner
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.visualization.petrinet import visualizer as pn_visualizer


if __name__ == '__main__':
    log = xes_importer.apply("logs/DomesticDeclarationsFiltered.xes")
    net, initial_marking, final_marking = heuristics_miner.apply(log)
    parameters = {pn_visualizer.Variants.PERFORMANCE.value.Parameters.FORMAT: "png"}
    gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.PERFORMANCE, log=log)
    print(gviz)
    pn_visualizer.save(gviz, "inductive_frequency.png")