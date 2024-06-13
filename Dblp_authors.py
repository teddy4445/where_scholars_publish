from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
import pandas as pd
import threading
from consts import *
import os
from datetime import datetime
import sys


class Dblp_authors:
    path = r'./'
    func_data_path = os.path.join(path, FUNC_DATA_JSON)

    def __init__(self):
        with open(Dblp_authors.func_data_path, "r") as func_data_file:
            self.func_data = json.load(func_data_file)
        con_file = open("conf.json")
        self.config = json.load(con_file)
        con_file.close()
        # self.path = config['path']

        ## Initialize client
        self.keysCount = 0
        ## Initialize client
        self.client = ElsClient(self.config['apikeys'][self.keysCount])
        self.client = ElsClient(self.config['apikey1'])

        self.client.inst_token = self.config['insttoken']
        original = sys.stdout
        sys.stdout = open('./redirect.txt', 'w')

    def get_authors_from_scopus(self, authors_df, starting_point=0):
        count = 0
        print(starting_point)
        # for idx, row in authors_df[authors_df.index >= starting_point].iterrows():
        for row in authors_df.iterrows():
            count += 1
            if count < starting_point:
                continue
            if count % 500 == 0:
                authors_df.to_csv('authors_hindex.csv')
                authors_df.to_csv('D:\\authors_hindex.csv')
                # self.keysCount += 1
                # if self.keysCount >= 9:
                #     break
                # self.client = ElsClient(self.config['apikeys'][self.keysCount])
            if count == starting_point + 26005:
                authors_df.to_csv('authors_hindex.csv')
                authors_df.to_csv('D:\\authors_hindex.csv')
                break

            try:
                author_name = row[1]['author name'].replace('\"', '').strip()
                author_name_parts = author_name.split(' ')
                if len(author_name_parts) < 3:
                    author_last_name = author_name_parts[-1]

                else:
                    author_last_name = ' '.join([author_name_parts[-2], author_name_parts[-1]])
                author_first_name = author_name_parts[0]
                try:
                    auth_srch = ElsSearch(
                        'AUTHLASTNAME(' + author_last_name + ') And AUTHFIRST(' + author_first_name + ')', 'author')
                    auth_srch.execute(self.client)
                    if len(auth_srch.results) == 1 and 'error' in auth_srch.results[0].keys():
                        author_last_name = author_name_parts[-1]
                        author_first_name = author_name_parts[0]
                        auth_srch = ElsSearch(
                            'AUTHLASTNAME(' + author_last_name + ') And AUTHFIRST(' + author_first_name + ')', 'author')
                        auth_srch.execute(self.client)
                    print("auth_srch has", len(auth_srch.results), "results.")
                    df = auth_srch.results_df
                    if 'orcid' in df.columns:
                        author_id = df.loc[df['orcid'].isna() == False, "dc:identifier"].array[0]
                        author_id = author_id.split(':')[1]
                        my_auth = ElsAuthor(author_id=author_id)
                        # Read author data, then write to disk
                        if my_auth.read_metrics(self.client):
                            h_index = my_auth.data['h-index']
                            print("author {} h index: {} ".format(author_name, h_index))
                            authors_df.loc[authors_df['author name'] == author_name, 'h-index'] = h_index
                        else:
                            print("Read author failed.")
                    elif len(auth_srch.results) == 1:
                        auth_srch.results[0]
                        author_id = df["dc:identifier"][0]
                        author_id = author_id.split(':')[1]
                        my_auth = ElsAuthor(author_id=author_id)
                        # Read author data, then write to disk
                        if my_auth.read_metrics(self.client):
                            h_index = my_auth.data['h-index']
                            print("author {} h index: {} ".format(author_name, h_index))
                            authors_df.loc[authors_df['author name'] == author_name, 'h-index'] = h_index
                        else:
                            print("Read author failed.")
                    else:
                        for auth_item in df.iterrows():
                            if isinstance(auth_item[1]['subject-area'], dict):
                                subject_area_str = auth_item[1]['subject-area']['@abbrev']
                            else:
                                subject_area_str = ';'.join(d['@abbrev'] for d in auth_item[1]['subject-area'])
                            if subject_area_str.count('COMP') > 0 or subject_area_str.count('MATH') > 0:
                                author_id = auth_item[1]['dc:identifier']
                                author_id = author_id.split(':')[1]
                                my_auth = ElsAuthor(author_id=author_id)
                                # Read author data, then write to disk
                                if my_auth.read_metrics(self.client):
                                    h_index = my_auth.data['h-index']
                                    print("author {} h index: {} ".format(author_name, h_index))
                                    authors_df.loc[authors_df['author name'] == author_name, 'h-index'] = h_index
                                    break
                                else:
                                    print("Read author failed.")


                except Exception as e:
                    print('exception {} for {}'.format(e, author_name))
            except Exception as ex:
                print('exception {}'.format(ex))
        return authors_df

    def get_authors_list(self):
        all_authors = set()

        for name, picked_author_dict in self.func_data.items():
            if picked_author_dict['func'] != 'exp' and picked_author_dict['func'] != 'inv':
                continue
            all_authors.add(name)
        return all_authors




if __name__ == '__main__':
    # utils=Utils()
    dblp = Dblp_authors()
    print(datetime.now())

    '''
    authors_list=dblp.get_authors_list()
    authors_list_df1=pd.DataFrame(authors_list, columns=['author name'])
    authors_list_df1['h-index']=-1
    # print(authors_list_df)

    print(datetime.now())
    print(authors_list_df.head(500))
    print(len(authors_list_df))
    authors_list_df.to_csv('authors_df.csv')
    '''
    authors_list_df = pd.read_csv('authors_df.csv')
    #     dblp.get_authors_from_scopus(authors_list_df, starting_point=281000)
    # dblp.get_authors_from_scopus(authors_list_df, starting_point=10)


    #authors_list_df.to_csv('authors_hindex.csv')
    print(datetime.now())