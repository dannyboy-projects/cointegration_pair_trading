import pandas as pd
from datetime import datetime, timedelta
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_std_n_ma(path,pairs,pairs_beta,formation_period_days = 365):
    std_dict = {}
    mean_dict = {}
    for p in pairs:
        beta = pairs_beta[p]
        asset_x = p[0]
        asset_y = p[1]

        x = pd.read_csv(path+asset_x, index_col = 0)
        y = pd.read_csv(path+asset_y, index_col = 0)
        df = pd.merge(x,y,left_index=True, right_index=True,how='inner')

        df.index = pd.to_datetime(df.index, utc = True)

        start_date = df.index.min()
        OneYear_formation = start_date + timedelta(days = formation_period_days)
        end_date_idx = df.index.get_indexer([OneYear_formation],method='nearest')[0]

        df = df.iloc[0:end_date_idx]

        spread = df['close_y'] - beta*df['close_x']

        std = spread.std()
        ma = spread.mean()

        std_dict[p]  = std
        mean_dict[p] = ma

    return std_dict,mean_dict

def plot_pair(path,pair, beta,mean,std):
    asset_x = pair[0]
    asset_y = pair[1]
    print(pair)

    x = pd.read_csv(path+asset_x, index_col = 0)
    y = pd.read_csv(path+asset_y, index_col = 0)
    df = pd.merge(x,y,left_index=True, right_index=True,how='inner')
    
    df['spread'] = df['close_y'] - beta*df['close_x']
    df['mean'] = mean
    df['+2sigma'] = mean + 2*std
    df['-2sigma'] = mean - 2*std
    df['+3sigma'] = mean + 3*std
    df['-3sigma'] = mean - 3*std
    # spread.plot()
    # plt.style.use('default')
    # sns.set_style("whitegrid")
    plt.plot(df.index, df['spread'], label = asset_y+' - b*'+asset_x)
    plt.plot(df.index, df['mean'],color = "blue",linestyle = "-")
    plt.plot(df.index, df['+2sigma'], color = "red",linestyle = "--",label = " 2sigma")
    plt.plot(df.index, df['-2sigma'], color = "red",linestyle = "--")
    plt.plot(df.index, df['+3sigma'], color = "red",linestyle = ":", label = '3sigma')
    plt.plot(df.index, df['-3sigma'], color = "red",linestyle = ":")

    # plt.grid(True)
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)
    plt.gca().set_facecolor('white')
    plt.show()




def get_hedge_ratio(path,pairs, method = 'ols'):
    pair_beta = {}
    for i in range(len(pairs)):
        asset_x = pairs[i][0]
        asset_y = pairs[i][1]

        x = pd.read_csv(path+asset_x, index_col = 0)
        y = pd.read_csv(path+asset_y, index_col = 0)
        df = pd.merge(x,y,left_index=True, right_index=True,how='inner')
        if method == 'ols':
            X = sm.add_constant(df['close_x'])

            lm = sm.OLS(df['close_y'],X).fit()
            hedge_ratio = lm.params.iloc[1]

        pair_beta[pairs[i]] = hedge_ratio

    return pair_beta



def find_coint_pairs(path,data_csv, pval_crit = 0.05,formation_period_days = 365,adj4day=False):
    n = len(data_csv)
    score_matrix = np.zeros((n,n))
    pval_matrix = np.zeros((n,n))
    pairs = []
    for i in range(len(data_csv)):
        x = pd.read_csv(path+data_csv[i], index_col = 0)
        if adj4day:
            print(x.index)
            # print(x['Date'])
            x['Date'] = pd.to_datetime(x.index,errors = 'coerce').date
            # x['Date'] = x.index.to_series().dt.date
            x = x.set_index('Date')
            
        
        for j in range(i+1,len(data_csv)):
            y = pd.read_csv(path+data_csv[j], index_col = 0)
            if adj4day:
                y['Date'] = pd.to_datetime(y.index).date
                y = y.set_index('Date')
            df = pd.merge(x,y,left_index=True, right_index=True,how='inner')
            df.index = pd.to_datetime(df.index, utc = True)
            # print(df)
            start_date = df.index.min()
            OneYear_formation = start_date + timedelta(days = formation_period_days)
            end_date_idx = df.index.get_indexer([OneYear_formation],method='nearest')[0]

            # print('coint test between: ', data_csv[i],' and ', data_csv[j])
            # print(df)
            try:
                coint_results = coint(df.iloc[0:end_date_idx]['close_x'],df.iloc[0:end_date_idx]['close_y'])
                
                s = coint_results[0]
                pval = coint_results[1]
                score_matrix[i,j] = s
                pval_matrix[i,j]  = pval

                

                if pval < pval_crit:
                    pairs.append((data_csv[i],data_csv[j]))
                    print('pval = ', pval, '(',data_csv[i],'/',data_csv[j],')')
                    print('--------------------------------------------------')
            except:
                print('error in',data_csv[i],data_csv[j])
            
           

    return score_matrix, pval_matrix, pairs



            

            
            

        
