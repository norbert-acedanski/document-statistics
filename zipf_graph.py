from fileinput import FileInput
import matplotlib.pyplot as plt
import re

file_name = "process_file.txt"
start_index = 0
amount_of_words_to_display = 100
list_of_characters_to_cut = ["‘", "’", "'", "–", "-"]

def load_data():
    # global data
    try:
        with open(file_name, "r", encoding='utf-8') as input_file:
            data = input_file.readlines()
            for (line_number, line) in enumerate(data):
                data[line_number] = line.replace('\n', '')
    except OSError:
        raise FileNotFoundError("File \"" + file_name + "\" could not be opened. Check file name or file path.")
    if len(data) == 0:
        raise Exception("No data found in given a file!")
    return data

def process_data(data):
    word_count = {}
    for line in data:
        for word in line.split():
            isolated_word = re.sub('[!?@#$\[\]<>%^&*():;]', '', word).lower()
            isolated_word = isolated_word.replace(',', '.') if ',' in isolated_word else isolated_word
            try:
                word_with_numbers_handled = float(isolated_word)
            except ValueError:
                word_with_numbers_handled = re.sub('[,.]', '', isolated_word)
                if word_with_numbers_handled[0] in list_of_characters_to_cut:
                    word_with_numbers_handled = word_with_numbers_handled[1:]
                if word_with_numbers_handled == "":
                    continue
                if word_with_numbers_handled[-1] in list_of_characters_to_cut:
                    word_with_numbers_handled = word_with_numbers_handled[:-1]
            if word_with_numbers_handled in word_count:
                word_count[str(word_with_numbers_handled)] += 1
            else:
                word_count[str(word_with_numbers_handled)] = 1
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    words_list, number_of_word_instances_list = [], []
    for pair in sorted_word_count:
        words_list.append(pair[0])
        number_of_word_instances_list.append(pair[1])
    return words_list, number_of_word_instances_list

def save_to_files(words_list, number_of_word_instances_list):
    with open("words_list.txt", "w", encoding='utf-8') as words_list_file, open("number_of_word_instances_list.txt", "w", encoding='utf-8') as number_of_word_instances_list_file:
        for count in range(len(words_list)):
            words_list_file.write(words_list[count] + '\n')
            number_of_word_instances_list_file.write(str(number_of_word_instances_list[count]) + '\n')

def print_number_of_words_in_given_file():
    print("Number of words in a given file: " + str(len(words_list)))

def plot_zipf(words_list, number_of_word_instances_list):
    for (number, word) in enumerate(words_list):
        words_list[number] = str(number + 1) + ". " + str(word)
    contunue_graph = "y"
    multiply_factor = 1
    plt.figure("Zipf Graph")
    plt.ion()
    plt.show()
    while contunue_graph == "y":
        if start_index + (multiply_factor - 1)*amount_of_words_to_display > len(words_list):
            print("No more words to graph")
            input("To close window, press Enter")
            break
        plt.clf()
        plt.title("Zipf Graph")
        plt.xlabel("Word in given document")
        plt.ylabel("Amount of times the word occurs in the document")
        plt.plot(words_list[start_index + (multiply_factor - 1)*amount_of_words_to_display: start_index + multiply_factor*amount_of_words_to_display], number_of_word_instances_list[start_index + (multiply_factor - 1)*amount_of_words_to_display: start_index + multiply_factor*amount_of_words_to_display], marker= "o")
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.draw()
        contunue_graph = input("Show next " + str(amount_of_words_to_display) + " words? (y/N): ").lower()
        while contunue_graph != "y" and contunue_graph != "n":
            contunue_graph = input("Unknown command. Try again!: ")
        multiply_factor += 1
    print("Closing window")

if __name__ == '__main__':
    data = load_data()
    words_list, number_of_word_instances_list = process_data(data)
    save_to_files(words_list, number_of_word_instances_list)
    print_number_of_words_in_given_file()
    plot_zipf(words_list, number_of_word_instances_list)