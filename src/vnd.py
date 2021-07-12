from copy import deepcopy


class VND:
    def __init__(self):
        self.switch = {
            1: self.swap,
            2: self.swapInter,
            3: self.reinsertion
        }

        self.neighborhoodMovementsName = {
            1: "swap",
            2: "swapInter(1,1)",
            3: "re-insertion",
        }

    def run(self, initial_solution, agent_list, cost_matrix):
        # exc = 0
        r = len(self.switch)
        k = 1  # tipo de estrutura de vizinhança corrente
        while (k <= r):
            func = self.switch.get(k)
            (sLine, new_agent_list) = func(
                deepcopy(initial_solution), deepcopy(agent_list), cost_matrix)
            # print('---init---')
            # print(agent_list)
            # print(new_agent_list)
            # print('----------')
            if (self.f(new_agent_list) < self.f(agent_list)):
                # exc += 1
                initial_solution = sLine
                # print(self.neighborhoodMovementsName.get(k), 'exec', exc)
                # self.showSolution(initial_solution)
                # print('total cost:', self.getRoutesTotalCost(
                #     initial_solution, cost_matrix))
                # print('\n')
                agent_list = new_agent_list
                k = 1
                # print('BEST found', 'k.value:', k)
            else:
                k = k + 1
                # print('BEST not found', 'k.value:', k)
        return (initial_solution, agent_list)

    def f(self, agent_list):
        oF = 0
        for i in agent_list:
            oF += i['cost']
        return oF

    def swap(self, initial_solution, agent_list, cost_matrix):
        best_value = float('inf')
        best_i = 0
        best_j = 0
        best_s = 0
        for s_id in range(0, len(initial_solution)):
            s = initial_solution[s_id][:]
            oF = agent_list[s_id]['cost']

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
                            cost_matrix[swapped_element2][swapped_element2_right] + \
                            cost_matrix[swapped_element1_left][swapped_element2] + \
                            cost_matrix[swapped_element1][swapped_element2_right]
                        # print('f0',
                        #       '- c(', swapped_element1_left, swapped_element1,
                        #       ') - c(', swapped_element2, swapped_element2_right,
                        #       ') + c(', swapped_element1_left, swapped_element2,
                        #       ') + c(', swapped_element1, swapped_element2_right, ')')
                    else:
                        oFLine = oF - \
                            cost_matrix[swapped_element1_left][swapped_element1] - \
                            cost_matrix[swapped_element2][swapped_element2_right] + \
                            cost_matrix[swapped_element1_left][swapped_element2] + \
                            cost_matrix[swapped_element1][swapped_element2_right]

                        # print('f0',
                        #       '- c(', swapped_element1_left, swapped_element1,
                        #       ') - c(', swapped_element2, swapped_element2_right,
                        #       ') + c(', swapped_element1_left, swapped_element2,
                        #       ') + c(', swapped_element1, swapped_element2_right, ')')
                    if (oFLine < best_value):
                        best_value = oFLine
                        best_i = i
                        best_j = j
                        best_s = s_id
                    # print('ObjectFunction(result):', oFLine)
            # print(
            #     '---------------------------------------------------------------------')
        if best_value < agent_list[best_s]['cost']:
            # print('agent', best_s+1)
            # print(initial_solution[best_s],
            #       'cost<initial>:', agent_list[best_s]['cost'])
            agent_list[best_s]['cost'] = best_value
            aux = initial_solution[best_s][best_i]
            initial_solution[best_s][best_i] = initial_solution[best_s][best_j]
            initial_solution[best_s][best_j] = aux
            # print(initial_solution[best_s], 'cost<swap>:',
            #       agent_list[best_s]['cost'], 'best(i, j):', best_i, best_j, '\n')
        # else:
        #     print('cost<swap>: notbetter, agent', best_s+1,
        #           '<compared>: ', best_value, '<', agent_list[best_s]['cost'])
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
                        # print(s[s1_id][i], s[s2_id][j])
                        # print('ObjectFunction(before, s):', oFs1)
                        # print('ObjectFunction(before, s+):', oFs2)

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
                        # print('f0',
                        #       '- c(', swapped_element1_left, swapped_element1,
                        #       ') - c(', swapped_element1, swapped_element1_right,
                        #       ') + c(', swapped_element1_left, swapped_element2,
                        #       ') + c(', swapped_element2, swapped_element1_right, ')')
                        oFLineS2 = oFs2 - \
                            cost_matrix[swapped_element2_left][swapped_element2] - \
                            cost_matrix[swapped_element2][swapped_element2_right] + \
                            cost_matrix[swapped_element2_left][swapped_element1] + \
                            cost_matrix[swapped_element1][swapped_element2_right]
                        # print('f0+',
                        #       '- c(', swapped_element2_left, swapped_element2,
                        #       ') - c(', swapped_element2, swapped_element2_right,
                        #       ') + c(', swapped_element2_left, swapped_element1,
                        #       ') + c(', swapped_element1, swapped_element2_right, ')')
                        # print((oFLineS1 + oFLineS2) < oFs1 + oFs2)
                        # a melhor solução s1 e s2 é a que tiver a soma das
                        # funções objetivos (s1+s2) com menor diferença da sulução original
                        # print('---------------------------------------')
                        # print('BEST.VALUE:', best_value)
                        if ((oFLineS1 + oFLineS2) - (oFs1 + oFs2) < best_value):
                            best_value = (oFLineS1 + oFLineS2) - (oFs1 + oFs2)

                            best_of_s1_s2 = (oFLineS1 + oFLineS2)
                            best_of_s1 = oFLineS1
                            best_of_s2 = oFLineS2

                            best_i_s1 = i
                            best_s1 = s1_id

                            best_j_s2 = j
                            best_s2 = s2_id
                        # print('ObjectFunction(result, s):', oFLineS1)
                        # print('ObjectFunction(result, s+):', oFLineS2)
        # print('\nINFO =-= BESTVALUE')
        # print('BEST.VALUE:', best_value)
        # print(s[best_s1], s[best_s2])
        # print(s[best_s1][best_i_s1], s[best_s2][best_j_s2])
        # print(best_s1, best_s2)

        # print('\n')
        # print(best_of_s1_s2 < (
        #     agent_list[best_s1]['cost'] + agent_list[best_s2]['cost']))
        # print(('before', agent_list[best_s1]
        #       ['cost'] + agent_list[best_s2]['cost']))
        # print(('after', best_of_s1_s2))
        # print('best s1:', best_of_s1)
        # print('best s2:', best_of_s2)
        # print('original s1', agent_list[best_s1]['cost'])
        # print('original s2', agent_list[best_s2]['cost'])
        # print('\n')

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
                for j in range(1, len(s) - 1):
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
