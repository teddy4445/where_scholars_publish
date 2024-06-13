import pandas as pd
import os
from consts import *
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Scientometrics:
    path = r'C:\Users\shira\OneDrive - Bar Ilan University\research\dblp'
    h_index_data_path = os.path.join(path, H_INDEX_CSV)
    func_data_path = os.path.join(path, FUNC_DATA_JSON)
    h_index_num_hj_path = os.path.join(path, H_INDEX_NUM_HJ_CSV)



    def __init__(self):
        with open(Scientometrics.func_data_path, "r") as func_data_file:
            self.func_data = json.load(func_data_file)
        self.df=pd.read_csv(Scientometrics.h_index_num_hj_path)
        #del self.df['id']
        self.df.dropna(inplace=True)
        self.df.drop(self.df[self.df['author name'].map(len) < 3].index, inplace=True)
        self.df.drop(self.df[self.df['h-index'] < 0].index, inplace=True)

    def match_h_index_to_num_hj(self):
        self.df['num hj']=0
        home_journals_dist = dict()
        for name, picked_author_dict in self.func_data.items():

            # filter authors with not enough data
            if picked_author_dict['func'] != 'exp' and picked_author_dict['func'] != 'inv':
                continue
            if len(self.df.loc[self.df['author name'] == name]==1):
                num_home_journals = picked_author_dict['hj']
                self.df.loc[self.df['author name']==name,'num hj']=num_home_journals
            # h_index = self.df.loc[self.df['author name']==name,'h-index'].values[0]
        print(self.df.head())
        self.df.to_csv('./'+'authors_hindex_num_hj.csv', index=False)

    def plot_h_index(self):
        # bins = [0, 0.35, 0.7, 1]
        df=self.df[self.df['h-index'] <=80]
        plt.hist(df['h-index'].values, bins=40, edgecolor="k")
        plt.xlabel("H Index")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def plot_h_index_with_hj(self):
        df=self.df[self.df['h-index'] <=80]
        df.loc[df['num hj']>4, 'num hj']=4
        df1=df.loc[df['num hj']==1,'h-index']
        df2 = df.loc[df['num hj'] == 2, 'h-index']
        df3 = df.loc[df['num hj'] == 3, 'h-index']
        df4 = df.loc[df['num hj'] == 4, 'h-index']

        plt.hist(df1, alpha=0.5, label='One', bins=40)
        plt.hist(df2, alpha=0.5, label='Two', bins=40)
        plt.hist(df3, alpha=0.5, label='Three', bins=40)
        plt.hist(df4, alpha=0.5, label='Four or more', bins=40)

        plt.title('H index Distribution by number of Home Journals')
        plt.xlabel('H index')
        plt.ylabel('Frequency')

        # add legend
        plt.legend(title='Num Home Journals')

        plt.show()
        # num_hjs = df['num hj'].unique().tolist()
        # heatmap_data=df[['h-index', 'num hj']]
        # sns.heatmap(heatmap_data, columns=num_hjs,  annot=True)
        # plt.show()



if __name__ == '__main__':
    sci=Scientometrics()
    # sci.match_h_index_to_num_hj()
    #sci.plot_h_index()
    sci.plot_h_index_with_hj()