EN_WHITELIST = '0123456789йцукенгшщзхъёфывапролджэячсмитьбю '  # space is included in whitelist
EN_BLACKLIST = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\''

FILENAME = 'general.txt'

limit = {
    'maxq': 20,
    'minq': 0,
    'maxa': 20,
    'mina': 3
}

# VOCAB_SIZE = 6000
VOCAB_SIZE = 15000


import numpy as np

import pickle

'''
 read lines from file
     return [list of lines]

'''


def read_lines(filename):
    return open(filename).read().split('\n')[:-1]


'''
 split sentences in one line
  into multiple lines
    return [list of lines]

'''


def split_line(line):
    return line.split('.')


'''
 remove anything that isn't in the vocabulary
    return str(pure ta/en)

'''


def filter_line(line, whitelist):
    return ''.join([ch for ch in line if ch in whitelist])


'''
 filter too long and too short sequences
    return tuple( filtered_ta, filtered_en )

'''


def filter_data(sequences):
    filtered_q, filtered_a = [], []
    # raw_data_len = len(sequences) // 2

    for i in range(0, len(sequences) - 1, 2):
        qlen, alen = len(sequences[i].split(' ')), len(sequences[i + 1].split(' '))
        if qlen >= limit['minq'] and qlen <= limit['maxq']:
            if alen >= limit['mina'] and alen <= limit['maxa']:
                filtered_q.append(sequences[i])
                filtered_a.append(sequences[i + 1])

    # print the fraction of the original data, filtered
    # filt_data_len = len(filtered_q)
    # filtered = int((raw_data_len - filt_data_len) * 100 / raw_data_len)
    # print(str(filtered) + '% filtered from original data')

    return filtered_q, filtered_a


def clear_message(message):
    message = message.lower()
    message = filter_line(message, EN_WHITELIST)
    return message.split()


def process_data():
    print('\n>> Read lines from file')
    lines = read_lines(filename=FILENAME)

    # filter out too long or too short sequences
    print('\n>> 2nd layer of filtering')
    qlines, alines = filter_data(lines)
    for a in [x for x in alines if x.find('~') != -1]: alines[alines.index(a)] = a[:a.find('~')]
    print('\nq : {0} ; a : {1}'.format(qlines[60], alines[60]))
    print('\nq : {0} ; a : {1}'.format(qlines[61], alines[61]))

    # change to lower case (just for en)
    qlines_filtered = [qline.lower() for qline in qlines]
    alines_filtered = [aline.lower() for aline in alines]

    print('\n:: Sample from read(p) lines')
    print(qlines[121:125])

    # filter out unnecessary characters
    print('\n>> Filter lines')
    qlines_filtered = [filter_line(line, EN_WHITELIST) for line in qlines_filtered]
    alines_filtered = [filter_line(line, EN_WHITELIST) for line in alines_filtered]

    # convert list of [lines of text] into list of [list of words ]
    print('\n>> Segment lines into words')
    qtokenized = [wordlist.split(' ') for wordlist in qlines_filtered]
    atokenized = [wordlist.split(' ') for wordlist in alines_filtered]
    print('\n:: Sample from segmented list of words')
    print('\nq : {0} ; a : {1}'.format(qtokenized[60], atokenized[60]))
    print('\nq : {0} ; a : {1}'.format(qtokenized[61], atokenized[61]))

    metadata = {
        'q_tok': qtokenized,
        'a_tok': atokenized,
        'limit': limit,
        'answers' : alines
    }

    # write to disk : data control dictionaries
    with open('metadata_corpus.pkl', 'wb') as f:
        pickle.dump(metadata, f)


if __name__ == '__main__':
    process_data()
