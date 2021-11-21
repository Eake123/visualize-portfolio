import matplotlib.pyplot as plt
import matplotlib.animation as anim
import os
import requests
import json
import os
# currency to measure
CURR = 'usd'
# save the txt files to this directory. If set to none it saves where this script is run
DIRECT = None
# how many ticks the plot shows
SHOW = 200
# the name of the market file
MARKET_FILE = 'market_owned.txt'
# if own is set to true it shows your portfolio, if set to false it saves to a different file and doesn't effect your portfolio txt
OWN = True
# the time it takes to refresh the plot. 60000 is one minute, 5 mins = 300000
REFRESH = 60000

# if own is set to False this needs to be filled. it has to be a list of the coins you want to plot ex. ['bnb','eth','algo']
COINS = None
# amount has to be filled if own is set to false. It is the amount of money you want your plot to use for the bottom subplot
AMOUNT = None
class Json:


    def __init__(self,file,directory=None):
        self.file = file
        self.fileKey = file.replace(".txt","")
        self.directory = directory if directory is not None else None
        

    
    
    def changeDump(self,info):
        if isinstance(self.directory,str):
            os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
        json_decoded.update({self.fileKey:info})
        with open(self.file, 'w') as f:
            f.write(json.dumps(json_decoded, sort_keys=True, indent=4, separators=(',', ': ')))
    
    
    def dicDump(self,infoDic):
        if isinstance(self.directory,str):
            os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
        dic = json_decoded[self.fileKey]
        fullDic = {}
        for i in dic.keys():
            if(infoDic.get(i) == None):
                fullDic[i] = dic[i]
            else:
                fullDic[i] = dic[i] + infoDic[i]
        for j in infoDic.keys():
            if(dic.get(j) == None):
                fullDic[j] = infoDic[j]
        realDic = {self.fileKey:fullDic}
        with open(self.file, 'w') as f:
            f.write(json.dumps(realDic, sort_keys=True, indent=4, separators=(',', ': ')))

    
    def addDump(self,add):
        if isinstance(self.directory,str):
            os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
        dic = json_decoded[self.fileKey]
        dic.append(add)
        realDic = {self.fileKey:dic}
        with open(self.file, 'w') as f:
            f.write(json.dumps(realDic, sort_keys=True, indent=4, separators=(',', ': ')))
    
    def createDump(self,add):
        if isinstance(self.directory,str):
            os.chdir(self.directory)
        dic = {self.fileKey:add}
        with open(self.file, 'w') as f:
            f.write(json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': ')))
    
    
    def readKey(self):
        if isinstance(self.directory,str):
            os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
        dic = json_decoded[self.fileKey]
        return dic
    
    def techReadKey(self):
        if isinstance(self.directory,str):
            os.chdir(self.directory)
        with open(self.file, 'r') as f:
            json_decoded = json.loads(f.read())
        value = []
        for j in range(len(json_decoded)):
            for i in json_decoded[j].values():
                value.append(i)
        return json_decoded, value

    def APIDump(self,add):
        if isinstance(self.directory,str):
            os.chdir(self.directory)
        try:
            with open(self.file, 'r') as f:
                json_decoded = json.loads(f.read())
            dic = json_decoded[self.fileKey]
            dic = dic + add
        except:
            dic = {self.fileKey:add}
        with open(self.file, 'w') as f:
            f.write(json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': ')))
        
    def dualDump(self,add):
        '''do not make it a list'''
        try:
            self.addDump(add)
        except:
            self.createDump([add])


    def jsonNuke(self,str):
        if isinstance(self.directory,str):
            os.chdir(self.directory)
        if(str == True):
            nuke = {self.fileKey:["N/A"]}
        else:
            nuke = {self.fileKey:{"N/A":1}}
        with open(self.file, 'w') as f:
            f.write(json.dumps(nuke, sort_keys=True, indent=4, separators=(',', ': ')))

    
    def in_json(self,condition) -> bool:
        if condition in self.readKey():
            return True
        else:
            return False
