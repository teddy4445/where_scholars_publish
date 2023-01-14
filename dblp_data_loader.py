# library imports
import os
import re
import gzip
import json
import time
import shutil
import requests
import pandas as pd

# project imports
from consts import *


class DLPBdataLoader:
    """
    A class to download the data from DBLP and parse it to something we can work with
    """

    # CONSTS #
    DATA_PATH = os.path.join(os.path.dirname(__file__), DLPB_DATA_XML)

    # END - CONSTS #

    def __init__(self):
        pass

    @staticmethod
    def run(save_path: str,
            need_download: bool = False):
        """
        A single entry method that downloads the data, if needed, and parse it to the right CSV format
        """
        xml_file_path = os.path.join(os.path.dirname(__file__), RAW_DATA_FOLDER, DLPB_DATA_XML)

        if need_download:
            # download data
            response = requests.get(DLPB_DATA_URL)
            zip_file_path = os.path.join(os.path.dirname(__file__), RAW_DATA_FOLDER, DLPB_DATA_ZIP)
            with open(zip_file_path, 'wb') as file:
                file.write(response.content)
            # download dtd
            response = requests.get(DLPB_DATA_URL_DTD)
            dtd_file_path = os.path.join(os.path.dirname(__file__), RAW_DATA_FOLDER, DLPB_DATA_DTD)
            with open(dtd_file_path, 'wb') as file:
                file.write(response.content)
            # unzip data
            with gzip.open(zip_file_path, 'rb') as f_in:
                with open(xml_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # remove the zip - no need it anymore
            os.remove(zip_file_path)

        # This is really hard to parse this data as it is 3.5GB so we need to do it in parts
        # Parse a row-level, remember authors in a dict and add the article's journal
        # Update the dict as needed by count the numbers
        answer = {}

        in_article_flag = False
        in_article_text = []
        # start clock
        start_time = time.time()
        # open xml file as txt file
        with open(xml_file_path, "r") as xml_data_file:
            line_number = 0
            # read line by line
            for line in xml_data_file:
                try:
                    # count line and print from some time to time
                    line_number += 1
                    if (line_number % DLPB_PARSE_PRINT_EACH) == 0:
                        print("Parse {} lines with {} authors so far after {:.3f} seconds".format(line_number,
                                                                                                  len(answer),
                                                                                                  time.time() - start_time))

                    # read data
                    if in_article_flag:
                        if "</article>" in line:
                            in_article_flag = False

                            # find the journal name
                            for line in in_article_text:
                                if "<journal>" in line:
                                    journal_name = line.replace("<journal>", "").replace("</journal>", "").strip().lower()
                                    journal_name = re.search("[a-zA-Z\s]+", journal_name)[0]
                                    break

                            for line in in_article_text:
                                if "<author>" not in line:
                                    continue
                                author_text = line.replace("<author>", "").replace("</author>", "").strip().lower()
                                author_text = re.search("[a-zA-Z\s]+", author_text)[0]
                                try:
                                    # check if we have this author
                                    answer[author_text]
                                    # if we do, add journal
                                    try:
                                        # check if we have this journal for this author
                                        answer[author_text][journal_name]
                                        # if we do, count this publicaiton
                                        answer[author_text][journal_name] += 1
                                    except KeyError as error:
                                        # if we do not have this journal, it is the first time
                                        answer[author_text][journal_name] = 1
                                except KeyError as error:
                                    # if we do not have this author, it is a new author and new journal with 1 count
                                    answer[author_text] = {journal_name: 1}
                        else:
                            # parse data inside an article
                            in_article_text.append(line)
                            continue
                    # check if we need to start collecting
                    if "<article " in line:
                        in_article_flag = True
                        in_article_text = []
                except Exception as error:
                    print("Error in line {}, saying {}".format(line_number, error))

        with open(save_path, "w") as answer_file:
            json.dump(answer, answer_file)
