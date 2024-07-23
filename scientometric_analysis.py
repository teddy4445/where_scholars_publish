import pandas as pd
import os
from consts import *
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import mannwhitneyu
from scipy.stats import kruskal
from scipy.stats import chi2_contingency

class Scientometrics:
    path = r'C:\Users\shira\OneDrive - Bar Ilan University\research\dblp'
    h_index_data_path = os.path.join(path, H_INDEX_CSV)
    func_data_path = os.path.join(path, FUNC_DATA_JSON)
    main_data_path = os.path.join(path, MAIN_DATA_CSV)
    journals_data_path = os.path.join(path, JOURNALS_CSV)
    conferences_data_path = os.path.join(path, CONFERENCES_CSV)
    journals_metrics_path = os.path.join(path, JOURNALS_METRICS_CSV)


    h_index_num_hv_path = os.path.join(path, H_INDEX_NUM_HV_CSV)
    h_index_num_papers_hv_type_ranks_path = os.path.join(path, H_INDEX_NUM_PAPERS_VENUE_TYPE_RANK_CSV)
    ranks_dist_path=os.path.join(path,RANKS_DIST_CSV)




    def __init__(self):

        '''
        with open(Scientometrics.func_data_path, "r") as func_data_file:
          self.func_data = json.load(func_data_file)
        self.df=pd.read_csv(Scientometrics.h_index_num_hv_path)
        #del self.df['id']
        self.df.dropna(inplace=True)
        self.df.drop(self.df[self.df['author name'].map(len) < 3].index, inplace=True)
        self.df.drop(self.df[self.df['h-index'] < 0].index, inplace=True)
        with open(Scientometrics.main_data_path, "r") as data_file:
            self.data = json.load(data_file)
        self.journals_data = pd.read_csv(Scientometrics.journals_data_path, keep_default_na=False)
        self.journals_data.loc[:, 'journal name'] = self.journals_data.loc[:, 'journal name'].str.lower()
        self.journals_data.loc[:, 'abbrv_name'] = self.journals_data.loc[:, 'abbrv_name'].str.lower()
        self.journals_data = self.journals_data.drop_duplicates()
        self.conf_data = pd.read_csv(Scientometrics.conferences_data_path, keep_default_na=False)
        self.conf_data.loc[:, 'conf name'] = self.conf_data.loc[:, 'conf name'].str.lower()
        self.conf_data.loc[:, 'abbrv_name1'] = self.conf_data.loc[:, 'abbrv_name1'].str.lower()
        self.conf_data.loc[:, 'abbrv_name2'] = self.conf_data.loc[:, 'abbrv_name2'].str.lower()
        self.conf_data = self.conf_data.drop_duplicates()
        self.journals_metrics_df = pd.read_csv(Scientometrics.journals_metrics_path, keep_default_na=False, delimiter=None)
        '''

        self.df = pd.read_csv(Scientometrics.h_index_num_papers_hv_type_ranks_path)
        # del self.df['id']
        self.df.dropna(inplace=True, how='all')
        self.df.drop(self.df[self.df['author name'].map(len) < 3].index, inplace=True)
        self.df.drop(self.df[self.df['h-index'] < 0].index, inplace=True)
        self.ranks_df=pd.read_csv(Scientometrics.ranks_dist_path)


    def match_h_index_to_num_hv(self):
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
        self.df.to_csv('./'+'authors_hindex_num_hv_with_IF.csv', index=False)


    def plot_h_index(self):
        # bins = [0, 0.35, 0.7, 1]
        df=self.df[self.df['h-index'] <=80]
        plt.hist(df['h-index'].values, bins=40, edgecolor="k")
        plt.xlabel("H Index")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def utest_h_index_vs_home_venues_2_groups(self):
        df = self.df[self.df['h-index'] <= 80]
        df.loc[df['num hv'] > 1, 'num hv'] = 2
        df1 = df.loc[df['num hv'] == 1, 'h-index']
        df2 = df.loc[df['num hv'] == 2, 'h-index']
        print('total num scholars with h-index- '+str(len(self.df)))
        print('num scholars h-index less than 100- '+str(len(df)))
        print('num scholars one hv- '+str(len(df1)))
        print('num scholars two or more hv- '+str(len(df2)))

        print('median')
        print('num hv 1- '+str(np.median(df1)))
        print('num hv 2 or more- '+str(np.median(df2)))
        print('mean')
        print('num hv 1- ' + str(np.mean(df1)))
        print('num hv 2 or more- ' + str(np.mean(df2)))

        u,p=mannwhitneyu(df1,df2)
        print('U-'+str(u))
        print('p-value - '+str(p))

    def utest_num_papers_vs_home_venues_2_groups(self):
        df = self.df.loc[self.df['num papers']<300]
        df.loc[df['num hv'] > 1, 'num hv'] = 2
        df1 = df.loc[df['num hv'] == 1, 'num papers']
        df2 = df.loc[df['num hv'] == 2, 'num papers']
        print('total num scholars with any number of papers- ' + str(len(self.df)))
        print('num scholars h-index less than 300- ' + str(len(df)))
        print('num scholars one hv- '+str(len(df1)))
        print('num scholars two or more hv- '+str(len(df2)))

        print('median')
        print('num hv 1- '+str(np.median(df1)))
        print('num hv 2 or more- '+str(np.median(df2)))
        print('mean')
        print('num hv 1- ' + str(np.mean(df1)))
        print('num hv 2 or more- ' + str(np.mean(df2)))

        u,p=mannwhitneyu(df1,df2)
        print('U-'+str(u))
        print('p-value - '+str(p))


    def plot_h_index_with_hv_2_groups(self,save_path):
        df = self.df.loc[self.df['h-index'] <= 80]
        df.loc[df['num hv'] > 1, 'num hv'] = 2
        df1 = df.loc[df['num hv'] == 1, 'h-index']
        df2 = df.loc[df['num hv'] == 2, 'h-index']

        # fig, axs = plt.subplots(1, 2, sharey=True)
        # m = 0

        # axs[0].hist(df1, alpha=0.5, label='One', bins=40, color='blue', density=True)
        # axs[0].set_title("One Home venue")
        # axs[1].hist(df2, alpha=0.5, label='Two or more', bins=40, color='green', density=True)
        # axs[1].set_title("Two or more Home Venues")

        # fig.suptitle('H-index Distribution by number of Home Venues')

        # fig.supxlabel('H-index')
        # fig.supylabel('Probability')

        ax = plt.subplot(111)
        plt.hist([df1, df2], bins=40, label=['One', 'Two or more'], color=['b','c'], density=True)
        # plt.hist(df1, alpha=0.5, label='One', bins=40, color='blue',density=True)
        # plt.hist(df2, alpha=0.5, label='Two or more', bins=40, color='green',density=True)
        # plt.yticks(fontsize=16)
        # plt.xticks(fontsize=16)
        plt.grid()
        ax.spines[['right', 'top']].set_visible(False)

        # plt.title('H index Distribution by number of Home Venues')
        plt.xlabel('H index')
        plt.ylabel('Probability')

        # add legend
        plt.legend(title='Num Home Venues')

        # plt.show()
        plt.savefig(save_path, dpi=300)


    def plot_num_papers_with_hv_2_groups(self,save_path):
        df = self.df.loc[self.df['num papers']<=150]
        df.loc[df['num hv'] > 1, 'num hv'] = 2
        df1 = df.loc[df['num hv'] == 1, 'num papers']
        df2 = df.loc[df['num hv'] == 2, 'num papers']

        # fig, axs = plt.subplots(1, 2, sharey=True)
        # m = 0
        #
        # axs[0].hist(df1, alpha=0.5, label='One', bins=40, color='blue',density=True)
        # axs[0].set_title("One Home venue")
        # axs[1].hist(df2, alpha=0.5, label='Two or more', bins=40, color='green',density=True)
        # axs[1].set_title("Two or more Home Venues")
        #
        # fig.suptitle('Num papers Distribution by number of Home Venues')

        # fig.supxlabel('Num papers')
        # fig.supylabel('Probability')

        ax = plt.subplot(111)
        plt.hist([df1, df2], bins=40, label=['One', 'Two or more'], color=['b','c'], density=True)
        # plt.hist(df1, alpha=0.5, label='One', bins=40, color='blue', density=True)
        # plt.hist(df2, alpha=0.5, label='Two or more', bins=40, color='green', density=True)
        plt.grid()
        ax.spines[['right', 'top']].set_visible(False)

        # plt.hist(df1, alpha=0.5, label='One', bins=40, color='blue',density=True)
        # plt.hist(df2, alpha=0.5, label='Two or more', bins=40, color='green',density=True)

        # plt.title('Num papers Distribution by number of Home Venues')
        plt.xlabel('Num papers')
        plt.ylabel('Probability')

        # add legend
        plt.legend(title='Num Home Venues')

        # plt.show()
        plt.savefig(save_path, dpi=300)


    def h_index_single_hv_dist_by_type(self):
        df = self.df.loc[self.df['h-index'] <= 80]
        print('num scholars h-index less than 80- ' + str(len(df)))

        df = df.loc[df['num hv'] == 1]

        df1= df.loc[df['num home journals']==1,'h-index']
        df2= df.loc[df['num home conferences']==1,'h-index']
        df3=df.loc[((df['num home journals']==0) & (df['num home conferences']==0)),'h-index']
        print('num scholars one home venue- ' + str(len(df)))
        print('num scholars one home journal- ' + str(len(df1)))
        print('mean, median H-index one home journal- '+str(np.mean(df1))+" "+str(np.median(df1)))
        print('num scholars one home conference- ' + str(len(df2)))
        print('mean, median H-index one home conference- '+str(np.mean(df2))+" "+str(np.median(df2)))
        print('num scholars one home other- ' + str(len(df3)))
        print('mean, median H-index one home other- '+str(np.mean(df3))+" "+str(np.median(df3)))



        kw, p = kruskal(df1, df2,df3)
        print('KW-' + str(kw))
        print('p-value - ' + str(p))

    def num_papers_single_hv_dist_by_type(self):
        df = self.df.loc[self.df['num papers'] <= 300]
        print('num scholars num papers less than 300- ' + str(len(df)))

        df = df.loc[df['num hv'] == 1]

        df1= df.loc[df['num home journals']==1,'num papers']
        df2= df.loc[df['num home conferences']==1,'num papers']
        df3=df.loc[((df['num home journals']==0) & (df['num home conferences']==0)),'num papers']
        print('num scholars one home venue- ' + str(len(df)))
        print('num scholars one home journal- ' + str(len(df1)))
        print('mean, median num papers one home journal -'+str(np.mean(df1))+" "+str(np.median(df1)))
        print('num scholars one home conference- ' + str(len(df2)))
        print('mean, median num papers one home conference- '+str(np.mean(df2))+" "+str(np.median(df2)))
        print('num scholars one home other- ' + str(len(df3)))
        print('mean, median num papers one home venue- '+str(np.mean(df3))+" "+str(np.median(df3)))


        kw, p = kruskal(df1, df2,df3)
        print('KW-' + str(kw))
        print('p-value - ' + str(p))

    def h_index_plot_single_hv_dist_by_type(self,save_path):
        df = self.df.loc[self.df['h-index'] <= 80]
        df = df.loc[df['num hv'] == 1]

        df1 = df.loc[df['num home journals'] == 1, 'h-index']
        df2 = df.loc[df['num home conferences'] == 1, 'h-index']
        df3 = df.loc[((df['num home journals'] == 0) & (df['num home conferences'] == 0)), 'h-index']

        # fig, axs = plt.subplots(1, 3, sharey=True)

        # axs[0].hist(df1, alpha=0.5, label='Journals', bins=40, color='blue', density=True)
        # axs[0].set_title("Journal")
        # axs[1].hist(df2, alpha=0.5, label='Conferences', bins=40, color='green', density=True)
        # axs[1].set_title("Conference")
        # axs[2].hist(df3, alpha=0.5, label='Other', bins=40, color='red', density=True)
        # axs[2].set_title("Other")

        # fig.suptitle('H-index Distribution by type of Home Venues- single venue')

        # plt.title('H index Distribution by number of Home Journals')
        # fig.supxlabel('H-index')
        # fig.supylabel('Probability')
        ax = plt.subplot(111)
        plt.hist([df1, df2,df3], bins=40, label=['Journals', 'Conferences','Other'], color=['b','c','g'], density=True)

        # plt.hist(df1, alpha=0.5, label='Journals', bins=40, color='blue', density=True)
        # plt.hist(df2, alpha=0.5, label='Conferences', bins=40, color='green', density=True)
        # plt.hist(df3, alpha=0.5, label='Other', bins=40, color='yellow', density=True)
        plt.grid()
        ax.spines[['right', 'top']].set_visible(False)

        plt.xlabel('H-index')
        plt.ylabel('Probability')

        plt.legend(title='Home venue type')

        # plt.show()
        plt.savefig(save_path, dpi=300)


    def num_papers_plot_single_hv_dist_by_type(self,save_path):
        df = self.df.loc[self.df['num papers'] <= 150]
        df = df.loc[df['num hv'] == 1]

        df1 = df.loc[df['num home journals'] == 1, 'num papers']
        df2 = df.loc[df['num home conferences'] == 1, 'num papers']
        df3 = df.loc[((df['num home journals'] == 0) & (df['num home conferences'] == 0)), 'num papers']

        # fig, axs = plt.subplots(1, 3, sharey=True)
        #
        # axs[0].hist(df1, alpha=0.5, label='Journals', bins=40, color='blue', density=True)
        # axs[0].set_title("Journal")
        # axs[1].hist(df2, alpha=0.5, label='Conferences', bins=40, color='green', density=True)
        # axs[1].set_title("Conference")
        # axs[2].hist(df3, alpha=0.5, label='Other', bins=40, color='red', density=True)
        # axs[2].set_title("Other")
        #
        # fig.suptitle('Num papers Distribution by type of Home Venues- single venue')

        # plt.title('H index Distribution by number of Home Journals')
        # fig.supxlabel('Num papers')
        # fig.supylabel('Probability')

        ax = plt.subplot(111)
        plt.hist([df1, df2,df3], bins=40, label=['Journals', 'Conferences','Other'], color=['b','c','g'], density=True)

        # plt.hist(df1, alpha=0.5, label='Journals', bins=40, color='blue', density=True)
        # plt.hist(df2, alpha=0.5, label='Conferences', bins=40, color='green', density=True)
        # plt.hist(df3, alpha=0.5, label='Other', bins=40, color='yellow', density=True)
        plt.grid()
        ax.spines[['right', 'top']].set_visible(False)

        plt.xlabel('Num papers')
        plt.ylabel('Probability')

        plt.legend(title='Home venue type')

        # plt.show()
        plt.savefig(save_path, dpi=300)



    def h_index_multi_hv_dist_by_type(self):
        df = self.df.loc[self.df['h-index'] <= 80]
        print('num scholars h-index less than 80- ' + str(len(df)))

        df = df.loc[df['num hv'] > 1]

        df1= df.loc[(df['num home journals']==df['num hv']) & (df['num home conferences']==0),'h-index']
        df2= df.loc[(df['num home conferences']==df['num hv']) & (df['num home journals']==0),'h-index']
        df3=df.loc[((df['num home journals']==0) & (df['num home conferences']==0)),'h-index']
        df4 = df[(df['num home journals']!=df['num hv'])]
        df4 = df4[(df4['num home conferences'] != df4['num hv'])]
        df4 = df4.loc[(df4['num home conferences'] !=0) | (df4['num home journals']!=0),'h-index' ]

        print('num scholars multiple home venue- ' + str(len(df)))
        print('num scholars multiple home journals- ' + str(len(df1)))
        print('mean, median H-index multiple home journal- '+str(np.mean(df1))+" "+str(np.median(df1)))
        print('num scholars multiple home conferences- ' + str(len(df2)))
        print('mean, median H-index multiple home conferences- '+str(np.mean(df2))+" "+str(np.median(df2)))
        print('num scholars multiple other home venues- ' + str(len(df3)))
        print('mean, median H-index multiple other home venues- '+str(np.mean(df3))+" "+str(np.median(df3)))
        print('num scholars multiple mixed home venues- ' + str(len(df4)))
        print('mean, median H-index multiple mixed home venues- '+str(np.mean(df4))+" "+str(np.median(df4)))



        kw, p = kruskal(df1, df2,df3,df4)
        print('KW-' + str(kw))
        print('p-value - ' + str(p))

    def num_papers_multi_hv_dist_by_type(self):
        df = self.df.loc[self.df['num papers'] <= 300]
        print('num scholars num papers less than 300- ' + str(len(df)))

        df = df.loc[df['num hv'] > 1]

        df1= df.loc[(df['num home journals']==df['num hv']) & (df['num home conferences']==0),'num papers']
        df2= df.loc[(df['num home conferences']==df['num hv']) & (df['num home journals']==0),'num papers']
        df3=df.loc[((df['num home journals']==0) & (df['num home conferences']==0)),'num papers']
        df4 = df[(df['num home journals']!=df['num hv'])]
        df4 = df4[(df4['num home conferences'] != df4['num hv'])]
        df4 = df4.loc[(df4['num home conferences'] !=0) | (df4['num home journals']!=0),'num papers' ]

        print('num scholars multiple home venue- ' + str(len(df)))
        print('num scholars multiple home journals- ' + str(len(df1)))
        print('mean, median num papers multiple home journals- '+str(np.mean(df1))+" "+str(np.median(df1)))
        print('num scholars multiple home conferences- ' + str(len(df2)))
        print('mean, median num papers multiple home conferences- '+str(np.mean(df2))+" "+str(np.median(df2)))
        print('num scholars multiple other home venues- ' + str(len(df3)))
        print('mean, median num papers multiple other home venues- '+str(np.mean(df3))+" "+str(np.median(df3)))
        print('num scholars multiple mixed home venues- ' + str(len(df4)))
        print('mean, median num papers multiple mixed home venues- '+str(np.mean(df4))+" "+str(np.median(df4)))



        kw, p = kruskal(df1, df2,df3,df4)
        print('KW-' + str(kw))
        print('p-value - ' + str(p))


    def plot_multi_hv_dist_by_type(self,save_path=None):
        df = self.df

        hj_df = df[(df['num home journals'] == df['num hv']) & (df['num home conferences'] == 0)]
        hc_df = df[(df['num home conferences'] == df['num hv']) & (df['num home journals'] == 0)]
        ho_df = df[((df['num home journals'] == 0) & (df['num home conferences'] == 0))]
        df4 = df[(df['num home journals'] != df['num hv'])]
        df4 = df4[(df4['num home conferences'] != df4['num hv'])]
        hm_df = df4[(df4['num home conferences'] != 0) | (df4['num home journals'] != 0)]
        journals=[]
        conferences = []
        other = []
        mixed = []

        journals.append(len(hj_df.loc[hj_df['num hv']==1]))
        conferences.append(len(hc_df.loc[hc_df['num hv']==1]))
        other.append(len(ho_df.loc[ho_df['num hv']==1]))
        mixed.append(len(hm_df.loc[hm_df['num hv'] == 1]))

        journals.append(len(hj_df.loc[hj_df['num hv'] == 2]))
        conferences.append(len(hc_df.loc[hc_df['num hv'] == 2]))
        other.append(len(ho_df.loc[ho_df['num hv'] == 2]))
        mixed.append(len(hm_df.loc[hm_df['num hv'] == 2]))

        journals.append(len(hj_df.loc[hj_df['num hv'] == 3]))
        conferences.append(len(hc_df.loc[hc_df['num hv'] == 3]))
        other.append(len(ho_df.loc[ho_df['num hv'] == 3]))
        mixed.append(len(hm_df.loc[hm_df['num hv'] == 3]))

        journals.append(len(hj_df.loc[hj_df['num hv'] == 4]))
        conferences.append(len(hc_df.loc[hc_df['num hv'] == 4]))
        other.append(len(ho_df.loc[ho_df['num hv'] == 4]))
        mixed.append(len(hm_df.loc[hm_df['num hv'] == 4]))

        ax = plt.subplot(111)
        j=np.array(journals)
        c=np.array(conferences)
        o=np.array(other)
        m=np.array(mixed)
        x=['1','2','3','4']
        plt.bar(x, j, color='b')
        plt.bar(x, c, bottom=j, color='g')
        plt.bar(x, o, bottom=j + c, color='r')
        plt.bar(x, m, bottom=j + c + other, color='m')
        plt.xlabel("Number of home venues")
        plt.ylabel("Number of scholars")
        plt.legend(["Journals", "Conferences", "Other", "Mixed"])
        plt.grid(axis='y')
        ax.spines[['right', 'top']].set_visible(False)

        # plt.title("Scores by Teams in 4 Rounds")

        # print('num scholars with home venue/s- ' + str(len(df)))
        # print('num scholars with only home journal/s- ' + str(len(hj_df)))
        # print('num scholars with only home conference/s- ' + str(len(hc_df)))
        # print('num scholars only other home venue/s- ' + str(len(ho_df)))
        # print('num scholars with mixed home venues- ' + str(len(hm_df)))

        # plt.plot([hj,hc,hw,hm])
        # plt.xticks(['Journals','Conferences','Other','Mixed'])
        # plt.show()
        plt.savefig(save_path, dpi=300)


    def h_index_plot_multi_hv_dist_by_type(self,save_path):
        df = self.df.loc[self.df['h-index'] <= 80]
        df = df.loc[df['num hv'] > 1]

        df1 = df.loc[(df['num home journals'] == df['num hv']) & (df['num home conferences'] == 0), 'h-index']
        df2 = df.loc[(df['num home conferences'] == df['num hv']) & (df['num home journals'] == 0), 'h-index']
        df3 = df.loc[((df['num home journals'] == 0) & (df['num home conferences'] == 0)), 'h-index']
        df4 = df[(df['num home journals'] != df['num hv'])]
        df4 = df4[(df4['num home conferences'] != df4['num hv'])]
        df4 = df4.loc[(df4['num home conferences'] != 0) | (df4['num home journals'] != 0), 'h-index']

        # fig, axs = plt.subplots(1, 4, sharey=True)
        #
        # axs[0].hist(df1, alpha=0.5, label='Journals', bins=40, color='blue', density=True)
        # axs[0].set_title("Journal")
        # axs[1].hist(df2, alpha=0.5, label='Conferences', bins=40, color='green', density=True)
        # axs[1].set_title("Conference")
        # axs[2].hist(df3, alpha=0.5, label='Other', bins=40, color='red', density=True)
        # axs[2].set_title("Other")
        # axs[3].hist(df4, alpha=0.5, label='Mixed', bins=40, color='purple', density=True)
        # axs[3].set_title("Mixed")
        #
        # fig.suptitle('H-index Distribution by type of Home Venues- multiple venues')

        # plt.title('H index Distribution by number of Home Journals')
        # fig.supxlabel('H-index')
        # fig.supylabel('Probability')
        ax = plt.subplot(111)
        plt.hist([df1, df2,df3,df4], bins=40, label=['Journals', 'Conferences','Other','Mixed'], color=['b','c','g','m'], density=True)
        # plt.hist(df1, alpha=0.5, label='Journals', bins=40, color='blue', density=True)
        # plt.hist(df2, alpha=0.5, label='Conferences', bins=40, color='green', density=True)
        # plt.hist(df3, alpha=0.5, label='Other', bins=40, color='yellow', density=True)
        # plt.hist(df4, alpha=0.5, label='Mixed', bins=40, color='red', density=True)

        plt.grid()
        ax.spines[['right', 'top']].set_visible(False)

        plt.xlabel('H-index')
        plt.ylabel('Probability')

        plt.legend(title='Home venue type')

        # plt.show()
        plt.savefig(save_path, dpi=300)


    def num_papers_plot_multi_hv_dist_by_type(self,save_path):
        df = self.df.loc[self.df['num papers'] <= 150]
        df = df.loc[df['num hv'] > 1]

        df1 = df.loc[(df['num home journals'] == df['num hv']) & (df['num home conferences'] == 0), 'num papers']
        df2 = df.loc[(df['num home conferences'] == df['num hv']) & (df['num home journals'] == 0), 'num papers']
        df3 = df.loc[((df['num home journals'] == 0) & (df['num home conferences'] == 0)), 'num papers']
        df4 = df[(df['num home journals'] != df['num hv'])]
        df4 = df4[(df4['num home conferences'] != df4['num hv'])]
        df4 = df4.loc[(df4['num home conferences'] != 0) | (df4['num home journals'] != 0), 'num papers']

        # fig, axs = plt.subplots(1, 4, sharey=True)

        # axs[0].hist(df1, alpha=0.5, label='Journals', bins=40, color='blue', density=True)
        # axs[0].set_title("Journal")
        # axs[1].hist(df2, alpha=0.5, label='Conferences', bins=40, color='green', density=True)
        # axs[1].set_title("Conference")
        # axs[2].hist(df3, alpha=0.5, label='Other', bins=40, color='red', density=True)
        # axs[2].set_title("Other")
        # axs[3].hist(df4, alpha=0.5, label='Mixed', bins=40, color='purple', density=True)
        # axs[3].set_title("Mixed")
        #
        # fig.suptitle('Num papers Distribution by type of Home Venues- multiple venues')

        # plt.title('H index Distribution by number of Home Journals')
        # fig.supxlabel('Num papers')
        # fig.supylabel('Probability')
        ax = plt.subplot(111)
        plt.hist([df1, df2,df3,df4], bins=40, label=['Journals', 'Conferences','Other','Mixed'], color=['b','c','g','m'], density=True)
        # plt.hist(df1, alpha=0.5, label='Journals', bins=40, color='blue', density=True)
        # plt.hist(df2, alpha=0.5, label='Conferences', bins=40, color='green', density=True)
        # plt.hist(df3, alpha=0.5, label='Other', bins=40, color='yellow', density=True)
        # plt.hist(df4, alpha=0.5, label='Mixed', bins=40, color='red', density=True)

        plt.grid()
        ax.spines[['right', 'top']].set_visible(False)

        plt.xlabel('Num papers')
        plt.ylabel('Probability')

        plt.legend(title='Home venue type')

        # plt.show()
        plt.savefig(save_path, dpi=300)


    def one_HJ_h_index_Q_value(self):
        df=self.df[self.df['h-index'] <=80]
        df = df.loc[df['num hv'] == 1]
        # df.replace(r'\[(.*?)\]', r'\1', regex=True, inplace=True)
        # df['jif_q_vals']=df.apply(lambda row: pd.Series)
        print('num scholars single home venue- ' + str(len(df)))
        df1 = df[df['num home journals'] == 1]
        print('num scholars single home journal- ' + str(len(df1)))
        count=df1['jif_q_vals'].isnull().sum()
        print('num scholars with no jif q rank- ' + str(count))
        df2= df1[df1['jif_q_vals'].notnull()]
        print('num scholars with jif q rank- ' + str(len(df2)))
        df_q1=pd.DataFrame(df2.loc[df2['jif_q_vals']=='1','h-index'].values, columns=['Q1'])
        print('num scholars with jif q rank 1- ' + str(len(df_q1)))
        df_q2 = pd.DataFrame(df2.loc[df2['jif_q_vals'] == '2','h-index'].values, columns=['Q2'])
        print('num scholars with jif q rank 2- ' + str(len(df_q2)))
        df_q3 = pd.DataFrame(df2.loc[df2['jif_q_vals'] == '3','h-index'].values, columns=['Q3'])
        print('num scholars with jif q rank 3- ' + str(len(df_q3)))
        df_q4 = pd.DataFrame(df2.loc[df2['jif_q_vals'] == '4','h-index'].values, columns=['Q4'])
        print('num scholars with jif q rank 4- ' + str(len(df_q4)))
        new_df= pd.concat([df_q1,df_q2, df_q3, df_q4], axis=1)
        new_df.to_csv('One_HJ_h_index_by_jifq.csv', index=False)

    def plot_one_HJ_h_index_q_value(self,save_path):
            df = self.df[self.df['h-index'] <= 80]
            df = df.loc[df['num hv'] == 1]
            # df.replace(r'\[(.*?)\]', r'\1', regex=True, inplace=True)
            # df['jif_q_vals']=df.apply(lambda row: pd.Series)
            df1 = df[df['num home journals'] == 1]
            count = df1['jif_q_vals'].isnull().sum()
            df2 = df1[df1['jif_q_vals'].notnull()]
            df2['jif_q_vals']=pd.to_numeric(df2['jif_q_vals'])

            fig, ax = plt.subplots()
            boxplot = sns.boxplot(x='jif_q_vals', y='h-index',  data=df2, hue='jif_q_vals', palette=['b','c','g','m'], showfliers=False, showmeans=True,
                                  native_scale=True, ax=ax)
            boxplot.set(xticks=[1,2,3,4],xlabel='Q ranks',ylabel='H-index')
            # ax.set_title("H-index distribution by quantile ranking, single home journal")

            # plt.show()

            plt.savefig(save_path, dpi=300)



    def one_HJ_num_papers_Q_value(self):
        df=self.df[self.df['num papers'] <=300]
        df = df.loc[df['num hv'] == 1]
        # df.replace(r'\[(.*?)\]', r'\1', regex=True, inplace=True)
        # df['jif_q_vals']=df.apply(lambda row: pd.Series)
        print('num scholars single home venue- ' + str(len(df)))
        df1 = df[df['num home journals'] == 1]
        print('num scholars single home journal- ' + str(len(df1)))
        count=df1['jif_q_vals'].isnull().sum()
        print('num scholars with no jif q rank- ' + str(count))
        df2= df1[df1['jif_q_vals'].notnull()]
        print('num scholars with jif q rank- ' + str(len(df2)))
        df_q1=pd.DataFrame(df2.loc[df2['jif_q_vals']=='1','num papers'].values, columns=['Q1'])
        print('num scholars with jif q rank 1- ' + str(len(df_q1)))
        df_q2 = pd.DataFrame(df2.loc[df2['jif_q_vals'] == '2','num papers'].values, columns=['Q2'])
        print('num scholars with jif q rank 2- ' + str(len(df_q2)))
        df_q3 = pd.DataFrame(df2.loc[df2['jif_q_vals'] == '3','num papers'].values, columns=['Q3'])
        print('num scholars with jif q rank 3- ' + str(len(df_q3)))
        df_q4 = pd.DataFrame(df2.loc[df2['jif_q_vals'] == '4','num papers'].values, columns=['Q4'])
        print('num scholars with jif q rank 4- ' + str(len(df_q4)))
        new_df= pd.concat([df_q1,df_q2, df_q3, df_q4], axis=1)
        new_df.to_csv('One_HJ_num_papers_by_jifq.csv', index=False)

    def plot_one_HJ_num_papers_q_value(self,save_path):
        df = self.df[self.df['num papers'] <= 150]
        df = df.loc[df['num hv'] == 1]
        # df.replace(r'\[(.*?)\]', r'\1', regex=True, inplace=True)
        # df['jif_q_vals']=df.apply(lambda row: pd.Series)
        df1 = df[df['num home journals'] == 1]
        count = df1['jif_q_vals'].isnull().sum()
        df2 = df1[df1['jif_q_vals'].notnull()]
        df2['jif_q_vals'] = pd.to_numeric(df2['jif_q_vals'])

        boxplot = sns.boxplot(x='jif_q_vals', y='num papers', data=df2, hue='jif_q_vals', palette=['b','c','g','m'], showfliers=False,
                         showmeans=True, native_scale=True,
                         )
        boxplot.set(xticks=[1, 2, 3, 4], xlabel='Q ranks', ylabel='Num papers')
        # ax.set_title("Number of papers distribution by quantile ranking, single home journal")

        # plt.show()
        boxplot.get_figure().savefig(save_path, dpi=300)

    def multi_HJ_h_index_Q_value(self):
        df = self.df[self.df['h-index'] <= 80]
        df = df.loc[df['num hv'] > 1]
        # df.replace(r'\[(.*?)\]', r'\1', regex=True, inplace=True)
        # df['jif_q_vals']=df.apply(lambda row: pd.Series)
        print('num scholars multi home venue- ' + str(len(df)))
        df1 = df[df['num home journals'] > 1]
        print('num scholars multi home journal- ' + str(len(df1)))
        count = df1['jif_q_vals'].isnull().sum()
        print('num scholars with no jif q rank- ' + str(count))
        df2 = df1[df1['jif_q_vals'].notnull()]
        print('num scholars with jif q rank- ' + str(len(df2)))
        df_q1 = pd.DataFrame(df2.loc[df2['jif_q_vals'].str.startswith('1'), 'h-index'].values, columns=['Q1'])
        print('num scholars with jif q rank 1- ' + str(len(df_q1)))
        df_q2 = pd.DataFrame(df2.loc[df2['jif_q_vals'].str.startswith('2'), 'h-index'].values, columns=['Q2'])
        print('num scholars with jif q rank 2- ' + str(len(df_q2)))
        df_q3 = pd.DataFrame(df2.loc[df2['jif_q_vals'].str.startswith('3'), 'h-index'].values, columns=['Q3'])
        print('num scholars with jif q rank 3- ' + str(len(df_q3)))
        df_q4 = pd.DataFrame(df2.loc[df2['jif_q_vals'].str.startswith('4'), 'h-index'].values, columns=['Q4'])
        print('num scholars with jif q rank 4- ' + str(len(df_q4)))
        new_df = pd.concat([df_q1, df_q2, df_q3, df_q4], axis=1)
        new_df.to_csv('Multi_HJ_h_index_by_jifq.csv', index=False)

    def plot_multi_HJ_h_index_q_value(self,save_path):
            df = self.df[self.df['h-index'] <= 80]
            df = df.loc[df['num hv'] > 1]
            df1 = df[df['num home journals'] > 1]
            count = df1['jif_q_vals'].isnull().sum()
            df2 = df1[df1['jif_q_vals'].notnull()]
            # df2['jif_q_vals']=pd.to_numeric(df2['jif_q_vals'])
            df2['first_jif_q_vals']=0
            df2.loc[df2['jif_q_vals'].str.startswith('1'), 'first_jif_q_vals']=1
            df2.loc[df2['jif_q_vals'].str.startswith('2'), 'first_jif_q_vals']=2
            df2.loc[df2['jif_q_vals'].str.startswith('3'), 'first_jif_q_vals'] = 3
            df2.loc[df2['jif_q_vals'].str.startswith('4'), 'first_jif_q_vals'] = 4

            boxplot = sns.boxplot(x='first_jif_q_vals', y='h-index',  data=df2, hue='first_jif_q_vals', palette=['b','c','g','m'], showfliers=False, showmeans=True,native_scale=True,
                             )
            boxplot.set(xticks=[1,2,3,4],xlabel='Q ranks',ylabel='H-index')
            # ax.set_title("H-index distribution by quantile ranking, multiple home journals")

            plt.show()
            boxplot.get_figure().savefig(save_path, dpi=300)



    def multi_HJ_num_papers_Q_value(self):
        df = self.df[self.df['num papers'] <= 300]
        df = df.loc[df['num hv'] > 1]
        # df.replace(r'\[(.*?)\]', r'\1', regex=True, inplace=True)
        # df['jif_q_vals']=df.apply(lambda row: pd.Series)
        print('num scholars multi home venue- ' + str(len(df)))
        df1 = df[df['num home journals'] > 1]
        print('num scholars multi home journal- ' + str(len(df1)))
        count = df1['jif_q_vals'].isnull().sum()
        print('num scholars with no jif q rank- ' + str(count))
        df2 = df1[df1['jif_q_vals'].notnull()]
        print('num scholars with jif q rank- ' + str(len(df2)))
        df_q1 = pd.DataFrame(df2.loc[df2['jif_q_vals'].str.startswith('1'), 'num papers'].values, columns=['Q1'])
        print('num scholars with jif q rank 1- ' + str(len(df_q1)))
        df_q2 = pd.DataFrame(df2.loc[df2['jif_q_vals'].str.startswith('2'), 'num papers'].values, columns=['Q2'])
        print('num scholars with jif q rank 2- ' + str(len(df_q2)))
        df_q3 = pd.DataFrame(df2.loc[df2['jif_q_vals'].str.startswith('3'), 'num papers'].values, columns=['Q3'])
        print('num scholars with jif q rank 3- ' + str(len(df_q3)))
        df_q4 = pd.DataFrame(df2.loc[df2['jif_q_vals'].str.startswith('4'), 'num papers'].values, columns=['Q4'])
        print('num scholars with jif q rank 4- ' + str(len(df_q4)))
        new_df = pd.concat([df_q1, df_q2, df_q3, df_q4], axis=1)
        new_df.to_csv('Multi_HJ_num_papers_by_jifq.csv', index=False)

    def plot_multi_HJ_num_papers_q_value(self,save_path):
        df = self.df[self.df['h-index'] <= 150]
        df = df.loc[df['num hv'] > 1]
        df1 = df[df['num home journals'] > 1]
        count = df1['jif_q_vals'].isnull().sum()
        df2 = df1[df1['jif_q_vals'].notnull()]
        # df2['jif_q_vals']=pd.to_numeric(df2['jif_q_vals'])
        df2['first_jif_q_vals'] = 0
        df2.loc[df2['jif_q_vals'].str.startswith('1'), 'first_jif_q_vals'] = 1
        df2.loc[df2['jif_q_vals'].str.startswith('2'), 'first_jif_q_vals'] = 2
        df2.loc[df2['jif_q_vals'].str.startswith('3'), 'first_jif_q_vals'] = 3
        df2.loc[df2['jif_q_vals'].str.startswith('4'), 'first_jif_q_vals'] = 4

        boxplot = sns.boxplot(x='first_jif_q_vals', y='num papers', data=df2, hue='first_jif_q_vals', palette=['b','c','g','m'],
                         showfliers=False, showmeans=True, native_scale=True,
                         )
        boxplot.set(xticks=[1, 2, 3, 4], xlabel='Q ranks', ylabel='Num papers')
        # ax.set_title("Number of papers distribution by quantile ranking, multiple home journals")

        plt.show()
        boxplot.get_figure().savefig(save_path, dpi=300)

    def chi_square_ranks_dist(self):
        df1=self.ranks_df[['Number of Journals','Number of Scholars with Single HJ']]
        stat, p, dof, expected = chi2_contingency(df1)
        print("chi square test for num journals and num scholars with single journal p-{}, stat {} ".format(p,stat))
        df1 = self.ranks_df[['Number of Scholars with Single HJ', 'Number of Scholars with Multiple HJs']]
        stat, p, dof, expected = chi2_contingency(df1)
        print("chi square test for num scholars with single journal and num scholars with multi home journals p-{}, stat {} ".format(p, stat))
        df1 = self.ranks_df[['Number of Scholars with Multiple HJs','Number of Journals']]
        stat, p, dof, expected = chi2_contingency(df1)
        print(
            "chi square test for num scholars with multi home journals and num journals p-{}, stat {} ".format(
                p, stat))

    def basic_stats(self):
        mean_h_index=np.mean(self.df['h-index'])
        median_h_index = np.median(self.df['h-index'])
        std_h_index = np.std(self.df['h-index'])
        mean_num_papers = np.mean(self.df['num papers'])
        median_num_papers = np.median(self.df['num papers'])
        std_num_papers = np.std(self.df['num papers'])
        print('mean h-index-{}'.format(mean_h_index))
        print('median h-index-{}'.format(median_h_index))
        print('std h-index-{}'.format(std_h_index))
        print('mean num papers-{}'.format(mean_num_papers))
        print('median num papers-{}'.format(median_num_papers))
        print('std num papers-{}'.format(std_num_papers))

    # add code here

    def plot_h_index_with_hv(self,save_path):
        df=self.df[self.df['h-index'] <=80]
        df.loc[df['num hj']>4, 'num hj']=4
        df1=df.loc[df['num hj']==1,'h-index']
        df2 = df.loc[df['num hj'] == 2, 'h-index']
        df3 = df.loc[df['num hj'] == 3, 'h-index']
        df4 = df.loc[df['num hj'] == 4, 'h-index']

        fig, axs = plt.subplots(2, 2)
        m = 0

        axs[0,0].hist(df1, alpha=0.5, label='One', bins=40, density=True)
        axs[0,0].set_title("One Home venue")
        axs[0,1].hist(df2, alpha=0.5, label='Two', bins=40, density=True)
        axs[0,1].set_title("Two Home Venues")

        axs[1,0].hist(df3, alpha=0.5, label='Three', bins=40, density=True)
        axs[1,0].set_title("Three Home Venues")

        axs[1,1].hist(df4, alpha=0.5, label='Four or more', bins=40, density=True)
        axs[1,1].set_title("Four or more Home Venues")


        fig.suptitle('H index Distribution by number of Home Journals')

        # plt.title('H index Distribution by number of Home Journals')
        fig.supxlabel('H index')
        fig.supylabel('Probability')

        # add legend
        #fig.legend(title='Num Home Journals')

        plt.show()
        # num_hjs = df['num hj'].unique().tolist()
        # heatmap_data=df[['h-index', 'num hj']]
        # sns.heatmap(heatmap_data, columns=num_hjs,  annot=True)
        # plt.show()
        plt.savefig(save_path, dpi=300)


    def match_h_index_to_type_hj_with_IF(self):
        count=0
        self.df['num home journals'] = 0
        self.df['num home conferences'] = 0
        journals_abbrv = set(self.journals_data['abbrv_name'])
        journals_full_name = set(self.journals_data['journal name'])
        conf_abbrv1 = set(self.conf_data['abbrv_name1'])
        conf_abbrv2 = set(self.conf_data['abbrv_name2'])
        conf_full_name = set(self.conf_data['conf name'])

        venues=set()
        for name, picked_author_dict in self.func_data.items():
            home_venues=0
            jif_q_vals=[]
            sjr_q_vals=[]
            # filter authors with not enough data
            if picked_author_dict['func'] != 'exp' and picked_author_dict['func'] != 'inv':
                continue
            if len(self.df.loc[self.df['author name'] == name] == 1):
                print("author - {}".format(name))
                count+=1
                if count==5000:
                    print("count {}".format(count))
                    self.df.to_csv('./' + 'authors_hindex_type_hv_with_metrics.csv', index=False)
                num_home_venues = picked_author_dict['hj']
                author_venues = self.data[name]
                for venue, num_papers in sorted(author_venues.items(), key=lambda item: item[1], reverse=True):
                    if num_home_venues==home_venues:
                        break
                    if venue == 'corr':
                            continue
                    home_venues+=1
                    if venue in journals_abbrv :
                        print(venue)
                        self.df.loc[self.df['author name'] == name, 'num home journals'] += 1
                        sjr_q=self.journals_metrics_df.loc[self.journals_metrics_df['abbrv_name'] == venue,'SJR Q']
                        if len(sjr_q==1) and len(sjr_q.values[0])>0:
                            sjr=int((sjr_q.values[0])[1])
                            sjr_q_vals.append(sjr)
                            self.df.loc[self.df['author name'] == name, 'sjr_q_vals'] = str(sjr_q_vals)
                        jif_q=self.journals_metrics_df.loc[self.journals_metrics_df['abbrv_name'] == venue,'JIF Quartile']
                        if len(jif_q == 1) and len(jif_q.values[0])>0:
                            jif = int((jif_q.values[0])[1])
                            jif_q_vals.append(jif)
                            self.df.loc[self.df['author name'] == name, 'jif_q_vals'] = str(jif_q_vals)
                    elif venue in journals_full_name:
                        print(venue)
                        self.df.loc[self.df['author name'] == name, 'num home journals'] += 1
                        sjr_q = self.journals_metrics_df.loc[self.journals_metrics_df['Journal name'] == venue, 'SJR Q']
                        if len(sjr_q == 1) and len(sjr_q.values[0])>0:
                            sjr = int((sjr_q.values[0])[1])
                            sjr_q_vals.append(sjr)
                            self.df.loc[self.df['author name'] == name, 'sjr_q_vals'] = str(sjr_q_vals)
                        jif_q = self.journals_metrics_df.loc[self.journals_metrics_df['Journal name'] == venue, 'JIF Quartile']
                        if len(jif_q == 1) and len(jif_q.values[0])>0:
                            jif = int((jif_q.values[0])[1])
                            jif_q_vals.append(jif)
                            self.df.loc[self.df['author name'] == name, 'jif_q_vals'] = str(jif_q_vals)


                    elif venue in conf_abbrv1 or venue in conf_abbrv2 or venue in conf_full_name:
                        # print(venue)
                        self.df.loc[self.df['author name'] == name, 'num home conferences'] += 1
        print(self.df.head())
        self.df.to_csv('./' + 'authors_hindex_type_hv_with_metrics.csv', index=False)

    def match_h_index_to_type_non_hj_with_IF(self):
        count = 0
        self.df['num non home journals'] = 0
        self.df['num non home conferences'] = 0
        journals_abbrv = set(self.journals_data['abbrv_name'])
        journals_full_name = set(self.journals_data['journal name'])
        conf_abbrv1 = set(self.conf_data['abbrv_name1'])
        conf_abbrv2 = set(self.conf_data['abbrv_name2'])
        conf_full_name = set(self.conf_data['conf name'])

        for name, picked_author_dict in self.func_data.items():
            num_venues = 0
            jif_q_vals = []
            sjr_q_vals = []
            # filter authors with not enough data
            if picked_author_dict['func'] != 'exp' and picked_author_dict['func'] != 'inv':
                continue
            if len(self.df.loc[self.df['author name'] == name] == 1):
                print("author - {}".format(name))
                count += 1
                if count == 50:
                    print("count {}".format(count))
                    self.df.to_csv('./' + 'authors_hindex_type_non_hv_with_metrics.csv', index=False)
                num_home_venues = picked_author_dict['hj']
                author_venues = self.data[name]
                for venue, num_papers in sorted(author_venues.items(), key=lambda item: item[1], reverse=True):
                    num_venues += 1
                    if num_home_venues >= num_venues:
                        continue
                    if venue == 'corr':
                        continue

                    if venue in journals_abbrv:
                        print(venue)
                        self.df.loc[self.df['author name'] == name, 'num non home journals'] += 1
                        sjr_q = self.journals_metrics_df.loc[self.journals_metrics_df['abbrv_name'] == venue, 'SJR Q']
                        if len(sjr_q == 1) and len(sjr_q.values[0]) > 0:
                            sjr = int((sjr_q.values[0])[1])
                            sjr_q_vals.append(sjr)
                            self.df.loc[self.df['author name'] == name, 'non home sjr_q_vals'] = str(sjr_q_vals)
                        jif_q = self.journals_metrics_df.loc[
                            self.journals_metrics_df['abbrv_name'] == venue, 'JIF Quartile']
                        if len(jif_q == 1) and len(jif_q.values[0]) > 0:
                            jif = int((jif_q.values[0])[1])
                            jif_q_vals.append(jif)
                            self.df.loc[self.df['author name'] == name, 'non home jif_q_vals'] = str(jif_q_vals)
                    elif venue in journals_full_name:
                        print(venue)
                        self.df.loc[self.df['author name'] == name, 'num non home journals'] += 1
                        sjr_q = self.journals_metrics_df.loc[self.journals_metrics_df['Journal name'] == venue, 'SJR Q']
                        if len(sjr_q == 1) and len(sjr_q.values[0]) > 0:
                            sjr = int((sjr_q.values[0])[1])
                            sjr_q_vals.append(sjr)
                            self.df.loc[self.df['author name'] == name, 'non home sjr_q_vals'] = str(sjr_q_vals)
                        jif_q = self.journals_metrics_df.loc[
                            self.journals_metrics_df['Journal name'] == venue, 'JIF Quartile']
                        if len(jif_q == 1) and len(jif_q.values[0]) > 0:
                            jif = int((jif_q.values[0])[1])
                            jif_q_vals.append(jif)
                            self.df.loc[self.df['author name'] == name, 'non home jif_q_vals'] = str(jif_q_vals)


                    elif venue in conf_abbrv1 or venue in conf_abbrv2 or venue in conf_full_name:
                        # print(venue)
                        self.df.loc[self.df['author name'] == name, 'num non home conferences'] += 1
        print(self.df.head())
        self.df.to_csv('./' + 'authors_hindex_type_non_hv_with_metrics.csv', index=False)

    def plot_h_index_with_hv_type(self,save_path):
        df=self.df[self.df['h-index'] <=80]
        df.loc[df['num hj']>4, 'num hj']=4
        journals=df.loc[df['num home journals']>0,['h-index']]
        conf = df.loc[df['num home conferences'] > 0, ['h-index']]

        fig, axs = plt.subplots(1, 2)
        m = 0

        axs[0].hist(journals, alpha=0.5, bins=40, density=True)
        axs[0].set_title("Journals")
        axs[1].hist(conf, alpha=0.5, bins=40, density=True)
        axs[1].set_title("Conferences")


        fig.suptitle('H index Distributation in respect to Home Venue type')

        # plt.title('H index Distribution by number of Home Journals')
        fig.supxlabel('H index')
        fig.supylabel('Probability')

        # add legend
        #fig.legend(title='Num Home Journals')

        plt.show()
        # num_hjs = df['num hj'].unique().tolist()
        # heatmap_data=df[['h-index', 'num hj']]
        # sns.heatmap(heatmap_data, columns=num_hjs,  annot=True)
        # plt.show()
        plt.savefig(save_path, dpi=300)





