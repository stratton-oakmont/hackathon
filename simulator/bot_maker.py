
# making the bots by having a random descriptor

#loop over all bots
import random

def create_bot():
    for bot in list_of_bots

        wtlist = [-1, -0.5, 0.5, 1]
        x = technical_indicators_alt.funct_ref.keys()
        x.sort()
        y = technical_indicators_alt.func_ref.keys()
        y.sort()

        for des_num in size_of_genome
        #randomly make descriptor for bot


            add_chromosone(bot)

        return bot



def functname_mut(bot):
        x = technical_indicators_alt.funct_ref.keys()
        x.sort()
        functname = random.choice(x))
        t = random.choice(bot)
        lst = list(t)
        lst[0] = wt
        t = tuple(lst)
        bot.append(t)
        return bot

def stockname_mut(bot):
        y = technical_indicators_alt.func_ref.keys()
        y.sort()
        functname = random.choice(y)
        t = random.choice(bot)
        lst = list(t)
        lst[1] = functname
        t = tuple(lst)
        bot.append(t)
        return bot

def wt_mut(bot):
        wtlist = [-1, -0.5, 0.5, 1]
        wt=random.choice(wtlist))
        t = random.choice(bot)
        lst = list(t)
        lst[2] = wt
        t = tuple(lst)
        bot.append(t)
        return bot

def remove_chromosone(bot):
        t = random.choice(bot)
        del bot[t]

        return bot

def add_chromosone(bot):
        wt=random.choice(wtlist))
        functname = random.choice(x))
        stock_name = random.choice(y))
        lst[] = [wt,functname,stockname]
        t=tuple(lst)

        bot.extend(t)


        return bot
