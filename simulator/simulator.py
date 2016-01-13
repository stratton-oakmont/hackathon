import os, sys, math
import tqdm
import numpy as np
import collections
import technical_indicators_alt

def execute_bot(bot, day, data):
    """pass the desired data to the bot"""
    stock_dict = collections.defaultdict(float)
    for strategy in bot:
        stock_data = data[strategy.stock]
        stock_data = stock_data[day-30:day]
        #print strategy.stock, stock_data
        decision = strategy.func(stock_data)
        stock_dict[strategy.stock] += strategy.weight*decision
    return stock_dict

def compile_bot(bot_desc):
    """given a description of the bot genome, produce the python structure for it"""
    Strategy = collections.namedtuple('Strategy',['func','stock','weight'])
    bot = []
    #normalize the weights: the total potential bot volume should be 1.0
    total_weight = float(sum([abs(s[2]) for s in bot_desc]))
    for strategy_string in bot_desc:
        s = Strategy(func = technical_indicators_alt.func_ref[strategy_string[0]],
                stock = strategy_string[1],
                weight = strategy_string[2]/total_weight)
        bot.append(s)
    return bot

def assets_change(stock_dict,assets,day,data):
    """given the stock buys and sells in the stock dict, calculate the net change in assets"""
    money = 0
    for stock in stock_dict.keys():
        assets[stock] = assets[stock]+stock_dict[stock]
        assets['cash'] = assets['cash'] - data[stock][day][3]*stock_dict[stock]
    return assets

def value_assets(assets, day, data):
    cash = 0.0
    for stock in assets.keys():
        if stock == 'cash':
            cash += assets['cash']
        else:
            cash += data[stock][day][3]*assets[stock]
    return cash

def simulate_bot(bot, start, end, data):
    """run the bot over the specified period.  At then end, calculate the total assets of the bot in cash on the end day"""
    bot = compile_bot(bot)
    assets = collections.defaultdict(float)
    for day in tqdm.tqdm(xrange(start, end)):
        stock_decision = execute_bot(bot, day, data)
        #merge the new assets with the old assets
        assets = assets_change(stock_decision,assets,day,data)
    #calculate the net value of the assets
    val = value_assets(assets, end, data)
    return val

def parse_data():
    #for now, really manual process
    path = os.getcwd()
    path = os.path.join(path,'data')
    data = {}
    #get list of folders with stock data
    folders = [o for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]
    for folder in folders:
        print 'Importing {}'.format(folder)
        stock_name = folder
        folder_path = os.path.join(path,folder)
        f = open(os.path.join(folder_path,'quote.csv'),'r')
        lines = f.readlines()
        f.close()
        stock_data = []
        for l in lines[1:]:
            l = l.strip()
            if l!='':
                l_data = l.split(',')
                l_data = l_data[1:]
                l_data = [float(d) for d in l_data]
                #flip high and low values for josh
                t = l_data[1]
                l_data[1] = l_data[2]
                l_data[2] = t
            stock_data.append(tuple(l_data))
        stock_data = tuple(stock_data)
        stock_data = stock_data[::-1] #reverse the data
        data[stock_name] = stock_data
    return data

def test_execute_bot(data):
    stocks = data.keys()
    stocks.sort()
    funcs = technical_indicators_alt.func_ref.keys()
    funcs.sort()
    weights = [-1,-0.5,0.5,1]
    #bot = [(funcs[0],stocks[0],weights[0]),
    #    (funcs[0],stocks[1],weights[0])]
    bot = [(f,s,weights[-1]) for f in funcs for s in stocks]
    pprint_bot(bot)
    bot = compile_bot(bot)
    results = execute_bot(bot,300,data)
    print results

def pprint_bot(bot_desc):
    print 'Bot:'
    for s in bot_desc:
        print '\t{}\t{}\t{}'.format(s[1],s[0],s[2])

def test_import_data():
    data = parse_data()
    #print data.keys(), len(data[data.keys()[0]]), data[data.keys()[0]][0:10]
    return data

def test_simulate_bot(data):
    stocks = data.keys()
    stocks.sort()
    funcs = technical_indicators_alt.func_ref.keys()
    funcs.sort()
    weights = [-1,-0.5,0.5,1]
    #bot = [(funcs[0],stocks[0],weights[0]),
    #    (funcs[0],stocks[1],weights[0])]
    bot = [(f,s,weights[-1]) for f in funcs for s in stocks]
    bot = compile_bot(bot)
    start = 200
    end = 500
    v = simulate_bot(bot, start, end, data)
    print v

data = parse_data()

if __name__ == '__main__':
    #data = test_import_data()
    #test_execute_bot(data)
    test_simulate_bot(data)
