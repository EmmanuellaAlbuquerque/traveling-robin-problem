from pathlib import Path
from robin_file_reader import RobinFileReader
from trp import TRP
from vnd import VND
from copy import deepcopy

# file_path = Path("../instances/n5.txt").absolute()
# file_path = Path("../instances/n6.txt").absolute()
# file_path = Path("../instances/n10p4.txt").absolute()
# file_path = Path("../instances/n15p5.txt").absolute()
# file_path = Path("../instances/n29p7A.txt").absolute()
# file_path = Path("../instances/n29p8B.txt").absolute()
# file_path = Path("../instances/n40p11.txt").absolute()
# file_path = Path("../instances/n52p11.txt").absolute()

file_path = Path("../instances_apa_cup/cup1.txt").absolute()
# file_path = Path("../instances_apa_cup/cup2.txt").absolute()
# file_path = Path("../instances_apa_cup/cup3.txt").absolute()


def showSolution(solution):
    for route in solution:
        print(', '.join(map(str, route)), end=' ;\n')


def f(agent_list):
    oF = 0
    for i in agent_list:
        oF += i['cost']
    return oF


def getRoutesTotalCost(solution, cost_matrix):
    total_cost = 0
    for route in solution:
        agent_cost = 0
        for address in range(0, len(route) - 1):
            address1 = route[address]
            address2 = route[address+1]
            agent_cost += int(cost_matrix[address1][address2])
        total_cost += agent_cost
    return total_cost


file = open(file_path, 'r')

(dimension, p, cost_matrix) = RobinFileReader(file).getResult()

# constructive algorithm solution
print('constructive algorithm solution')
trp = TRP(dimension, p, cost_matrix)
trp_solution = trp.run()
(initial_cost, trp_agent_list) = trp.calculateTotalCost()
# print(trp_agent_list)
# showSolution(trp_solution)
print('-> total cost:', f(trp_agent_list))
print('-> recalculated trp:', getRoutesTotalCost(trp_solution, cost_matrix))
print('\n')

# variable neighbourhood descent solution
print('variable neighbourhood descent solution')
vnd = VND()
(vnd_solution, vnd_agent_list) = vnd.run(
    deepcopy(trp_solution), deepcopy(trp_agent_list), cost_matrix)
# print(vnd_agent_list)
# showSolution(vnd_solution)
print('-> final cost:', f(vnd_agent_list))
print('-> recalculated vnd:', getRoutesTotalCost(vnd_solution, cost_matrix))
print('\n')


def calculateSolution(solution, cost_matrix):
    total_cost = 0
    for route in solution:
        for i in range(0, len(route)):
            if (i != 0):
                origin = route[i-1]
                destination = route[i]
                # print(origin, destination)
                total_cost += cost_matrix[origin][destination]
        # print('\n')
    print(total_cost)


calculateSolution(vnd_solution, cost_matrix)
