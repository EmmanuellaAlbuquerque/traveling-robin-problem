from pathlib import Path
from robin_file_reader import RobinFileReader
from trp import TRP

file_path = Path("../instances/n52p11.txt").absolute()
file = open(file_path, 'r')

(dimension, p, cost_matrix) = RobinFileReader(file).getResult()

trp = TRP(dimension, p, cost_matrix)
trp.run()
