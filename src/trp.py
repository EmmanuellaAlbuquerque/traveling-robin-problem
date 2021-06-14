from numpy import array
from numpy.lib.function_base import select


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
        self.solution = [0, int(self.d/2), self.d - 1, 0]
        self.q = []

        for i in range(0, self.d - 1):
            if i not in self.solution:
                self.q.append(i)

        # print(self.q)
        # print(self.cost_matrix)
        # print(self.solution)

    def run(self):
        lowest_cost = {"cost": 0, "u": 0, "v": 0, "address": 0}
        # while len(self.solution) < self.d:
        #     pass

        # while len(self.solution) < self.p:
        while len(self.solution) < self.d + 1:
            # while len(self.solution) < self.p + 1:
            for x in self.q:
                for i in range(0, len(self.solution) - 1):
                    u = self.solution[i]
                    v = self.solution[i + 1]

                    cost_expression = int(self.cost_matrix[u][x]) + \
                        int(self.cost_matrix[x][v]) - \
                        int(self.cost_matrix[u][v])
                    if (lowest_cost["cost"] > cost_expression):
                        lowest_cost["cost"] = cost_expression
                        lowest_cost["u"] = u
                        lowest_cost["v"] = v
                        lowest_cost["address"] = x
            # print(lowest_cost)
            position = self.solution.index(lowest_cost["u"]) + 1
            self.solution.insert(position, lowest_cost["address"])

            # reset lowest_cost after insert in solution
            lowest_cost["cost"] = 0
            self.q.remove(int(lowest_cost["address"]))

        print(self.solution)
