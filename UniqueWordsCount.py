import re
from collections import Counter
import csv
import os
import time


def read_dict(path_info, path_dict):
    with open(path_info, 'r', newline='', encoding='utf-8') as info_file:
        reader = csv.reader(info_file)
        info = list()
        for row in reader:
            info.append(row[0])
    with open(path_dict, 'r', newline='', encoding='utf-8') as dict_file:
        reader = csv.reader(dict_file)
        word_dict = {}
        for row in reader:
            values = [int(row[1]), float(row[2]), float(row[3]), int(row[4]), float(row[5]), float(row[6]),
                      float(row[7]), float(row[8])]
            word_dict[row[0]] = values
    return int(info[1]), int(info[2]), word_dict


def read_text(path):
    pattern = r"[^\w\s\-\']"
    file = open(path, 'r', encoding='utf-8')
    text = file.read()
    file.close()
    lower_case_text = text.lower()
    prepared_text = re.sub(pattern, '', lower_case_text)
    splitted_text = prepared_text.split()
    stripped_text = [el.strip('\'-') for el in splitted_text]
    remove_chars_pattern = r"[\'\-]"
    cleared_text = [re.sub(remove_chars_pattern, '', el) for el in stripped_text]
    non_empty_text = [el for el in cleared_text if el]
    F_counter = Counter(non_empty_text)
    return F_counter


main_folder_path = 'D:/English base2cleaned&expanded_Metko'
main_corpora_data_path = 'D:/Research/PythonProjects/CorpusData'
corpora_name = 'English base2cleaned&expanded_Metko_with2lotr'
info_path = os.path.join(main_corpora_data_path, corpora_name + '_info.csv')
dict_path = os.path.join(main_corpora_data_path, corpora_name + '_dict.csv')
start_time = time.perf_counter()
print('loading dictionary...')
n, sum_L, words_corpora = read_dict(info_path, dict_path)
print('dictionary loaded')
print('loading texts...')
current_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_path, 'UniqueWordsCount_result.csv'), 'w', newline='', encoding='utf-8') as rang_file:
    writer = csv.writer(rang_file)
    n, SumL = 0, 0
    for root, dirs, files in os.walk(main_folder_path):
        n += len(files)
    processed_n = 0
    for root, dirs, files in os.walk(main_folder_path):
        for name in files:
            text_path = os.path.join(root, name)
            F_counter = read_text(text_path)
            i = 1
            count = 0
            words = '('
            for key, value in F_counter.most_common():
                if value == words_corpora[key][0] and words_corpora[key][0] >= 10:
                    words += key + ', ' + str(value) + ';'
                    count = count + 1
            words = words[:-1]
            if len(words)>0:
                words += ')'
            # print(os.path.basename(text_path), count, words)
            writer.writerow([i, name, count, words])
            i = i + 1
            processed_n += 1
            if processed_n % 50 == 0:
                print('{0:.2f} %'.format(processed_n / n * 100))
    print('{0:.2f} %'.format(processed_n / n * 100))
print('texts loaded')
print("time elapsed", time.perf_counter()-start_time, "s")
