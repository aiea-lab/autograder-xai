
"""
You are writing a program to help design signs for a local community fair. Your program will receive a slogan from each participant and needs to be able to transform the sentence into the desired format so it can be neatly fit onto a sign that follows the fair's specifications.

The fair's specifications are as follows:
* Each sign must have a top and a bottom border.
* Each sign must have exactly one word per line, save for the border lines which must not have any words.
* Each sign must be wide enough for every word to fit properly within its borders, with at least one space on either side of each word.

For example, the slogan "Hello world in a frame" would be displayed as:
*********
* Hello *
* world *
* in    *
* a     *
* frame *
*********

Use the function below to get started.

When you're ready to test, please run: `python grader.py` or `python3 grader.py`, depending on your system.

(for tool group only):
This problem is supported by a tool we've been developing in my lab.

This tool aims to help you figure out a good structure for your solution and help you pinpoint the reason behind certain errors. When you submit your code, some recommendations from the tool will be included in your output.
"""

def frame_printing(slogan: str) -> str:
    # YOUR CODE HERE
    raise NotImplementedError

def frame_printing_solution(slogan: str) -> str:
    # First, split the words string into a list of strings
    words = slogan.split(' ')

    # Next, get the length of the longest word in words.
    longest_word_length = len(max(words, key=len))

    # Print out the first border line
    top_or_bottom_border = "**" + ('*' * longest_word_length) + "**\n"

    # Start building answer string, can immediately add the top border
    answer_string = ""
    answer_string += top_or_bottom_border

    # Iterate through each word in the string and add it to the answer string
    for word in words:
        if len(word) and word.isalnum():
            # Construst the string according to the following structure:
            # '* '
            # word
            # ' ' * longest_word_length - len(word)
            # ' *\n'
            cont_string = "* "
            cont_string += word
            cont_string += " " * (longest_word_length - len(word))
            cont_string += " *\n"

            # Add the word string to the answer string
            answer_string += cont_string

    # Add the bottom border
    answer_string += top_or_bottom_border[:len(top_or_bottom_border)-1]

    return answer_string