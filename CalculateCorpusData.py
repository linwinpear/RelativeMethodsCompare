from collections import Counter
import os
import re
import time
import csv
import math


def read_corpora(main_folder_path, new_file_path):
    g_sumF_counter, g_fm_counter, g_fmw_counter, g_nt_counter = Counter(), Counter(), Counter(), Counter()
    g_fqm_counter, g_fcm_counter = Counter(), Counter()
    g_sigma_counter, g_sigmaw_counter = Counter(), Counter()
    n, SumL = 0, 0
    for root, dirs, files in os.walk(main_folder_path):
        n += len(files)
    processed_n = 0
    pattern = r"[^\w\s\-\']"
    print('start reading corpora')
    for root, dirs, files in os.walk(main_folder_path):
        for name in files:
            file = open(os.path.join(root, name), 'r', encoding='utf-8')
            text = file.read()
            file.close()
            lower_case_text = text.lower()
            prepared_text = re.sub(pattern, '', lower_case_text)
            splitted_text = prepared_text.split()
            stripped_text = [el.strip('\'-') for el in splitted_text]
            non_empty_text = [el for el in stripped_text if el]
            L = len(non_empty_text)
            l_F_counter = Counter(non_empty_text)
            l_fm_counter = Counter()
            l_fqm_counter = Counter()
            l_fcm_counter = Counter()
            for key in l_F_counter:
                F = l_F_counter[key]
                Fq = F ** 2
                l_fm_counter[key] = F / L
                l_fqm_counter[key] = Fq / (L ** 2)
                l_fcm_counter[key] = Fq / L
                g_nt_counter[key] += 1
            g_sumF_counter += l_F_counter
            g_fm_counter += l_fm_counter
            g_fqm_counter += l_fqm_counter
            g_fcm_counter += l_fcm_counter
            SumL += L
            processed_n += 1
            if processed_n % 50 == 0:
                print('{0:.2f} %'.format(processed_n/n*100))
    print('{0:.2f} %'.format(processed_n / n * 100))
    for key in g_fm_counter:
        g_fm_counter[key] /= n
    for key in g_sumF_counter:
        sumF = g_sumF_counter[key]
        g_fmw_counter[key] = sumF / SumL
        g_sigma_counter[key] = math.sqrt((g_fqm_counter[key] / n) - (g_fm_counter[key] ** 2))
        g_sigmaw_counter[key] = math.sqrt((g_fcm_counter[key] - (sumF ** 2) / SumL) / SumL)
    SumTypes = len(list(g_sumF_counter))
    corpora_name = os.path.split(main_folder_path)[-1]
    path = os.path.join(new_file_path, corpora_name + '_info.csv')
    write_info(path, corpora_name, n, SumL, SumTypes, pattern)
    return g_sumF_counter, g_fm_counter, g_fmw_counter, g_nt_counter, g_sigma_counter, g_sigmaw_counter, \
           g_fcm_counter, g_fqm_counter


def write_info(path, corpora_name, n, sum_l, sum_types, pattern):
    with open(path, 'w', newline='', encoding='utf-8') as info_file:
        writer = csv.writer(info_file)
        writer.writerow([corpora_name, 'root folder (corpora name)'])
        writer.writerow([n, 'number of all texts'])
        writer.writerow([sum_l, 'number of all words in all texts'])
        writer.writerow([sum_types, 'number of words types in all texts'])
        writer.writerow([pattern, 'pre-processing regex pattern'])


def write_dict(path, F, fm, fmw, n_t, sigma, sigmaw, fc, fq):
    with open(path, 'w', newline='', encoding='utf-8') as dict_file:
        writer = csv.writer(dict_file)
        for key in dict(F.most_common()):
            writer.writerow([key, F[key], fm[key], fmw[key], n_t[key], sigma[key], sigmaw[key], fc[key], fq[key]])


# corpora_path = 'D:/Test'
corpora_path = 'D:/English base2cleaned&expanded_Metko'
start_time = time.perf_counter()
current_path = os.path.dirname(os.path.abspath(__file__))
new_path = os.path.join(current_path, 'CorpusData')
if not os.path.exists(new_path):
    os.makedirs(new_path)
F, fm, fmw, n_t, sigma, sigmaw, fc, fq = read_corpora(corpora_path, new_path)
corpora_name = os.path.split(corpora_path)[-1]
path = os.path.join(new_path,corpora_name + '_dict.csv')
write_dict(path, F, fm, fmw, n_t, sigma, sigmaw, fc, fq)
# print(f.most_common(1000))
# print(fm.most_common(1000))
# print(fmw.most_common(1000))
print("time elapsed", time.perf_counter()-start_time, "s")
