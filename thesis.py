#! /usr/bin/python3

import sys


def get_value(line):
    line = line.strip()
    dirty_list = line.split('-')

    dirty_list.pop(0)
    while dirty_list[0] == '':
        dirty_list.pop(0)

    return_string = ''

    print(dirty_list)

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


def get_run_information(file_name):
    with open(file_name, 'r') as settings_file:
        runs = []

        run_name = settings_file.readline()

        while "***" in run_name:
            run_dictionary = {}
            run_name = run_name.split(' ')[1]

            run_dictionary['RUN_NAME'] = run_name
            remove_fluff(settings_file)
            run_dictionary['DIRECTORY'] = get_value(settings_file.readline())
            remove_fluff(settings_file)
            run_dictionary['WIKI_ADDRESS'] = get_value(settings_file.readline())
            run_dictionary['HEADING_NAME'] = get_value(settings_file.readline())
            run_dictionary['BODY_NAME'] = get_value(settings_file.readline())
            run_dictionary['CRAWL_DEPTH'] = get_value(settings_file.readline())
            run_dictionary['MAX_CRAWL_ITEMS'] = get_value(settings_file.readline())
            remove_fluff(settings_file)
            run_dictionary['VAR_MAX_ITER'] = get_value(settings_file.readline())
            run_dictionary['VAR_CONVERGENCE'] = get_value(settings_file.readline())
            run_dictionary['EM_MAX_ITER'] = get_value(settings_file.readline())
            run_dictionary['EM_CONVERGENCE'] = get_value(settings_file.readline())
            run_dictionary['ALPHA'] = get_value(settings_file.readline())
            run_dictionary['ALPHA_VALUE'] = get_value(settings_file.readline())
            run_dictionary['TOPIC_AMOUNT'] = get_value(settings_file.readline())
            run_dictionary['GENERATION'] = get_value(settings_file.readline())
            remove_fluff(settings_file)
            run_dictionary['NUM_WORDS'] = get_value(settings_file.readline())

            runs.append(run_dictionary)
            run_name = settings_file.readline()

        return runs


def process_run(run_info):
    print("Processing Run: %s" % run_info['RUN_NAME'])



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: ./thesis.py <settings>")
        exit()

    runs = get_run_information(sys.argv[1])

    for run in runs:
        process_run(run)
