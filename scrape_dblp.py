import time
import urllib.request as urlreq
import os
import pandas as pd
from bs4 import BeautifulSoup

class Scrape:
    path = r'C:\Users\shira\OneDrive - Bar Ilan University\research\dblp'


    def getJournalsData(self,df):
        journals_list=[]
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent, }
        # for offset in range(1,100, 100):
        for offset in range(1, 4500, 100):

            url = "https://dblp.org/db/journals/index.html?pos="+str(offset)

            request = urlreq.Request(url, None, headers)  # The assembled requestprint(html.read())
            response = urlreq.urlopen(request)
            data = response.read()  # The data u need
        # print(data)
            bsObj = BeautifulSoup(data, "html.parser")

            try:
                div1 = bsObj.find('div', {"class": "hide-body"})
                list1=div1.findAll('a')
                for journal in list1:
                    href=journal['href']
                    # journal_name=journal.text
                    journals_list.append(href)
                    print(href)

            except Exception as e:
                print("error "+e)
        count =0
        for url in journals_list:
            count+=1
            try:
                request = urlreq.Request(url, None, headers)  # The assembled requestprint(html.read())
                time.sleep(3)
                print(count)
                response = urlreq.urlopen(request)
                data = response.read()  # The data u need
            # print(data)
                bsObj = BeautifulSoup(data, "html.parser")
                journal_name = bsObj.find('h1').text
                journal_details = bsObj.findAll('div', {"class": "hide-body"})[1]
                journal_details=journal_details.findAll('li')
                abbrv_name=''
                for i in range(0,len(journal_details)):
                    if 'ISO 4 abbr.:' in journal_details[i].text:
                        abbrv_name=journal_details[0].text.split('issn')[0].split('ISO 4 abbr.:')[1].strip()
                    if 'issn' in journal_details[i].text:
                        issn_eissn=journal_details[i].text.split('issn')[1].strip(':').strip()
                        if ';' in issn_eissn:
                            issn_eissn= issn_eissn.split(';')
                            issn=issn_eissn[0].strip('(print)').strip()
                            eissn=issn_eissn[1].strip('(online)').strip()
                        else:
                            if '(online)' in issn_eissn:
                                eissn=issn_eissn.strip('(online)').strip()
                                issn=''
                            else:
                                issn=issn_eissn.strip('(print)').strip()
                                eissn=''
                    # print(journal_details[i])
                print(journal_name, abbrv_name, issn, eissn)
                df.loc[len(df)]=[journal_name, abbrv_name, url, issn, eissn]
            except:
                continue

    def getConfData(self,df):
        journals_list=[]
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent, }
        for offset in range(15001,19200, 100):
        # for offset in range(1, 19100, 100):
            print('offset {}'.format(offset))
            # if offset==10001:
            #     time.sleep(10)
            url = "https://dblp.org/db/conf/index.html?pos="+str(offset)

            request = urlreq.Request(url, None, headers)  # The assembled requestprint(html.read())
            response = urlreq.urlopen(request)
            data = response.read()  # The data u need
        # print(data)
            bsObj = BeautifulSoup(data, "html.parser")
            try:
                div1 = bsObj.find('div', {"class": "hide-body"})
                list1=div1.findAll('a')
                for journal in list1:
                    href=journal['href']
                    # journal_name=journal.text
                    journals_list.append(href)
                    print(href)

            except Exception as e:
                print("error "+e)
        count =0
        for url in journals_list:
            count+=1
            conf_abbrv=url.split('/')[-2].lower()
            # print(conf_abbrv)
            try:
                request = urlreq.Request(url, None, headers)  # The assembled requestprint(html.read())
                time.sleep(3)
                print(count)
                response = urlreq.urlopen(request)
                data = response.read()  # The data u need
            # print(data)
                bsObj = BeautifulSoup(data, "html.parser")
                conf_name = bsObj.find('h1').text
                abbrv_name2=''
                parts=conf_name.split('(')
                if len(parts)>1:
                    abbrv_name2=parts[1].split(')')[0].lower()
                # print(abbrv_name2)
                df.loc[len(df)]=[conf_name, conf_abbrv, abbrv_name2, url]
            except:
                continue

    def write_to_csv(self, df, name, index=False):
        df.to_csv(name, index=index)



if __name__ == '__main__':
    dblp_scrape= Scrape()
    df = pd.DataFrame(columns=['conf name','abbrv_name1','abbrv_name2', 'url'])
    dblp_scrape.getConfData(df)
    dblp_scrape.write_to_csv(df,r'C:\Users\shira\OneDrive - Bar Ilan University\research\dblp\my_conf4.csv')

