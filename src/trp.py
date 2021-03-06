from numpy import array, inf
from random import randrange


class TRP():
    def __init__(self, dimension, p, cost_matrix):
        """ Traveling Robin Problem

        Args:
            dimension (int): number of vertices
            p (int): maximum number of addresses visited on each route
            cost_matrix (list): cost/time adjacency matrix to travel each of the edges
        """
        self.d = dimension
        self.p = p
        self.cost_matrix = array(cost_matrix)
        self.solution = []
        self.partial_solution = [0]
        self.q = []

        for i in range(0, self.d):
            if i not in self.partial_solution:
                self.q.append(i)

    def selectBestTriangle(self):
        self.partial_solution = [0]
        # encontra o triângulo no qual os endereços são os mais distantes possíveis
        while len(self.partial_solution) < 3:
            max_value = -inf
            vertex = 0
            for v in self.q:
                last_element_solution = self.partial_solution[-1]
                if (int(self.cost_matrix[last_element_solution][v]) > float(max_value)):
                    max_value = self.cost_matrix[last_element_solution][v]
                    vertex = v

            self.partial_solution.append(vertex)
            self.q.remove(vertex)
        self.partial_solution.append(0)

    def selectRandomTriangle(self):
        # encontra o triângulo escolhendo os endereços de forma aleatória
        random_range = len(self.q)
        random_address1 = randrange(random_range)
        address1 = self.q.pop(random_address1)
        random_address2 = randrange(random_range - 1)
        address2 = self.q.pop(random_address2)

        self.partial_solution = [
            0, address1, address2, 0]

    def selectSequenceTriangle(self):
        address1 = self.q[0]
        address2 = self.q[1]
        self.partial_solution = [
            0, address1, address2, 0]
        self.q.remove(address1)
        self.q.remove(address2)

    def printAnalysisOfCheaperInsertion(self, cost, x, u, v):
        print('menor valor:', cost,
              '-> vértice:', x, 'inserção entre: (', u, ',', v, ')')

    def calculateTotalCost(self):
        agent_id = 1
        total_cost = 0
        agent_cost = 0
        agent_cost_list = []
        for route in self.solution:
            agent_cost = 0
            for address in range(0, len(route) - 1):
                address1 = route[address]
                address2 = route[address+1]
                agent_cost += int(self.cost_matrix[address1][address2])
            agent_cost_list.append({'agent_id': agent_id, 'cost': agent_cost})
            total_cost += agent_cost
            agent_id += 1
        return total_cost, agent_cost_list

    def run(self, bt=True):
        if (bt == True):
            # self.selectBestTriangle()
            self.selectSequenceTriangle()
        else:
            self.selectRandomTriangle()

        lowest_cost = {"cost": inf, "u": 0, "v": 0, "address": 0}

        while len(self.q) != 0:
            while len(self.partial_solution) <= self.p + 1:
                for x in self.q:
                    for i in range(0, len(self.partial_solution) - 1):
                        u = self.partial_solution[i]
                        v = self.partial_solution[i + 1]

                        cost_expression = self.cost_matrix[u][x] + \
                            self.cost_matrix[x][v] - self.cost_matrix[u][v]

                        # verifica se o custo de inserir o novo vértice
                        # no meio dos 2 é maior ou menor do que deixar o antigo
                        if (lowest_cost["cost"] > cost_expression):
                            lowest_cost["cost"] = cost_expression
                            lowest_cost["u"] = u
                            lowest_cost["v"] = v
                            lowest_cost["address"] = x

                        # self.printAnalysisOfCheaperInsertion(
                        #     cost_expression, x, u, v)

                if (len(self.q)):
                    position = self.partial_solution.index(
                        lowest_cost["u"]) + 1

                    self.partial_solution.insert(
                        position, lowest_cost["address"])

                    self.q.remove(int(lowest_cost["address"]))
                else:
                    break
                # reset lowest_cost after insert in solution
                lowest_cost = {"cost": inf, "u": 0, "v": 0, "address": 0}

            self.solution.append(self.partial_solution)

            # selecting the new triangle
            if (len(self.q) >= 2):
                if (bt == True):
                    # self.selectBestTriangle()
                    self.selectSequenceTriangle()
                else:
                    self.selectRandomTriangle()

                if(len(self.q) == 0):
                    self.solution.append(self.partial_solution)
            elif (len(self.q)):  # case self.q == 1
                self.solution.append([0] + self.q + [0])
                break
            else:
                break

        return self.solution
