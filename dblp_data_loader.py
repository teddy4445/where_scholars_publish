# library imports
import os
import re
import gzip
import json
import time
import shutil
import requests
import pandas as pd
from bs4 import BeautifulSoup

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
            print("DLPBdataLoader.run: download dplb data as zip file")
            with open(zip_file_path, 'wb') as file:
                file.write(response.content)
            # download dtd
            response = requests.get(DLPB_DATA_URL_DTD)
            dtd_file_path = os.path.join(os.path.dirname(__file__), RAW_DATA_FOLDER, DLPB_DATA_DTD)
            print("DLPBdataLoader.run: download dplb dtd file")
            with open(dtd_file_path, 'wb') as file:
                file.write(response.content)
            # unzip data
            print("DLPBdataLoader.run: unzip data")
            with gzip.open(zip_file_path, 'rb') as f_in:
                with open(xml_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # remove the zip - no need it anymore
            os.remove(zip_file_path)

        # This is really hard to parse this data as it is 3.5GB so we need to do it in parts
        # Parse a row-level, remember authors in a dict and add the article's journal
        # Update the dict as needed by count the numbers
        answer = {}
        connections = 0
        journal_list = set()
        author_list = set()

        in_article_lines = ["<object>"]
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
                        print("Parse {} lines with {} authors and {} connections so far after {:.3f} seconds".format(line_number,
                                                                                                                     len(answer),
                                                                                                                     connections,
                                                                                                                     time.time() - start_time))

                        print("DLPBdataLoader.run: save temp file to {}".format(save_path))
                        with open(save_path, "w") as answer_file:
                            json.dump(answer, answer_file)

                    # check if we need to process
                    if any([option in line for option in DLPB_TYPES_LINE_END]):
                        # generate the xml text for processing
                        in_article_lines.append("</object>")
                        object_tree = BeautifulSoup("\n".join(in_article_lines), "html.parser")
                        # get the journal name
                        published_at = object_tree.find(DLPB_TYPES[0])
                        if published_at is None:
                            published_at = object_tree.find(DLPB_TYPES[1])
                        published_at = published_at.text.strip().lower()
                        journal_list.add(published_at)
                        for author_obj in object_tree.find_all("author"):
                            author_text = re.search("[a-zA-Z\s]+", author_obj.text)[0].strip().lower()
                            author_list.add(author_text)
                            try:
                                # check if we have this author
                                answer[author_text]
                                # if we do, add journal
                                try:
                                    # check if we have this journal for this author
                                    answer[author_text][published_at]
                                    # if we do, count this publication
                                    answer[author_text][published_at] += 1
                                except KeyError as error:
                                    # if we do not have this journal, it is the first time
                                    answer[author_text][published_at] = 1
                            except KeyError as error:
                                # if we do not have this author, it is a new author and new journal with 1 count
                                answer[author_text] = {published_at: 1}
                            # count connection between author and journal
                            connections += 1
                        # reset to start
                        in_article_lines = ["<object>"]

                    else:  # just recall the line
                        in_article_lines.append(line)
                        # IMPORTANT: edge case - we have "www" section, so clear memory if too large
                        if len(in_article_lines) > DLPB_TOO_LARGE_MEMORY:
                            in_article_lines = ["<object>"]

                except Exception as error:
                    print("Error in line {}, saying {}".format(line_number, error))

        print("DLPBdataLoader.run: analyzed data and save to {}".format(save_path))
        with open(save_path, "w") as answer_file:
            json.dump(answer, answer_file)

        print("DLPBdataLoader.run: journal list to {}".format("journal_list.txt"))
        with open("journal_list.txt", "w") as answer_file:
            json.dump(list(journal_list), answer_file)

        print("DLPBdataLoader.run: journal list to {}".format("author_list.txt"))
        with open("author_list.txt", "w") as answer_file:
            json.dump(list(author_list), answer_file)
