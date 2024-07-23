# library imports
import math
import os
import json
import time
import pandas as pd

# project imports
from consts import *
import pickle
import csv
from plotter import Plotter
from data_analytical_fit import DataAnalyticalFit
from research_type_profiler import ResearchTypeProfiler
import main as Main
from plotter import Plotter



class DBLP_venues:
    path=r'C:\Users\shira\OneDrive - Bar Ilan University\research\dblp'
    func_data_path = os.path.join(path, FUNC_DATA_JSON)
    main_data_path = os.path.join(path, MAIN_DATA_CSV)
    journals_data_path = os.path.join(path, JOURNALS_CSV)
    conferences_data_path=os.path.join(path,CONFERENCES_CSV)

    """
    A class responsible to perform different analysis on the data
    """

    # CONSTS #

    # END - CONSTS #

    def __init__(self):
        with open(DBLP_venues.main_data_path, "r") as data_file:
            self.data = json.load(data_file)
        with open(DBLP_venues.func_data_path, "r") as func_data_file:
            self.func_data = json.load(func_data_file)
        self.journals_data=pd.read_csv(DBLP_venues.journals_data_path,keep_default_na=False)
        self.journals_data.loc[:, 'journal name'] = self.journals_data.loc[:, 'journal name'].str.lower()
        self.journals_data.loc[:, 'abbrv_name'] = self.journals_data.loc[:, 'abbrv_name'].str.lower()
        self.journals_data=self.journals_data.drop_duplicates()
        self.conf_data=pd.read_csv(DBLP_venues.conferences_data_path, keep_default_na=False)
        self.conf_data.loc[:, 'conf name'] = self.conf_data.loc[:, 'conf name'].str.lower()
        self.conf_data.loc[:, 'abbrv_name1'] = self.conf_data.loc[:, 'abbrv_name1'].str.lower()
        self.conf_data.loc[:, 'abbrv_name2'] = self.conf_data.loc[:, 'abbrv_name2'].str.lower()
        self.conf_data=self.conf_data.drop_duplicates()





    def author_journals_pareto(self,
                        sample_rate: int = 1,
                        print_rate: int = 50):
        """
        An author-venue type data for the entire dataset
        """
        answer = {}

        index = 0
        count_authors=0
        count_authors_with_journals=0
        count_authors_with_corr=0
        journals_abbrv=set(self.journals_data['abbrv_name'])
        journals_full_name=set(self.journals_data['journal name'])

        func_data_length = len(self.func_data)
        all_authors=len(self.data)
        start_time = time.time()
        venues=set()
        journals=set()
        for name, picked_author_dict in self.func_data.items():
            index += 1
            # if (index % print_rate) == 0:
            #     print("Analyzer.identify venue type: Working on line {}/{} ({:.3f}%) in {:.2f} seconds".format(
            #     index,
            #         func_data_length,
            #         100 * index / func_data_length,
            #         time.time() - start_time))

            # filter authors with not enough data
            if picked_author_dict['func'] != 'exp' and picked_author_dict['func']!='inv':
                continue
            num_home_journals=picked_author_dict['hj']
            author_venues= self.data[name]

            count_authors+=1
            home_venues=0
            found=False
            for venue,num_papers in author_venues.items():
                venues.add(venue)
                if (num_home_journals == 1):
                    if venue=='corr':
                        count_authors_with_corr += 1
                        break
                home_venues+=1
                if venue in journals_abbrv:
                    print(venue)
                    journals.add(venue)
                    found=True
                if home_venues==num_home_journals:
                    break
            if found:
                count_authors_with_journals+=1
                print('found for ', name)
            else:
                home_venues=0
                for venue, num_papers in author_venues.items():
                    home_venues += 1
                    if venue in journals_full_name:
                        journals.add(venue)
                        found = True
                    if home_venues == num_home_journals:
                        break
                if found:
                    count_authors_with_journals+=1
                    print('found for ', name)
        print('')
        print('')
        print('num authors with journals as home venues ',count_authors_with_journals)
        print('num authors with pareto dist ',count_authors)
        print('total num authors with a dist func including error',func_data_length)
        print('total num authors ',all_authors)
        print('num authors with corr as home venues',count_authors_with_corr)
        print('total num venues',len(venues))
        print('total num journals', len(self.journals_data))
        print('num home journals of authors with pareto dist',len(journals))
        self.journals_data['found']=False
        for journal in journals:
            if journal in self.journals_data['abbrv_name'].values:
                self.journals_data.loc[self.journals_data['abbrv_name']==journal,'found']=True
            elif journal in self.journals_data['journal name'].values:
                self.journals_data.loc[self.journals_data['journal name']==journal,'found']=True

        home_journals_df=self.journals_data.loc[self.journals_data['found']==True]
        # home_journals_df.to_csv(self.path+'home_journals.csv', index=False)



        # for journal in journals:
        #     self.journals_data[self.journals_data['abbrv_name']==journal]
        # home_journals_df=self.journals_data[self.journals_data['abbrv_name'].isin(journals)]
        # home_journals_df.to_csv(self.path+'home_journals.csv', index=False)

        # with open(journals_path + '.pkl', 'wb') as f:
        #     pickle.dump(journals, f, pickle.DEFAULT_PROTOCOL)
        # with open(journals_path, 'w', newline='') as myfile:
        #     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        #     wr.writerow(journals)

    def author_conf_pareto(self):

        index = 0
        count_authors = 0
        count_authors_with_conf = 0
        count_authors_with_corr = 0
        conf_abbrv1 = set(self.conf_data['abbrv_name1'])
        conf_abbrv2 = set(self.conf_data['abbrv_name2'])
        conf_full_name = set(self.conf_data['conf name'])

        func_data_length = len(self.func_data)
        start_time = time.time()
        venues = set()
        conf = set()
        for name, picked_author_dict in self.func_data.items():
            index += 1

            # filter authors with non pareto dist
            if picked_author_dict['func'] != 'exp' and picked_author_dict['func'] != 'inv':
                continue
            num_home_venues = picked_author_dict['hj']
            author_venues = self.data[name]

            count_authors += 1
            home_venues = 0
            found = False
            for venue, num_papers in author_venues.items():
                venues.add(venue)
                if (num_home_venues == 1):
                    if venue == 'corr':
                        count_authors_with_corr += 1
                        break
                home_venues += 1
                if venue in conf_abbrv1 or venue in conf_abbrv2:
                    print(venue)
                    conf.add(venue)
                    found = True
                if home_venues == num_home_venues:
                    break
            if found:
                count_authors_with_conf += 1
                print('found for ', name)
            else:
                home_venues=0
                for venue, num_papers in author_venues.items():
                    home_venues += 1
                    if venue in conf_full_name:
                        conf.add(venue)
                        found = True
                    if home_venues == num_home_venues:
                        break
                if found:
                    count_authors_with_conf += 1
                    print('found for ', name)
        print('')
        print('')
        print('num authors with conf as home venues ', count_authors_with_conf)
        print('num authors with pareto dist ', count_authors)
        print('total num authors with a dist func including error', func_data_length)
        print('num authors with corr as home venues', count_authors_with_corr)
        print('total num venues', len(venues))
        print('total num conferences', len(self.conf_data))
        print('num home conferences of authors with pareto dist', len(conf))
        self.conf_data['found'] = False
        for co in conf:
            if co in self.conf_data['abbrv_name1'].values:
                self.conf_data.loc[self.conf_data['abbrv_name1'] == co, 'found'] = True
            elif co in self.conf_data['abbrv_name2'].values:
                self.conf_data.loc[self.conf_data['abbrv_name2'] == co, 'found'] = True
            elif co in self.conf_data['conf name'].values:
                self.conf_data.loc[self.conf_data['conf name'] == co, 'found'] = True

        home_conf_df = self.conf_data.loc[self.conf_data['found'] == True]
        home_conf_df.to_csv(self.path+'home_conferences.csv', index=False)


    def write_to_csv(self, df, name, index=False):
        # file_path = os.path.join(self.path, name)
        df.to_csv(name, index=index)

    def read_from_csv(self, name, delimiter=None):
        # csv_path = os.path.join(self.path, name)
        papers = pd.read_csv(name, keep_default_na=False, delimiter=delimiter)
        return papers

    def remove_dash(self, issn, eIssn=None):
        journal_ISSN = issn.strip().replace('-', '')
        if eIssn==None:
            return journal_ISSN, eIssn
        journal_eISSN = eIssn.strip().replace('-', '')
        return journal_ISSN, journal_eISSN

    def remove_leading_zeros(self, issn, eIssn=None):
        journal_ISSN = issn.strip().lstrip('0')
        if eIssn==None:
            return journal_ISSN, eIssn
        journal_eISSN = eIssn.strip().lstrip('0')
        return journal_ISSN, journal_eISSN

    def match_to_JCR(self,df, df_JCR):
        df_JCR[['ISSN','eISSN']]=df_JCR.apply(lambda row: pd.Series(self.remove_dash(row['ISSN'], row['eISSN'])), axis=1)
        df_JCR[['ISSN','eISSN']]=df_JCR.apply(lambda row: pd.Series(self.remove_leading_zeros(row['ISSN'], row['eISSN'])), axis=1)
        df_JCR[['Journal name']]=df_JCR.apply(lambda row: pd.Series(row['Journal name'].lower()), axis=1)

        df[['ISSN', 'eISSN']] = df.apply(lambda row: pd.Series(self.remove_dash(row['ISSN'], row['eISSN'])),
                                                 axis=1)
        df[['ISSN', 'eISSN']] = df.apply(
            lambda row: pd.Series(self.remove_leading_zeros(row['ISSN'], row['eISSN'])), axis=1)
        df[['Journal name']] = df.apply(lambda row: pd.Series(row['Journal name'].lower()), axis=1)

        # issn=df_JCR['ISSN'].tolist()

        for row in df.iterrows():
            journal_ISSN = row[1]['ISSN']
            journal_eISSN = row[1]['eISSN']

            journal_name = row[1]['Journal name'].lower()

            # indices = [(s, s.lower().index(journal_ISSN)) for s in issn if s.lower() == journal_ISSN]
            result=df_JCR.loc[df_JCR['ISSN']==journal_ISSN,'JIF Quartile']
            if len(result)>0:
                JIF=result.iloc[0]
                # print(JIF)
                # print(journal_name)
                df.loc[df['ISSN'] == journal_ISSN, 'JIF Quartile'] = JIF
            else:
                result = df_JCR.loc[df_JCR['eISSN'] == journal_eISSN, 'JIF Quartile']
                if len(result) > 0:
                    JIF = result.iloc[0]
                    df.loc[df['ISSN'] == journal_ISSN, 'JIF Quartile'] = JIF
                else:
                    result = df_JCR.loc[df_JCR['Journal name'] == journal_name, 'JIF Quartile']
                    if len(result) > 0:
                        JIF = result.iloc[0]
                        df.loc[df['ISSN'] == journal_ISSN, 'JIF Quartile'] = JIF

    def match_to_JIF(self):
        hj_df = pd.read_csv(self.path + '\\home_journals_sjrq.csv', keep_default_na=False, delimiter=None)
        hj_df['JIF'] = 0
        hj_df['JIF Quartile'] = ''
        list_of_files = list(os.listdir(self.path))
        for file in list_of_files:
            if file.endswith("_2024.csv"):
                filePath = os.path.join(self.path, file)
                print(filePath)
                jcr_df = self.read_from_csv(filePath)
                self.match_to_JCR(hj_df, jcr_df)
        self.write_to_csv(hj_df,self.path+'\\home_journals_sjrq_jifq.csv')

    def extract_catogries_from_jcr(self):
        list_of_files = list(os.listdir(self.path))
        jcr_cats=set()
        for file in list_of_files:
            if file.endswith("_2024.csv"):
                filePath = os.path.join(self.path, file)
                print(filePath)
                jcr_df = self.read_from_csv(filePath)
                cat_names=set(jcr_df['Category'])
                jcr_cats=jcr_cats.union(cat_names)
        print(len(jcr_cats))

    def author_venues(self,
                        sample_rate: int = 1,
                        print_rate: int = 50):
        """
        An author-venue type data for the entire dataset
        """
        answer = {}

        index = 0
        count_authors=0
        count_authors_with_journals=0
        count_authors_with_corr=0
        journals_abbrv=set(self.journals_data['abbrv_name'])
        journals_full_name=set(self.journals_data['journal name'])

        func_data_length = len(self.func_data)
        all_authors=len(self.data)
        start_time = time.time()
        venues=set()
        journals=set()
        for name, picked_author_dict in self.data.items():
            index += 1
            # if (index % print_rate) == 0:
            #     print("Analyzer.identify venue type: Working on line {}/{} ({:.3f}%) in {:.2f} seconds".format(
            #     index,
            #         func_data_length,
            #         100 * index / func_data_length,
            #         time.time() - start_time))
            if name=='ariel rosenfeld':
                print(picked_author_dict)
            # filter authors with not enough data
            # author_venues= self.data[name]
            found=False
            count_authors+=1
            for venue,num_papers in picked_author_dict.items():
                venues.add(venue)
                if venue=='corr':
                    count_authors_with_corr += 1
                    break
                if venue in journals_abbrv:
                    print(venue)
                    journals.add(venue)
                    found=True
            if found:
                count_authors_with_journals+=1
            else:
                for venue, num_papers in picked_author_dict.items():
                    if venue in journals_full_name:
                        journals.add(venue)
                        found = True
                if found:
                    count_authors_with_journals+=1
        print('num authors with journals as home venues ',count_authors_with_journals)
        print('num authors with pareto dist ',count_authors)
        print('total num authors ',all_authors)
        print('num authors with corr',count_authors_with_corr)
        print('total num venues ',len(venues))
        print('total num journals ',journals)

    def match_to_scimago(self):
        hj_df = self.read_from_csv(os.path.join(self.path, 'home_journals.csv'), delimiter=None)
        hj_df['SJR Q'] = 0
        df_scopus = self.read_from_csv(os.path.join(self.path,'scopus_scores_2022.csv'), delimiter=';')
        df_scopus[['Issn', 'eISSN']] = df_scopus['Issn'].str.split(',', n=1, expand=True)
        df_scopus['Title'] = df_scopus.apply(lambda row: pd.Series(row['Title'].lower()), axis=1)

        df_scopus[['Issn', 'eISSN']] = df_scopus.apply(lambda row: pd.Series(self.remove_dash(row['Issn'], row['eISSN'])),
                                                     axis=1)
        df_scopus[['Issn','eISSN']] = df_scopus.apply(
                lambda row: pd.Series(self.remove_leading_zeros(row['Issn'], row['eISSN'])), axis=1)

        hj_df[['ISSN', 'eISSN']] = hj_df.apply(lambda row: pd.Series(self.remove_dash(row['ISSN'], row['eISSN'])),
                                             axis=1)
        hj_df[['ISSN', 'eISSN']] = hj_df.apply(
                lambda row: pd.Series(self.remove_leading_zeros(row['ISSN'], row['eISSN'])), axis=1)
        hj_df[['Journal name']] = hj_df.apply(lambda row: pd.Series(row['Journal name'].lower()), axis=1)

        for row in hj_df.iterrows():
            journal_ISSN = row[1]['ISSN']
            journal_eISSN = row[1]['eISSN']

            journal_name = row[1]['Journal name'].lower()

            # indices = [(s, s.lower().index(journal_ISSN)) for s in issn if s.lower() == journal_ISSN]
            result = df_scopus.loc[df_scopus['Issn'] == journal_ISSN, 'SJR Best Quartile']
            if len(result) > 0:
                SJR_Q = result.iloc[0]
                # print(JIF)
                # print(journal_name)
                hj_df.loc[hj_df['ISSN'] == journal_ISSN, 'SJR Q'] = SJR_Q
            else:
                result = df_scopus.loc[df_scopus['eISSN'] == journal_eISSN, 'SJR Best Quartile']
                if len(result) > 0:
                    SJR_Q = result.iloc[0]
                    hj_df.loc[hj_df['ISSN'] == journal_ISSN, 'SJR Q'] = SJR_Q
                else:
                    result = df_scopus.loc[df_scopus['Title'] == journal_name, 'SJR Best Quartile']
                    if len(result) > 0:
                        SJR_Q = result.iloc[0]
                        hj_df.loc[hj_df['ISSN'] == journal_ISSN, 'SJR Q'] = SJR_Q
        self.write_to_csv(hj_df,self.path+'\\home_journals_sjrq.csv')
        return hj_df

    def home_venues_dist(self):
        func_data_length = len(self.func_data)
        start_time = time.time()
        venues = set()
        home_journals_dist=dict()
        for name, picked_author_dict in self.func_data.items():

            # filter authors with not enough data
            if picked_author_dict['func'] != 'exp' and picked_author_dict['func'] != 'inv':
                continue
            num_home_journals = picked_author_dict['hj']
            if (num_home_journals>=5):
                continue
            if not num_home_journals in home_journals_dist.keys():
                home_journals_dist[num_home_journals]=0
            home_journals_dist[num_home_journals]+=1
        for k,v in home_journals_dist.items():
            print(k,v)

        Plotter.bar_std(x=list(home_journals_dist.keys()),
                        y=[val for val in home_journals_dist.values()],
                        y_err=None,
                        x_label="Home Venues",
                        y_label="Number of Scholars",
                        x_names=list(home_journals_dist.keys()),
                        save_path=os.path.join("home_venues_dist.pdf"), grid=True)



if __name__ == '__main__':
    dblp_venues = DBLP_venues()
    # journals_list=os.path.join(dblp_venues.path, 'home_journals_list')
    # dblp_venues.author_journals_pareto()
    # dblp_venues.author_conf_pareto()
    # dblp_venues.match_to_JIF()
    # dblp_venues.extract_catogries_from_jcr()
    # dblp_venues.match_to_scimago()
    dblp_venues.home_venues_dist()