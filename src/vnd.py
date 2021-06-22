def swap(initial_solution, agent_list, cost_matrix):
    for s_id in range(0, len(initial_solution)):
        s = initial_solution[s_id][:]
        oF = agent_list[s_id]['cost']
        best_value = float('inf')
        best_i = 0
        best_j = 0

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
                # print('ObjectFunction(result):', oFLine)
        # print(
        #     '---------------------------------------------------------------------')
        if best_value < agent_list[s_id]['cost']:
            agent_list[s_id]['cost'] = best_value
            initial_solution[s_id][best_i] = s[best_j]
            initial_solution[s_id][best_j] = s[best_i]
            print('\n', s, 'cost<initial>:', oF)
            print('agent', s_id+1, initial_solution[s_id], 'cost<swap>:',
                  agent_list[s_id]['cost'], 'best(i, j):', best_i, best_j, '\n')
        else:
            print('cost<swap>: notbetter, agent', s_id+1)
    return (initial_solution, agent_list)
