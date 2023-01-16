# library imports
import os
import json
import time
import pandas as pd

# project imports
from consts import *
from fit_functions import *
from plotter import Plotter
from data_analytical_fit import DataAnalyticalFit
from research_type_profiler import ResearchTypeProfiler


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
            x = list(range(1, 1 + len(data_as_list)))
            y = [val[1] for val in data_as_list]

            # add the fitting
            best_func, params, best_r2 = DataAnalyticalFit.fit_data(data=y)

            Plotter.author_journal(x=x,
                                   y=y,
                                   y_fit=fit_funcs[best_func](np.asarray(x), *params),
                                   fit_label="$y = {} | R^2={:.3f}$".format(fit_string_funcs[best_func].format(*params),
                                                                            best_r2),
                                   x_label="Journals",
                                   y_label="Counts",
                                   author_name=author_name.title(),
                                   x_names=[val[0] for val in data_as_list],
                                   save_path=plot_save_path,
                                   ylim=(0, max(y) + 1),
                                   xlim=(0.5, max(x) + 0.5))
        except KeyError as error:
            print("Cannot compute Analyzer.author_journal_dist with author_name={}, because={}".format(author_name,
                                                                                                       error))

    def profile_author_journal_dist(self,
                                    analysis_save_path: str,
                                    plot_save_path: str,
                                    min_journal_count: int = 1,
                                    min_r2_score: float = 0.3,
                                    sample_rate: int = 1,
                                    print_rate: int = 1):
        """
        An author-journal dist data for the entire dataset
        """
        answer = {}
        plot_answer = {}
        index = 0
        data_length = len(self.data)
        start_time = time.time()
        for name, picked_author_dict in self.data.items():
            index += 1
            if index > 1 and (index % sample_rate) != 0:
                continue
            if (index % print_rate) == 0:
                print("Analyzer.profile_author_journal_dist: Working on line {}/{} ({:.3f}%) in {:.2f} seconds".format(
                    index,
                    data_length,
                    100 * index / data_length,
                    time.time() - start_time))

            # filter authors with not enough data
            if len(picked_author_dict) < min_journal_count:
                continue

            data_as_list = [(name, count) for name, count in picked_author_dict.items()]
            data_as_list = sorted(data_as_list,
                                  key=lambda x: x[1],
                                  reverse=True)
            best_func, params, r2 = DataAnalyticalFit.fit_data(data=[val[1] for val in data_as_list])

            answer[name] = {"func": best_func,
                            "params": list(params),
                            "r2": r2}

            if r2 < min_r2_score:
                best_func = "error"
            try:
                plot_answer[best_func] += 1
            except:
                plot_answer[best_func] = 1

        # show plot
        Plotter.bar(x=list(range(len(plot_answer.keys()))),
                    y=list(plot_answer.values()),
                    x_label="Fit type",
                    y_label="Counts",
                    x_names=list(plot_answer.keys()),
                    save_path=plot_save_path)
        # save analyzed data
        with open(analysis_save_path, "w") as answer_file:
            json.dump(answer, answer_file)

    @staticmethod
    def profile_author_journal_r2_dist(data_path: str,
                                       folder_save_path: str):
        """
        A profile of author and journals fit type with mean and std of each fit type as well as
        """
        # start with preparation of the folder
        try:
            os.mkdir(folder_save_path)
        except:
            pass

        # load data
        with open(data_path, "r") as data_file:
            data = json.load(data_file)

        # for each fit type, r2 dist
        fit_r2 = {func_name: [] for func_name in fit_funcs}
        [fit_r2[val["func"]].append(val["r2"]) for key, val in data.items()]

        fit_stats = {}
        # print and calc mean and std
        for key, value in fit_r2.items():
            Plotter.hist(data=value,
                         x_label="$R^2$",
                         y_label="Count",
                         xlim=(0, 1),
                         save_path=os.path.join(folder_save_path, "r2_{}_hist.pdf".format(key)))
            fit_stats[key] = [np.mean(value), np.std(value)]
        print("Analyzer.profile_author_journal_r2_dist, stats summary: {}".format(fit_stats))
        Plotter.bar_std(x=list(range(len(fit_funcs))),
                        y=[val[0] for val in fit_stats.values()],
                        x_label="Function type",
                        y_label="$R^2$",
                        y_err=[val[1] for val in fit_stats.values()],
                        x_names=list(fit_funcs.keys()),
                        save_path=os.path.join(folder_save_path, "r2_dist.pdf"))

    @staticmethod
    def cluster_author_journal(x_train: pd.DataFrame,
                               x_test: pd.DataFrame,
                               y_test: pd.Series,
                               cluster_n: int,
                               save_path: str):
        """
        Check if we can cluster the data properly with some hypothesis we have
        The hypothesis check is reflected using the test set where one declares which
        samples in x_test should be in the same cluster using the y_test vector
        """
        # train the clusters
        cluster_model = ResearchTypeProfiler(cluster_n=cluster_n)
        cluster_model.train(x=x_train)
        test_results = cluster_model.test(x=x_test,
                                          y=y_test)
        with open(save_path, "w") as result_file:
            json.dump(test_results,
                      result_file,
                      indent=2)