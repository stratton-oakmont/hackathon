# making the bots by having a random descriptor
#loop over all bots
import random
import technical_indicators_alt, simulator

weights = [-1,-0.8,-0.6,-0.4,-0.2,1,0.8,0.6,0.4,0.2]

def create_bot(genome_stop_probability = 0.5):
    bot = []
    bot = add_chromosone(bot)
    while random.random()>genome_stop_probability:
    #randomly make descriptor for bot
        bot = add_chromosone(bot)
    return bot

def funcname_mut(bot):
    x = technical_indicators_alt.func_ref.keys()
    x.sort()
    funcname = random.choice(x)
    t = random.choice(bot)
    bot.remove(t)
    lst = list(t)
    lst[0] = funcname
    t = tuple(lst)
    bot.append(t)
    return bot

def stockname_mut(bot):
    y = simulator.data.keys()
    y.sort()
    stock_name = random.choice(y)
    t = random.choice(bot)
    bot.remove(t)
    lst = list(t)
    lst[1] = stock_name
    t = tuple(lst)
    bot.append(t)
    return bot

def wt_mut(bot):
    #simulator.pprint_bot(bot)
    #print
    botbot.remove(t)
    lst = list(t)
    updown = random.random()
    if updown > 0.5:
        if lst[2]=1:
                return bot
        lst[2] = lst[2] + 0.2
    else:
        if lst[2]=-1:
                return bot
        lst[2] = lst[2] - 0.2

    t = tuple(lst)
    bot.append(t)
    return bot

def remove_chromosone(bot):
    t = random.choice(bot)
    bot.remove(t)
    return bot

def add_chromosone(bot):
    wt=0.2
    x = technical_indicators_alt.func_ref.keys()
    x.sort()
    func_name = random.choice(x)
    y = simulator.data.keys()
    y.sort()
    stock_name = random.choice(y)
    lst = [func_name,stock_name,wt]
    t=tuple(lst)
    bot.append(t)
    return bot

def mutate_chromosone(bot):
    """mutate one component of the bot chromosome, selected with uniform random probability"""
    mods = [wt_mut, stockname_mut, funcname_mut]
    mod = random.choice(mods)
    return mod(bot)

def test_bot_maker():
    random.seed(103)
    bot = create_bot(genome_stop_probability=0.3)
    simulator.pprint_bot(bot)
    bot = funcname_mut(bot)
    simulator.pprint_bot(bot)
    bot = stockname_mut(bot)
    simulator.pprint_bot(bot)
    bot = wt_mut(bot)
    simulator.pprint_bot(bot)
    bot = remove_chromosone(bot)
    simulator.pprint_bot(bot)

if __name__ == '__main__':
    test_bot_maker()
