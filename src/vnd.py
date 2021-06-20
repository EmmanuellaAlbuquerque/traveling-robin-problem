def swap(initial_solution, agent_list, cost_matrix):
    for i in range(0, len(initial_solution)):
        s = initial_solution[i]
        oF = agent_list[i]['cost']
        print(s, 'cost:', oF)

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
                    foLine = oF - \
                        cost_matrix[swapped_element1_left][swapped_element1] - \
                        cost_matrix[swapped_element1][swapped_element1_right] - \
                        cost_matrix[swapped_element2][swapped_element2_right] + \
                        cost_matrix[swapped_element1_left][swapped_element2] + \
                        cost_matrix[swapped_element2][swapped_element2_left] + \
                        cost_matrix[swapped_element1][swapped_element2_right]
                    # print('f0',
                    #       '- c(', swapped_element1_left, swapped_element1,
                    #       ') - c(', swapped_element1, swapped_element1_right,
                    #       ') - c(', swapped_element2, swapped_element2_right,
                    #       ') + c(', swapped_element1_left, swapped_element2,
                    #       ') + c(', swapped_element2, swapped_element2_left,
                    #       ') + c(', swapped_element1, swapped_element2_right, ')')
                else:
                    foLine = oF - \
                        cost_matrix[swapped_element1_left][swapped_element1] - \
                        cost_matrix[swapped_element1][swapped_element1_right] - \
                        cost_matrix[swapped_element2_left][swapped_element2] - \
                        cost_matrix[swapped_element2][swapped_element2_right] + \
                        cost_matrix[swapped_element1_left][swapped_element2] + \
                        cost_matrix[swapped_element2][swapped_element1_right] + \
                        cost_matrix[swapped_element2_left][swapped_element1] + \
                        cost_matrix[swapped_element1][swapped_element2_right]

                    # print('f0',
                    #       '- c(', swapped_element1_left, swapped_element1,
                    #       ') - c(', swapped_element1, swapped_element1_right,
                    #       ') - c(', swapped_element2_left, swapped_element2,
                    #       ') - c(', swapped_element2, swapped_element2_right,
                    #       ') + c(', swapped_element1_left, swapped_element2,
                    #       ') + c(', swapped_element2, swapped_element1_right,
                    #       ') + c(', swapped_element2_left, swapped_element1,
                    #       ') + c(', swapped_element1, swapped_element2_right, ')')
                print('FO(result):', foLine)
        print(
            '---------------------------------------------------------------------')
