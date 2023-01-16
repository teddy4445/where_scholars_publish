# library imports
import os
import json

# project imports
from consts import *
from analyzer import Analyzer
from dblp_data_loader import DLPBdataLoader


class Main:
    """
    A class to run the main and test the components of model
    """

    # CONSTS #
    main_data_path = os.path.join(os.path.dirname(__file__), RESULTS_FOLDER, MAIN_DATA_CSV)
    # END - CONSTS #

    def __init__(self):
        pass

    @staticmethod
    def run(prepare_data: bool = False,
            need_download: bool = False):
        Main.prepare_io()
        Main.prepare_data(prepare_data=prepare_data,
                          need_download=need_download)
        Main.analyze_data()

    @staticmethod
    def prepare_io():
        create_paths = [os.path.join(os.path.dirname(__file__), RESULTS_FOLDER),
                        os.path.join(os.path.dirname(__file__), RAW_DATA_FOLDER)]
        for path in create_paths:
            try:
                os.mkdir(path)
            except Exception as error:
                pass

    @staticmethod
    def prepare_data(prepare_data: bool = False,
                     need_download: bool = False):
        # prepare data
        if prepare_data:
            DLPBdataLoader.run(save_path=Main.main_data_path,
                               need_download=need_download)

    @staticmethod
    def analyze_data():
        # prepare analyzer from data file
        analyzer = Analyzer(data_path=Main.main_data_path)

        # run several analysis tasks with plots #
        analyzer.author_journals_count(plot_save_path=os.path.join(os.path.dirname(__file__),
                                                                   RESULTS_FOLDER,
                                                                   "author_journals_count.pdf"),
                                       plot_save_zoom_path=os.path.join(os.path.dirname(__file__),
                                                                        RESULTS_FOLDER,
                                                                        "author_journals_count_zoom.pdf"))

        for author_name in ["ariel rosenfeld", "teddy lazebnik", "ariel alexi"]:
            analyzer.author_journal_dist(author_name=author_name,
                                         plot_save_path=os.path.join(os.path.dirname(__file__),
                                                                     RESULTS_FOLDER,
                                                                     "author_journal_dist_{}.pdf".format(author_name)))

        min_journal_count = 5
        min_r2_score = 0.3
        sample_rate = 100

        analyzer.profile_author_journal_dist(plot_save_path=os.path.join(os.path.dirname(__file__),
                                                                         RESULTS_FOLDER,
                                                                         "profile_author_journal_dist_sr_{}_c_{}_r2_{}.pdf".format(
                                                                             sample_rate,
                                                                             min_journal_count,
                                                                             min_r2_score)),
                                             analysis_save_path=os.path.join(os.path.dirname(__file__),
                                                                             RESULTS_FOLDER,
                                                                             "profile_author_journal_dist_sr_{}_c_{}_r2_{}.json".format(
                                                                                 sample_rate,
                                                                                 min_journal_count,
                                                                                 min_r2_score)),
                                             sample_rate=1,
                                             print_rate=1000,
                                             min_journal_count=min_journal_count,
                                             min_r2_score=min_r2_score)

        author_journal_json_path = os.path.join(os.path.dirname(__file__),
                                                RESULTS_FOLDER,
                                                "profile_author_journal_dist_sr_{}_c_{}_r2_{}.json".format(
                                                    sample_rate,
                                                    min_journal_count,
                                                    min_r2_score))
        Analyzer.profile_author_journal_r2_dist(data_path=author_journal_json_path,
                                                folder_save_path=os.path.join(os.path.dirname(__file__),
                                                                              RESULTS_FOLDER))

        # TODO: think how to finish this one later
        """
        Analyzer.cluster_author_journal(x_train=,
                                        x_test=,
                                        y_test=,
                                        cluster_n=,
                                        save_path=)
        """


if __name__ == '__main__':
    Main.run(prepare_data=True,
             need_download=False)
