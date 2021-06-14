class RobinFileReader:
    def __init__(self, file):
        self.file = file

    def getResult(self):
        content = self.file.read().split("\n")
        dimension = [int(d) for d in content.pop(0).split() if d.isdigit()][0]
        p = [int(d) for d in content.pop(0).split() if d.isdigit()][0]
        content.pop(0)

        cost_matrix = list()
        for element in content:
            edges_costs = [number for number in element.split()
                           if number.isdigit()]
            if (edges_costs):
                cost_matrix.append(edges_costs)
        return (dimension, p, cost_matrix)
