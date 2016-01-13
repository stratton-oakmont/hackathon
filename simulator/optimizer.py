import os, sys, random, copy
import simulator, technical_indicators_alt, bot_maker
import tqdm

def initialize_population(pop_size):
    pop = [None]*pop_size
    for i in xrange(pop_size):
        pop[i] = bot_maker.create_bot(genome_stop_probability=0.1)
    return pop

def make_generation(seeds, num_children):
    #print seeds
    pop = [None]*len(seeds)*(num_children+1)
    i = 0
    for seed in seeds:
        #print seed
        pop[i] = seed
        i += 1
        for n in xrange(num_children):
            #print seed
            #run one mutation, TODO: variable number of mutations based on size
            #print 'Seed: ',seed
            bot = mutate(copy.deepcopy(seed))
            #print bot, bot != []
            if bot != []:
                pop[i] = bot
            else:
                #print "creating new bot"
                pop[i] = bot_maker.create_bot(genome_stop_probability=0.2)
            i += 1
    return pop

def mutate(bot):
    """mutate the bot.  Provides a wrapper to bot_maker, allowing us to tweak probabilities of mutations"""
    ratios = [(1,bot_maker.remove_chromosone),(30,bot_maker.mutate_chromosone),(5,bot_maker.add_chromosone)]
    total = float(sum(e[0] for e in ratios))
    threshold = 0.0
    thresholds = []
    for ratio in ratios:
        threshold += ratio[0]/total
        thresholds.append(threshold)
    mutators = [e[1] for e in ratios]
    probabilities = zip(thresholds,mutators)
    choice = random.random()
    #print probabilities, choice
    i = 0
    while choice>probabilities[i][0]:
        i+=1
    #execute the selected mutator
    mod = probabilities[i][1]
    bot = mod(bot)
    return bot

def score_generation(gen):
    """score the generation over a period from start to end"""
    periods = [random.randint(61,550) for n in xrange(10)]
    scores = []
    for bot in gen:
        avg_score = 0.0
        for period in periods:
            score = simulator.simulate_bot(bot, period, period+5, simulator.data)
            avg_score += score
        avg_score = avg_score/float(len(periods))
        scores.append((avg_score, bot))
    scores.sort(key=lambda e:e[0])
    scores.reverse()
    return scores

def optimize(pop_size, num_gens, num_survivors, verbose = True):
    """Use an asexual genetic algo to optimize the bots."""
    standard_period = 40 #standardize one testing period, to track progress
    gen = initialize_population(pop_size)
    num_children = int(pop_size/num_survivors)-1
    for n in tqdm.tqdm(range(num_gens)):
        scores = score_generation(gen)
        survivors = [e[1] for e in scores[:num_survivors]]
        if verbose == True:
            score = scores[0][0]
            std_score = simulator.simulate_bot(scores[0][1], standard_period, standard_period+5, simulator.data)
            print "Generation {},\tScore:{}\tStd score:{}".format(n+1,score,std_score)
        #print survivors
        gen = make_generation(survivors,num_children)
    return scores

def test_initialize_population():
    pop = initialize_population(3)
    for bot in pop:
        simulator.pprint_bot(bot)

def test_make_generation():
    pop = initialize_population(3)
    gen = make_generation(pop,3)
    assert len(gen) == 12
    print gen
    for bot in gen:
        simulator.pprint_bot(bot)
    return gen

def test_score_generation():
    gen = test_make_generation()
    scores = score_generation(gen)
    print scores

if __name__ == '__main__':
    random.seed(100)
    #test_initialize_population()
    #test_score_generation()

    #population generation childer
    scores = optimize(200,30,10)
    print scores
