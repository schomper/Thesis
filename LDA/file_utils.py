import os
import util_functions
import global_att


# read_settings
#   read in the settings file into global variables
def read_settings(file_name):
    settings_file = open(file_name, "r")

    # set global variables from settings file
    global_att.VAR_MAX_ITER = int(settings_file.readline().strip())
    global_att.VAR_CONVERGED = float(settings_file.readline().strip())
    global_att.EM_MAX_ITER = int(settings_file.readline().strip())
    global_att.EM_CONVERGED = float(settings_file.readline().strip())
    alpha_action = settings_file.readline().strip()

    # set estimate alpha varible
    if alpha_action == "fixed":
        global_att.ESTIMATE_ALPHA = 0
    else:
        global_att.ESTIMATE_ALPHA = 1

    settings_file.close()


def make_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def save_gamma(filename, gamma, num_docs, num_topics):
    file_pointer = open(filename, "w")

    for d in range(0, num_docs):
        file_pointer.write("%5.10f" % gamma[d][0])

        for k in range(1, num_topics):
            file_pointer.write(" %5.10f" % gamma[d][k])

        file_pointer.write("\n")

    file_pointer.close()


# writes the word assignments line for a document to a file
def write_word_assignment(file_pointer, document, phi):
    file_pointer.write("%03d" % document.unique_word_count)

    # for each word
    for n in range(0, document.unique_word_count):
        file_pointer.write(" %04d:%02d" % (
            document.words[n], util_functions.max_value_position(phi[n])))

    file_pointer.write("\n")
