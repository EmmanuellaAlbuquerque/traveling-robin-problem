from pathlib import Path
from robin_file_reader import RobinFileReader
from trp import TRP
from vnd import swap

file_path = Path("../instances/n15p5.txt").absolute()
file = open(file_path, 'r')

(dimension, p, cost_matrix) = RobinFileReader(file).getResult()

trp = TRP(dimension, p, cost_matrix)
initial_solution = trp.run()

(initial_total_cost, agent_list) = trp.calculateTotalCost()

swap(initial_solution, agent_list, cost_matrix)