if __name__ == '__main__':
    sci=Scientometrics()
    # sci.basic_stats()
    sci.plot_multi_hv_dist_by_type(save_path=os.path.join(sci.path,"vis/home_venues_dist.pdf"))
    # sci.match_h_index_to_num_hv()
    # sci.plot_h_index()
    # sci.plot_h_index_with_hv()
    #sci.match_h_index_to_type_hj_with_IF()
    # sci.plot_h_index_with_hv_type()
    #sci.match_h_index_to_type_non_hj_with_IF()
    # sci.plot_h_index_with_hv_2_groups(save_path=os.path.join(sci.path,"vis/h index by num HV 2 groups histogram.pdf"))
    # sci.utest_h_index_vs_home_venues_2_groups()
    # sci.plot_num_papers_with_hv_2_groups(save_path=os.path.join(sci.path,"vis/num papers by num HV 2 groups histogram.pdf"))
    # sci.utest_num_papers_vs_home_venues_2_groups()
    # sci.h_index_single_hv_dist_by_type()
    # sci.h_index_plot_single_hv_dist_by_type(save_path=os.path.join(sci.path,"vis/h index by HV type single HV.pdf"))
    # sci.num_papers_single_hv_dist_by_type()
    # sci.num_papers_plot_single_hv_dist_by_type(save_path=os.path.join(sci.path,"vis/num papers by HV type single HV.pdf"))
    # sci.h_index_multi_hv_dist_by_type()
    # sci.h_index_plot_multi_hv_dist_by_type(save_path=os.path.join(sci.path,"vis/h index by HV type multi HV.pdf"))
    # sci.num_papers_multi_hv_dist_by_type()
    # sci.num_papers_plot_multi_hv_dist_by_type(save_path=os.path.join(sci.path,"vis/num papers by HV type multi HV.pdf"))
    # sci.one_HJ_h_index_Q_value()
    # sci.plot_one_HJ_h_index_q_value(save_path=os.path.join('.',"h index by Q rank single HJ boxplots.pdf"))
    # sci.one_HJ_num_papers_Q_value()
    # sci.plot_one_HJ_num_papers_q_value(save_path=os.path.join('.',"num papers by Q rank single HJ boxplots.pdf"))
    # sci.multi_HJ_h_index_Q_value()
    # sci.plot_multi_HJ_h_index_q_value(save_path=os.path.join('.',"h index by Q rank multi HJ boxplots.pdf"))
    # sci.multi_HJ_num_papers_Q_value()
    # sci.plot_multi_HJ_num_papers_q_value(save_path=os.path.join('.',"num papers by Q rank multi HJ boxplots.pdf"))
    # sci.chi_square_ranks_dist()