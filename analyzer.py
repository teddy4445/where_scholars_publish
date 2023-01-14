# library imports
import os
import json

# project imports
from consts import *
from plotter import Plotter


class Analyzer:
    """
    A class responsible to perform different analysis on the data
    """

    # CONSTS #

    # END - CONSTS #

    def __init__(self,
                 data_path: str):
        with open(data_path, "r") as data_file:
            self.data = json.load(data_file)

    def author_journals_count(self,
                              plot_save_path: str,
                              plot_save_zoom_path: str,
                              zoom_threshold: int = 20):
        """
        authors to journals count plot
        """
        data = [len(data) for data in self.data.values()]
        Plotter.hist(data=data,
                     x_label="Journals per author",
                     y_label="Count",
                     normalize=False,
                     save_path=plot_save_path)

        Plotter.hist(data=[val for val in data if val < zoom_threshold],
                     x_label="Journals per author",
                     y_label="Count",
                     normalize=False,
                     save_path=plot_save_zoom_path)

    def author_journal_dist(self,
                            author_name: str,
                            plot_save_path: str):
        """
        An author-journal dist data
        """
        try:
            picked_author_dict = self.data[author_name]
            data_as_list = [(name, count) for name, count in picked_author_dict.items()]
            data_as_list = sorted(data_as_list,
                                  key=lambda x: x[1],
                                  reverse=True)
            x = list(range(1, 1+len(data_as_list)))
            y = [val[1] for val in data_as_list]
            Plotter.author_journal(x=x,
                                   y=y,
                                   x_label="Journals",
                                   y_label="Counts",
                                   x_names=[val[0] for val in data_as_list],
                                   save_path=plot_save_path,
                                   ylim=(0, max(y)+1),
                                   xlim=(0.5, max(x)+0.5))
        except KeyError as error:
            print("Cannot compute Analyzer.author_journal_dist with author_name={}, because={}".format(author_name,
                                                                                                       error))
