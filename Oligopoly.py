import pprint
import random
import numpy

def populate_stochastic_matrix_1_die_roll(number_of_dice=2):
    matrix = []
    for i1 in range(0,6*number_of_dice+1):
        row = []
        for j1 in range(0,6*number_of_dice+1):
            if (i1 < j1 and j1 <= i1 + 6):
                row.append(1/6)
            else:
                row.append(0)
        matrix.append(row)
    return matrix

def populate_stochastic_matrix_full_board(number_of_dice=2,number_of_tiles=40):
    single_move_matrix = roll_x_number_of_dice(number_of_dice)
    matrix = []
    for i1 in range(0,number_of_tiles+1):
        row = numpy.full(number_of_tiles+1,0.0)
        for j1 in range(0,number_of_dice*6+1):
            if (i1+j1 < number_of_tiles+1):
                row[i1+j1] = single_move_matrix[j1] + row[i1+j1]
            else:
                row[number_of_tiles] = single_move_matrix[j1] + row[number_of_tiles]
        matrix.append(row)
    return matrix

def populate_state_matrix_game(number_of_tiles=40):
    matrix = numpy.full([1,number_of_tiles+1],0.0)
    matrix[0][0] = 1.0
    return matrix

def roll_1_die(state_matrix, stochastic_matrix):
    return numpy.matmul(state_matrix,stochastic_matrix)

def roll_x_number_of_dice(x=2):
    stochastic_matrix_1_die_roll = populate_stochastic_matrix_1_die_roll(x)
    results = numpy.full([1,6*x+1],0)[0]
    results[0] = 1
    for _1 in range(0,x):
        results = roll_1_die(results, stochastic_matrix_1_die_roll)
    return results

def play_round(starting_tile=0,number_of_dice=2,number_of_tiles=40):
    roll = 0
    for _2 in range(0,number_of_dice):
       roll += random.choice([1,2,3,4,5,6])
    landing_tile = starting_tile + roll
    if landing_tile > number_of_tiles:
        landing_tile = number_of_tiles
    return landing_tile

def play_game(results = [],number_of_dice=2,number_of_tiles=40):
    if len(results) == 0:
        results = numpy.full((number_of_tiles+1),0)
    tile = 0
    while (tile < number_of_tiles):
        tile = play_round(tile,number_of_dice,number_of_tiles)
        results[tile] += 1
    return results

def play_games(number_of_games,number_of_dice=2,number_of_tiles=40):
    results = numpy.full((number_of_tiles+1), 0)
    for g1 in range(0,number_of_games):
        results = play_game(results,number_of_dice,number_of_tiles)
    return results.tolist()

def normalize_list(games_results):
    games_results.pop()
    sum_results = sum(games_results)
    normalized_results = numpy.array(games_results) / sum_results
    return normalized_results.tolist()

def apply_markov_chains(number_of_dice=2,number_of_tiles=40):
    stochastic_matrix_full_board = populate_stochastic_matrix_full_board(number_of_dice,number_of_tiles)
    state_matrix_game = populate_state_matrix_game(number_of_tiles)
    probability_board = numpy.full((1, number_of_tiles+1), 0.0)
    is_game_finished = False
    rounds = 0
    while (not (is_game_finished)):
        rounds += 1
        state_matrix_round = numpy.matmul(state_matrix_game, stochastic_matrix_full_board)
        if (rounds > number_of_tiles/number_of_dice+1):
            is_game_finished = True
        else:
            probability_board = probability_board + state_matrix_round
            state_matrix_game = state_matrix_round
    return probability_board[0].tolist()

def markov_chain_vs_simulation(number_of_simulations=1000,number_of_dice=2,number_of_tiles = 40):
    #First find the answer by Markov Chai
    markov_chain_results = apply_markov_chains(number_of_dice,number_of_tiles)
    normalized_markov_chain_results = normalize_list(markov_chain_results)

    #Then run simulations to validate the Markov Chain results
    game_simulation_results = play_games(number_of_simulations,number_of_dice)
    normalized_game_simulation_results = normalize_list(game_simulation_results)
    print('Tile' + '\t' + 'Prob from Markov Chain' + '\t' + 'Prob from Simulation' + '\t' + 'Discrepancy'
    )
    for i3 in range(0,number_of_tiles):
        print(str(i3) + '\t' + str(round(normalized_markov_chain_results[i3],5)) + '\t' + str(round(normalized_game_simulation_results[i3],5))+ '\t' + str(round(normalized_game_simulation_results[i3]-normalized_markov_chain_results[i3],4)))

    frequency_of_most_frequent_tile = numpy.max(normalized_markov_chain_results)
    most_frequent_tile = normalized_markov_chain_results.index(frequency_of_most_frequent_tile)
    frequency_of_least_frequent_tile = numpy.min([normalized_markov_chain_results[p] for p in range(10,number_of_tiles)])
    least_frequent_tile = normalized_markov_chain_results.index(frequency_of_least_frequent_tile)
    max_error = numpy.max([abs(normalized_game_simulation_results[i4]-normalized_markov_chain_results[i4]) for i4 in range(0,number_of_tiles)])
    print()
    print('The max discrepancy found between the simulation and Markov chain methods is: {0}%'.format((round(max_error*100,5))))
    print('Fiddler: The most frequently visited tile is: {0} at {1}%'.format(most_frequent_tile,round(frequency_of_most_frequent_tile*100,5)))
    print('Extra Credit: The least frequently visited tile (Tile 10 or higher) is: {0} at {1}%'.format(least_frequent_tile,round(frequency_of_least_frequent_tile*100,5)))

def markov_chains_for_different_numbers_of_dice(max_number_of_dice=30,number_of_tiles=1000):
    all_results = numpy.full((number_of_tiles,max_number_of_dice),0.0)
    for num_of_dice in range(1,max_number_of_dice):
        results = apply_markov_chains(num_of_dice,number_of_tiles)
        normalized_results = normalize_list(results)
        for tile_number in range(0,number_of_tiles):
            all_results[tile_number][num_of_dice] = round(normalized_results[tile_number]*number_of_tiles,5)
    numpy.savetxt('results.csv',all_results,delimiter='\t')

markov_chain_vs_simulation(number_of_simulations=1000000,number_of_dice=2,number_of_tiles = 40)
#markov_chains_for_different_numbers_of_dice()