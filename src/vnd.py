from copy import deepcopy


class VND:
    def __init__(self):
        self.switch = {
            1: self.swapInter,
            2: self.reinsertion,
            3: self.intra_2opt,
            4: self.swap,
        }

        self.neighborhoodMovementsName = {
            1: "swapInter(1,1)",
            2: "re-insertion",
            3: "2-opt",
            4: "swap",
        }

    def run(self, initial_solution, agent_list, cost_matrix):
        r = len(self.switch)
        k = 1  # tipo de estrutura de vizinhança corrente
        while (k <= r):
            func = self.switch.get(k)

            (sLine, new_agent_list) = func(
                deepcopy(initial_solution), deepcopy(agent_list), cost_matrix)

            if (self.f(new_agent_list) < self.f(agent_list)):
                initial_solution = sLine
                agent_list = new_agent_list
                k = 1
            else:
                k = k + 1
        return (initial_solution, agent_list)

    def f(self, agent_list):
        oF = 0
        for i in agent_list:
            oF += i['cost']
        return oF

    def swap(self, initial_solution, agent_list, cost_matrix):
        best_value = float('inf')
        best_difference = float('inf')
        best_i = 0
        best_j = 0
        best_s = 0

        for s_id in range(0, len(initial_solution)):
            s = initial_solution[s_id]
            oF = agent_list[s_id]['cost']
            # print(s, 'cost:', oF)

            # for with improved constant factors
            for i in range(1, len(s) - 1):
                for j in range(i+1, len(s) - 1):
                    # simulating the swap
                    swapped_element1 = s[i]
                    swapped_element2 = s[j]
                    swapped_element1_left = s[i-1]
                    swapped_element1_right = s[i+1]
                    swapped_element2_left = s[j-1]
                    swapped_element2_right = s[j+1]

                    # particular situation of adjacent vertices
                    if (j == i+1):
                        oFLine = oF - \
                            cost_matrix[swapped_element1_left][swapped_element1] - \
                            cost_matrix[swapped_element1][swapped_element1_right] - \
                            cost_matrix[swapped_element2][swapped_element2_right] + \
                            cost_matrix[swapped_element1_left][swapped_element2] + \
                            cost_matrix[swapped_element2][swapped_element2_left] + \
                            cost_matrix[swapped_element1][swapped_element2_right]
                    else:
                        oFLine = oF - \
                            cost_matrix[swapped_element1_left][swapped_element1] - \
                            cost_matrix[swapped_element1][swapped_element1_right] - \
                            cost_matrix[swapped_element2_left][swapped_element2] - \
                            cost_matrix[swapped_element2][swapped_element2_right] + \
                            cost_matrix[swapped_element1_left][swapped_element2] + \
                            cost_matrix[swapped_element2][swapped_element1_right] + \
                            cost_matrix[swapped_element2_left][swapped_element1] + \
                            cost_matrix[swapped_element1][swapped_element2_right]

                    if ((oFLine - oF) < best_difference):
                        best_difference = oFLine - oF
                        best_value = oFLine
                        best_i = i
                        best_j = j
                        best_s = s_id

        if best_value < agent_list[best_s]['cost']:
            agent_list[best_s]['cost'] = best_value
            aux = initial_solution[best_s][best_i]
            initial_solution[best_s][best_i] = initial_solution[best_s][best_j]
            initial_solution[best_s][best_j] = aux
        return (initial_solution, agent_list)

    def swapInter(self, s, agent_list, cost_matrix):
        best_value = float('inf')

        best_i_s1 = 0
        best_s1 = 0

        best_j_s2 = 0
        best_s2 = 0

        best_of_s1_s2 = float('inf')
        best_of_s1 = float('inf')
        best_of_s2 = float('inf')

        for s1_id in range(0, len(s)):
            oFs1 = agent_list[s1_id]['cost']
            for s2_id in range(s1_id + 1, len(s)):
                oFs2 = agent_list[s2_id]['cost']

                for i in range(1, len(s[s1_id]) - 1):
                    for j in range(1, len(s[s2_id]) - 1):

                        # simulating the swap
                        swapped_element1 = s[s1_id][i]
                        swapped_element2 = s[s2_id][j]
                        swapped_element1_left = s[s1_id][i - 1]
                        swapped_element1_right = s[s1_id][i + 1]
                        swapped_element2_left = s[s2_id][j - 1]
                        swapped_element2_right = s[s2_id][j + 1]

                        oFLineS1 = oFs1 - \
                            cost_matrix[swapped_element1_left][swapped_element1] - \
                            cost_matrix[swapped_element1][swapped_element1_right] + \
                            cost_matrix[swapped_element1_left][swapped_element2] + \
                            cost_matrix[swapped_element2][swapped_element1_right]

                        oFLineS2 = oFs2 - \
                            cost_matrix[swapped_element2_left][swapped_element2] - \
                            cost_matrix[swapped_element2][swapped_element2_right] + \
                            cost_matrix[swapped_element2_left][swapped_element1] + \
                            cost_matrix[swapped_element1][swapped_element2_right]

                        if ((oFLineS1 + oFLineS2) - (oFs1 + oFs2) < best_value):
                            best_value = (oFLineS1 + oFLineS2) - (oFs1 + oFs2)

                            best_of_s1_s2 = (oFLineS1 + oFLineS2)
                            best_of_s1 = oFLineS1
                            best_of_s2 = oFLineS2

                            best_i_s1 = i
                            best_s1 = s1_id

                            best_j_s2 = j
                            best_s2 = s2_id

        if (best_of_s1_s2 < (agent_list[best_s1]['cost'] + agent_list[best_s2]['cost'])):
            aux = s[best_s1][best_i_s1]
            s[best_s1][best_i_s1] = s[best_s2][best_j_s2]
            s[best_s2][best_j_s2] = aux

            agent_list[best_s1]['cost'] = best_of_s1
            agent_list[best_s2]['cost'] = best_of_s2

        return (s, agent_list)

    def reinsertion(self, initial_solution, agent_list, cost_matrix):
        best_value = float('inf')
        best_difference = float('inf')
        best_i = 0
        best_j = 0
        best_s = 0

        for s_id in range(0, len(initial_solution)):
            s = initial_solution[s_id]
            oF = agent_list[s_id]['cost']

            # controla o elemento que vai ser removido
            for i in range(1, len(s) - 1):
                # controla onde vai inserir o elemento
                for j in range(i+4, len(s) - 1):
                    # simulating reinsertion
                    swapped_element1 = s[i]
                    swapped_element2 = s[j]
                    swapped_element1_left = s[i-1]
                    swapped_element1_right = s[i+1]
                    swapped_element2_left = s[j-1]
                    swapped_element2_right = s[j+1]

                    oFLine = oF - \
                        cost_matrix[swapped_element1_left][swapped_element1] - \
                        cost_matrix[swapped_element1][swapped_element1_right] - \
                        cost_matrix[swapped_element2][swapped_element2_right] + \
                        cost_matrix[swapped_element1_left][swapped_element1_right] + \
                        cost_matrix[swapped_element2][swapped_element1] + \
                        cost_matrix[swapped_element1][swapped_element2_right]

                    if ((oFLine - oF) < best_difference):
                        best_difference = oFLine - oF

                        best_value = oFLine
                        best_i = i
                        best_j = j
                        best_s = s_id

        if best_value < agent_list[best_s]['cost']:
            agent_list[best_s]['cost'] = best_value
            element = initial_solution[best_s].pop(best_i)
            initial_solution[best_s].insert(best_j, element)

        return (initial_solution, agent_list)

    def intra_2opt(self, initial_solution, agent_list, cost_matrix):
        best_value = float('inf')
        best_difference = float('inf')
        best_i = 0
        best_j = 0
        best_s = 0

        for s_id in range(0, len(initial_solution)):
            s = initial_solution[s_id]
            oF = agent_list[s_id]['cost']

            # controla o primeiro ponto de corte
            for i in range(1, len(s) - 1):
                # controla o segundo ponto de corte
                for j in range(i+4, len(s) - 1):
                    # simulating 2-opt
                    swapped_element1 = s[i]
                    swapped_element2 = s[j]
                    swapped_element1_left = s[i-1]
                    swapped_element1_right = s[i+1]
                    swapped_element2_left = s[j-1]
                    swapped_element2_right = s[j+1]

                    oFLine = oF - \
                        cost_matrix[swapped_element1_left][swapped_element1] - \
                        cost_matrix[swapped_element2][swapped_element2_right] + \
                        cost_matrix[swapped_element1_left][swapped_element2] + \
                        cost_matrix[swapped_element1][swapped_element2_right]

                # no final lembrar de trocar o miolo, inverter
                    if ((oFLine - oF) < best_difference):
                        best_value = oFLine
                        best_difference = oFLine - oF

                        best_i = i
                        best_j = j
                        best_s = s_id

        if best_value < agent_list[best_s]['cost']:
            croppedList = initial_solution[best_s][best_i:best_j+1]

            leftCrop = initial_solution[best_s][:best_i]
            rightCrop = initial_solution[best_s][best_j+1:]

            reversedList = list(reversed(croppedList))

            # leftCrop + reversedList + rightCrop
            leftCrop.extend(reversedList)
            leftCrop.extend(rightCrop)

            initial_solution[best_s] = leftCrop
            agent_list[best_s]['cost'] = best_value

        return (initial_solution, agent_list)

    def showSolution(self, solution):
        for route in solution:
            print(', '.join(map(str, route)), end=';\n')

    def getRoutesTotalCost(self, solution, cost_matrix):
        total_cost = 0
        for route in solution:
            agent_cost = 0
            for address in range(0, len(route) - 1):
                address1 = route[address]
                address2 = route[address+1]
                agent_cost += int(cost_matrix[address1][address2])
            total_cost += agent_cost
        return total_cost
