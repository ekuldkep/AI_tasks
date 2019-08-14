import csv


class Constants:
    enron = 0
    company = 1
    statements = 2
    may = 3
    http = 4
    email = 5
    within = 6
    report = 7
    price = 8
    money = 9
    now = 10
    securities = 11
    spam = 12


def read_txt_file(filename):
    with open(filename) as f:
        first = f.readline()  # skip first line
        lines = f.readlines()
        matrix = []
        for line in lines:
            row = line.split(',')
            row = [int(i) for i in row]
            print(row)
            matrix.append(row)
        return matrix, first


def classify_spam(spam_matrix):
    spam = [row for row in spam_matrix if row[Constants.spam]]
    not_spam = [row for row in spam_matrix if not row[Constants.spam]]
    return spam, not_spam


def calculate_percentages(matrix, first):
    spam, no_spam = classify_spam(matrix)
    spam_count = len(spam)
    no_spam_count = len(no_spam)
    matrix_row_count = len(matrix)
    spam_probability = spam_count/matrix_row_count
    no_spam_probability = no_spam_count/matrix_row_count

    no_spam_dic = {}
    spam_dic = {}
    word_prob_global = {}

    no_spam_dic_multy = 1
    spam_dic_multy = 1
    word_prob_global_multy = 1
    for i, word in enumerate(first):
        word_count_spam = sum(row[i] for row in spam)
        word_count_no_spam = sum(row[i] for row in no_spam)
        word_count_global = sum(row[i] for row in matrix)

        no_spam_dic[word] = (word_count_no_spam + 1)/(no_spam_count + 2)
        spam_dic[word] = (word_count_spam + 1)/(spam_count + 2)
        word_prob_global[word] = word_count_global/len(matrix)

        no_spam_dic_multy *= no_spam_dic[word]
        spam_dic_multy *= spam_dic[word]
        word_prob_global_multy *= word_prob_global[word]

    spam_probability_words = spam_dic_multy * spam_probability / word_prob_global_multy
    no_spam_probability_words = no_spam_dic_multy * no_spam_probability / word_prob_global_multy

    return spam_probability_words, no_spam_probability_words



read_txt_file('spam.txt')
