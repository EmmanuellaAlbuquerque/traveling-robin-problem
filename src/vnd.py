class VND:
    def __init__(self):
        self.switch = {
            1: self.swap
        }

    def run(self, initial_solution, agent_list, cost_matrix):
        r = len(self.switch)
        k = 1  # tipo de estrutura de vizinhança corrente
        while (k <= r):
            func = self.switch.get(k)
            (sLine, new_agent_list) = func(
                initial_solution, agent_list, cost_matrix)
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
            print('agent', best_s+1)
            print(initial_solution[best_s],
                  'cost<initial>:', agent_list[best_s]['cost'])
            agent_list[best_s]['cost'] = best_value
            aux = initial_solution[best_s][best_i]
            initial_solution[best_s][best_i] = initial_solution[best_s][best_j]
            initial_solution[best_s][best_j] = aux
            print(initial_solution[best_s], 'cost<swap>:',
                  agent_list[best_s]['cost'], 'best(i, j):', best_i, best_j, '\n')
        else:
            print('cost<swap>: notbetter, agent', best_s+1,
                  '<compared>: ', best_value, '<', agent_list[best_s]['cost'])
        return (initial_solution, agent_list)
