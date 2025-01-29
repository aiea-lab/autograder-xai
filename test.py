from explainer import Analysis

src='''def frame_printing_solution(slogan: str) -> str:
    # First, split the words string into a list of strings
    words = slogan.split(' ')
    # print(words)

    # Next, get the length of the longest word in words.
    longest_word_length = len(max(words, key=len))
    # print(longest_word_length)

    # Print out the first border line
    top_or_bottom_border = "**" + ("*") + "**"
    # print(top_or_bottom_border)

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
            # ' *'
            cont_string = "* "
            cont_string += word
            cont_string += " " * (longest_word_length - len(word))
            cont_string += " *"

            # Add the word string to the answer string
            answer_string += cont_string

    # Add the bottom border
    answer_string += top_or_bottom_border[:len(top_or_bottom_border)-1]

    return answer_string'''
explainer = Analysis() 
feedback = explainer.get_feedback('study', src)
print(feedback)