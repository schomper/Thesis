#! /usr/bin/python3

import os
import sys


def get_value(line):
    line = line.strip()
    dirty_list = line.split('-')

    dirty_list.pop(0)
    while dirty_list[0] == '':
        dirty_list.pop(0)

    return_string = ''

    for x in range(len(dirty_list) - 1):
        return_string += dirty_list[x]
        return_string += '-'

    return_string += dirty_list[-1]

    return return_string


def remove_fluff(settings_file):
    """ Reads through the comment sections of the settings file

    :param settings_file: the setting file pointer
    """

    settings_file.readline()
    settings_file.readline()
    settings_file.readline()


def get_session_info(file_name):
    with open(file_name, 'r') as settings_file:
        runs = []

        run_name = settings_file.readline()

        while "***" in run_name:
            run_dictionary = {}
            run_name = run_name.split(' ')[1]

            run_dictionary['RUN_NAME'] = run_name
            # Run info
            remove_fluff(settings_file)
            run_dictionary['DIRECTORY'] = get_value(settings_file.readline()) + "/" + run_dictionary['RUN_NAME']
            make_directory(run_dictionary['DIRECTORY'])
            # Crawler info
            remove_fluff(settings_file)
            run_dictionary['WIKI_ADDRESS'] = get_value(settings_file.readline())
            run_dictionary['HEADING_NAME'] = get_value(settings_file.readline())
            run_dictionary['BODY_NAME'] = get_value(settings_file.readline())
            run_dictionary['CRAWL_DEPTH'] = get_value(settings_file.readline())
            run_dictionary['MAX_CRAWL_ITEMS'] = get_value(settings_file.readline())
            # Estimate info
            remove_fluff(settings_file)
            run_dictionary['VAR_MAX_ITER'] = get_value(settings_file.readline())
            run_dictionary['VAR_CONVERGENCE'] = get_value(settings_file.readline())
            run_dictionary['EM_MAX_ITER'] = get_value(settings_file.readline())
            run_dictionary['EM_CONVERGENCE'] = get_value(settings_file.readline())
            run_dictionary['ALPHA'] = get_value(settings_file.readline())
            run_dictionary['ALPHA_VALUE'] = get_value(settings_file.readline())
            run_dictionary['TOPIC_AMOUNT'] = get_value(settings_file.readline())
            run_dictionary['GENERATION'] = get_value(settings_file.readline())
            # Print topic info
            remove_fluff(settings_file)
            run_dictionary['NUM_WORDS'] = get_value(settings_file.readline())

            runs.append(run_dictionary)
            run_name = settings_file.readline()

        return runs

def make_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def generate_settings(run_info):

    f = open('generated_settings.txt', 'w')
    
    f.write(run_info['VAR_MAX_ITER'] + "\n")
    f.write(run_info['VAR_CONVERGENCE'] + "\n")
    f.write(run_info['EM_MAX_ITER'] + "\n")
    f.write(run_info['EM_CONVERGENCE'] + "\n")
    f.write(run_info['ALPHA'] + "\n")

    f.close()

def process_run(run_info):

    generate_settings(run_info)

    print("Processing Run: %s" % run_info['RUN_NAME'])

    # Run webcrawler
    print("###################################")
    print("# Web crawler")
    print("###################################")
    input_text = "./Tools/Crawler/web_crawler.py " + run_info['WIKI_ADDRESS'] + " " +  run_info['CRAWL_DEPTH'] + " " + run_info['HEADING_NAME']\
                                                  + " " + run_info['BODY_NAME'] + " " + run_info['MAX_CRAWL_ITEMS'] + " " + run_info['DIRECTORY'] + "/documents.txt" 
    os.system(input_text)
    
    # Run process webcrawler output
    print("###################################")
    print("# Vocab Generation")
    print("###################################")
    input_text = "./Tools/gen_vocab_file.py " + run_info['DIRECTORY']
    os.system(input_text)

    # Run estimation script
    print("###################################")
    print("# LDA Estimate")
    print("###################################")
    input_text = "./LDA/lda_estimate.py " + run_info['ALPHA_VALUE'] + " " + run_info['TOPIC_AMOUNT'] + " generated_settings.txt " + run_info['DIRECTORY'] + "/formatted.txt "\
                                          + run_info['GENERATION'] + " " + run_info['DIRECTORY'] + "/Estimate"
    os.system(input_text)

    print("###################################")
    print("# Print Topics")
    print("###################################")
    input_text = "./Tools/print_topics.py " + run_info['DIRECTORY'] + "/Estimate/final.beta" + " " + run_info['DIRECTORY'] + "/vocab.txt" + " " + run_info['NUM_WORDS'] + " " + run_info['DIRECTORY']
    os.system(input_text)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: ./thesis.py <settings>")
        exit()

    runs = get_session_info(sys.argv[1])

    for run in runs:
        process_run(run)