class gecko_getter_coin:
    def __init__(self,ticker) -> None:
        if isinstance(ticker,list):
            self.ticker = ','.join(ticker)
        else:
            self.ticker = ticker
        self.sess = requests.Session()

    
    def get_ticker(self):
        return self._url(self.ticker,'tickers')
    

    def get_coin_id(self):
        return self._url(self.ticker)
    
    def get_market_chart_range(self,before,to,currency='usd'):
        parameter = {
            'vs_currency':currency,
            'from':convert_time(before),
            'to':convert_time(to)
        }
        return self._url('coins',self.ticker,'market_chart','range',parameter=parameter)
    
    def get_ohlc(self,days,currency='usd'):
        parameter = {
            'id':self.ticker,
            'vs_currency':currency,
            'days':days
        }
        return self._url('coins',self.ticker,'ohlc',parameter=parameter)

    def get_coin_list(self,include_platform='false'):
        parameter = {
            'include_platform':include_platform
        }
        return self._url('coins','list',parameter=parameter)


    def get_market_chart(self,days,currency='usd',interval='Hourly'):
        parameter = {
            'id':self.ticker,
            'vs_currency':currency,
            'days':days,
            'interval':interval
        }
        return self._url('coins',self.ticker,'market_chart',parameter=parameter)

    def get_markets(self,vs_currency='usd',ids=None,category=None,order='market_cap_desc',per_page='100',page='1',sparkline='false',price_change_percentage=None):
        parameter = {
            'vs_currency':vs_currency,
            'ids':None,
            'category':category,
            'order':order,
            'per_page':per_page,
            'page':page,
            'sparkline':sparkline,
            'price_change_percentage':price_change_percentage
        }
        return self._url('coins','markets',parameter=parameter)
    

    def get_price(self,vs_currencies='usd',include_market_cap='true',include_24hr_vol=False,include_24hr_change=False,include_last_updated_at=False):
        parameter = {
            'ids':self.ticker,
            'vs_currencies':vs_currencies,
            'include_market_cap':include_market_cap,
            'include_24hr_vol':include_24hr_vol,
            'include_24hr_change':include_24hr_change,
            'include_last_updated_at':include_last_updated_at
        }
        return self._url('simple','price',parameter=parameter)
        

    def _url(self,*attributes,parameter=None):
        parameter = parameter if parameter is not None else None
        url = 'http://api.coingecko.com/api/v3'
        
        for attribute in attributes:
            url += '/' + attribute
        
        
        r = self.sess.get(url,params=parameter)
        return r.json()
class coin:
    def __init__(self,symbol,suffix='') -> None:
        self.symbol = symbol + suffix
        self.gec = gecko_getter_coin(self.symbol)


    def gecko_id(self):
        J = Json('coin_ids.txt',directory=DIRECT)
        dic = J.readKey()
        for ticker in dic:
            for key,value in ticker.items():
                if self.symbol.lower() == value.lower():
                    return ticker['id']



def get_port_coins():
    try:
        J = Json('own_port.txt',DIRECT)
        return list(J.readKey().keys())
    except:
        return list(make_market_owned().keys())

def add_to_json(key,value):
    file_name = key + 'visual.txt' 
    J = Json(file_name,directory=DIRECT)
    J.dualDump(value)
    dic = J.readKey()
    if len(dic) > SHOW:
        return dic[-SHOW:]
    else:
        return dic
def owned_perc(symbol,price):
    J = Json('own_port.txt',DIRECT)
    for key,value in J.readKey().items():
        if key == symbol:
            return price *value



def perc_dic(dic):
    dic_new = {}
    for key,value in dic.items():
        # print(key,value,'---------------------------------------------------------------')
        if OWN == False:
            dic_new[key] = add_to_json(key,value[CURR])
        else:
            v = owned_perc(key,value[CURR])
            dic_new[key] = add_to_json(key,v)
    return dic_new

