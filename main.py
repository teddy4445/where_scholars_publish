# library imports
import os

# project imports
from consts import *
from analyzer import Analyzer
from dblp_data_loader import DLPBdataLoader


class Main:
    """
    A class to run the main and test the components of model
    """

    def __init__(self):
        pass

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
    def run(prepare_data: bool = False,
            need_download: bool = False):
        # prepare IO
        Main.prepare_io()
        main_data_path = os.path.join(os.path.dirname(__file__), RESULTS_FOLDER, MAIN_DATA_CSV)
        # prepare data
        if prepare_data:
            DLPBdataLoader.run(save_path=main_data_path,
                               need_download=need_download)
        # prepare analyzer from data file
        analyzer = Analyzer(data_path=main_data_path)

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
        Analyzer.profile_author_journal_r2_dist(data_path=os.path.join(os.path.dirname(__file__),
                                                                       RESULTS_FOLDER,
                                                                       "profile_author_journal_dist_sr_{}_c_{}_r2_{}.json".format(
                                                                           sample_rate,
                                                                           min_journal_count,
                                                                           min_r2_score)),
                                                folder_save_path=os.path.join(os.path.dirname(__file__),
                                                                              RESULTS_FOLDER))


if __name__ == '__main__':
    Main.run(prepare_data=True,
             need_download=False)
