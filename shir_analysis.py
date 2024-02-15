import json


def run():
    with open("results/data.json", "r") as data_file:
        data = json.load(data_file)
    author_list = set()
    journal_list = set()

    for key, value in data.items():
        author_list.add(key)
        for name, count in value.items():
            journal_list.add(name)

    print("Journal size {}".format(len(journal_list)))

    with open("journal_list.txt", "w") as answer_file:
        json.dump(list(journal_list), answer_file)

    with open("author_list.txt", "w") as answer_file:
        json.dump(list(author_list), answer_file)


if __name__ == '__main__':
    run()