def get_coins(coins):
    g = gecko_getter_coin(coins)
    return g.get_price(vs_currencies=CURR)


def total_cap(dic):
    m_cap = 0
    m_str = CURR + '_market_cap'
    for i in dic.values():
        m_cap += i[m_str]
    return m_cap


def percentage(dic_old):
    dic = {}
    total_mc = total_cap(dic_old)
    m_str = CURR + '_market_cap'
    for key,item in dic_old.items():
        dic[key] = item[m_str] / total_mc
    new_dic = {}
    for key,value in dic_old.items():
        for key2,value2 in dic.items():
            if key == key2:
                value['perc'] = value2
                new_dic[key] = value
    return new_dic

def owned_amount(dic,amount) -> list:
    dic = percentage(dic)
    new_dic = {}
    for key,item in dic.items():
        money = amount * item['perc']
        owned = money / item[CURR]
        new_dic[key] = owned
    J = Json(MARKET_FILE,DIRECT)
    J.createDump(new_dic)
    return multiply_market(dic,new_dic,True)


def check_same(dic,new_dic):
    for key in dic.keys():
        if key not in new_dic:
            return False
    for key in new_dic.keys():
        if key not in dic:
            return False
    return True

def perc_json(dic):
    J = Json(MARKET_FILE,DIRECT)
    new_dic = J.readKey()
    if check_same(dic,new_dic) == False:
        raise Exception
    return multiply_market(dic,new_dic,False)
    


def my_own(dic):
    J = Json('own_port.txt',DIRECT)
    new_dic = J.readKey()
    return multiply_market(dic,new_dic,False,True)

def multiply_market(dic,new_dic,new_market,owned=False):
    t = 0
    for key,value in dic.items():
        for key_owned,value_owned in new_dic.items():
            if key == key_owned:
                t += value[CURR] * value_owned
    if owned == False:
        return add_to_json('market',t)
    else:
        return add_to_json('market_owned',t)




def total_market(dic,amount):
    if OWN == True:
        return my_own(dic)
    else:
        try:
            l = perc_json(dic)
        except:
            l = owned_amount(dic,amount)
        return l
        




def market_analysis(coins,amount):
    dic = get_coins(coins)
    ticker_dic = perc_dic(dic)
    ticker_dic['market'] = total_market(dic,amount)
    return ticker_dic

def plot_port(file,y,ax,i):
    x = range(len(y))
    ax.clear()
    ax.plot(x,y)
    ax.set_ylabel(file)



def verify_coins(coins):
    ver_coin = []
    for ticker in coins:
        c = coin(ticker)
        ver_coin.append(c.gecko_id())
    return ver_coin

def while_update(coins=None,amount=None):
    if OWN == True:
        coins = get_port_coins()
    else:
        coins = verify_coins(coins)
    plt.style.use('dark_background')
    coin_len = len(coins) + 1
    vis = [x for x in plt.subplots(coin_len,1)]
    fig = vis[0]
    sub = vis[1:]
    sub = sub[0]
    def update_y(i):
        count = 0
        market_dic = market_analysis(coins,amount)
        for key,value in market_dic.items():
            plot_port(key,value,sub[count],i)
            count += 1
    a = anim.FuncAnimation(fig,update_y,frames=10000,interval=60000,repeat=False)
    plt.show()


def make_market_owned(just_add=False):
    if just_add == False:
        dic = {}
        J = Json('own_port.txt',DIRECT)
    else:
        J = Json('market_ownedvisual.txt',DIRECT)
        dic = J.readKey()
    while True:
        a = str(input('enter ticker, enter 1 to break: '))
        if a == '1':
            break
        else:
            b = float(input('enter the amount of %s you have: ' %(a)))
            c = coin(a)
            key = c.gecko_id()
            dic[key] = b
    J = Json('own_port.txt',DIRECT)
    J.createDump(dic)
    return dic

if __name__ == '__main__':
    while_update(coins=COINS,amount=AMOUNT)

    # make_market_owned(True)