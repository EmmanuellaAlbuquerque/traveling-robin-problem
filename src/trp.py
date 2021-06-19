from numpy import array, inf
from bisect import insort


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

        self.selectBestTriangle()
        # self.selectRandomTriangle(int(self.d/2), self.d - 1)

    def selectBestTriangle(self):
        self.partial_solution = [0]
        # encontra o triângulo no qual as cidades são as mais distantes possíveis
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

    def selectRandomTriangle(self, random_address1, random_address2):
        # escolha aleatória de cidades
        # self.partial_solution = [0, int(self.d/2), self.d - 1, 0]
        # random_address1 = 0
        # random_address2 = 1

        # self.partial_solution = [
        #     0, self.q[random_address1], self.q[random_address2], 0]
        self.partial_solution = [
            0, random_address1, random_address2, 0]
        self.q.remove(random_address1)
        self.q.remove(random_address2)

    def printAnalysisOfCheaperInsertion(self, cost, x, u, v):
        print('menor valor:', cost,
              '-> vértice:', x, 'inserção entre: (', u, ',', v, ')')

    def run(self):
        lowest_cost = {"cost": inf, "u": 0, "v": 0, "address": 0}

        while len(self.q) != 0:
            while len(self.partial_solution) < self.p + 1:
                for x in self.q:
                    for i in range(0, len(self.partial_solution) - 1):
                        u = self.partial_solution[i]
                        v = self.partial_solution[i + 1]

                        cost_expression = int(self.cost_matrix[u][x]) + \
                            int(self.cost_matrix[x][v]) - \
                            int(self.cost_matrix[u][v])
                        if (lowest_cost["cost"] > cost_expression):
                            lowest_cost["cost"] = cost_expression
                            lowest_cost["u"] = u
                            lowest_cost["v"] = v
                            lowest_cost["address"] = x

                        # self.printAnalysisOfCheaperInsertion(
                        #     cost_expression, x, u, v)
                position = self.partial_solution.index(lowest_cost["u"]) + 1
                self.partial_solution.insert(position, lowest_cost["address"])

                # reset lowest_cost after insert in solution
                lowest_cost["cost"] = inf
                self.q.remove(int(lowest_cost["address"]))

            self.solution.append(self.partial_solution)

            # selecting the new triangle
            if (len(self.q) >= 2):
                self.selectBestTriangle()
                # self.selectRandomTriangle(self.q[0], self.q[1])
                if(len(self.q) == 0):
                    self.solution.append(self.partial_solution)

        print(self.solution, 'solution')
