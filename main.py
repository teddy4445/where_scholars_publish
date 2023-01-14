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
    def run(prepare_data: bool = False):
        # prepare IO
        Main.prepare_io()
        main_data_path = os.path.join(os.path.dirname(__file__), RESULTS_FOLDER, MAIN_DATA_CSV)
        # prepare data
        if prepare_data:
            DLPBdataLoader.run(save_path=main_data_path,
                               need_download=False)
        # prepare analyzer from data file
        analyzer = Analyzer(data_path=main_data_path)

        # run several analysis tasks with plots #
        analyzer.author_journals_count(plot_save_path=os.path.join(os.path.dirname(__file__),
                                                                   RESULTS_FOLDER,
                                                                   "author_journals_count.pdf"),
                                       plot_save_zoom_path=os.path.join(os.path.dirname(__file__),
                                                                        RESULTS_FOLDER,
                                                                        "author_journals_count_zoom.pdf"))

        analyzer.author_journal_dist(author_name="felix lazebnik",
                                     plot_save_path=os.path.join(os.path.dirname(__file__),
                                                                 RESULTS_FOLDER,
                                                                 "author_journal_dist_felix_lazebnik.pdf"))


if __name__ == '__main__':
    Main.run(prepare_data=True)
