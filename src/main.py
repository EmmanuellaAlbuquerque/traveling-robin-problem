from pathlib import Path
from robin_file_reader import RobinFileReader
from trp import TRP
from vnd import swap

# file_path = Path("../instances/n5.txt").absolute()
# file_path = Path("../instances/n10p4.txt").absolute()
# file_path = Path("../instances/n15p5.txt").absolute()
# file_path = Path("../instances/n29p7A.txt").absolute()
# file_path = Path("../instances/n29p8B.txt").absolute()
# file_path = Path("../instances/n40p11.txt").absolute()
file_path = Path("../instances/n52p11.txt").absolute()

# file_path = Path("../instances_apa_cup/cup1.txt").absolute()
# file_path = Path("../instances_apa_cup/cup2.txt").absolute()
# file_path = Path("../instances_apa_cup/cup3.txt").absolute()
file = open(file_path, 'r')

(dimension, p, cost_matrix) = RobinFileReader(file).getResult()

trp = TRP(dimension, p, cost_matrix)
print('--- changes ---')
initial_solution = trp.run()

(initial_total_cost, agent_list) = trp.calculateTotalCost()
# print('total cost:', initial_total_cost)
# print(agent_list)
# print(initial_solution)
(initial_solution, agent_list) = swap(
    initial_solution, agent_list, cost_matrix)

new_total = 0
for i in agent_list:
    new_total += i['cost']

print('total cost:', initial_total_cost)
print('new total cost:', new_total)
# print(agent_list)

# --------------------------------------------

# for element in initial_solution:
#     print(', '.join(map(str, element)), end=';\n')
