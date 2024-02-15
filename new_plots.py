import json
import numpy as np


def run():
    with open("results/profile_author_journal_dist_sr_1_c_5_r2_0.3.json", "r") as data_file:
        data = json.load(data_file)

    r_square_pareto = []
    r_square_non_pareto = []
    pareto_counts = 0
    non_pareto_counts = 0

    for key, items in data.items():
        if items["func"] != "error":
            if items["func"] == "exp" or items["func"] == "inv":
                pareto_counts += 1
                r_square_pareto.append(items["r2"])
            else:
                non_pareto_counts += 1
                r_square_non_pareto.append(items["r2"])

    print("pareto portion: {:.2f}%, non-pareto portion: {:.2f}%".format(100*pareto_counts/(pareto_counts + non_pareto_counts),
                                                                        100*non_pareto_counts/(pareto_counts + non_pareto_counts)))

    print("Pareto R^2: {:.2f} \pm {:.2f}".format(np.mean(r_square_pareto),
                                                 np.std(r_square_pareto)))

    print("Non-Pareto R^2: {:.2f} \pm {:.2f}".format(np.mean(r_square_non_pareto),
                                                     np.std(r_square_non_pareto)))


if __name__ == '__main__':
    run()
