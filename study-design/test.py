from studyExplainer import Analysis
# from ipynb.fs.full.practical import *
import inspect
from practical import frame_printing_solution

# src='''def frame_printing_solution(slogan: str) -> str:
#     # First, split the words string into a list of strings
#     words = slogan.split(' ')
#     # print(words)

#     # Next, get the length of the longest word in words.
#     longest_word_length = len(max(words, key=len))
#     # print(longest_word_length)

#     # Print out the first border line
#     top_or_bottom_border = "**" + ('*' * longest_word_length) + "**\n"
#     # print(top_or_bottom_border)

#     # Start building answer string, can immediately add the top border
#     answer_string = ""
#     answer_string += top_or_bottom_border

#     # Iterate through each word in the string and add it to the answer string
#     for word in words:
#         if len(word) and word.isalnum():
#             # Construst the string according to the following structure:
#             # '* '
#             # word
#             # ' ' * longest_word_length - len(word)
#             # ' *\n'
#             cont_string = "* "
#             cont_string += word
#             cont_string += " " * (longest_word_length - len(word))
#             cont_string += " *\n"

#             # Add the word string to the answer string
#             answer_string += cont_string

#     # Add the bottom border
#     answer_string += top_or_bottom_border[:len(top_or_bottom_border)-1]

#     return answer_string
# '''

# def frame_printing_solution(slogan: str) -> str:
#     # First, split the words string into a list of strings
#     words = slogan.split(' ')

#     # Next, get the length of the longest word in words.
#     longest_word_length = len(max(words, key=len))

#     # Print out the first border line
#     top_or_bottom_border = "**" + ('*' * longest_word_length) + "**\n"

#     # Start building answer string, can immediately add the top border
#     answer_string = ""
#     answer_string += top_or_bottom_border

#     # Iterate through each word in the string and add it to the answer string
#     for word in words:
#         if len(word) and word.isalnum():
#             # Construst the string according to the following structure:
#             # '* '
#             # word
#             # ' ' * longest_word_length - len(word)
#             # ' *\n'
#             cont_string = "* "
#             cont_string += word
#             cont_string += " " * (longest_word_length - len(word))
#             cont_string += " *\n"

#             # Add the word string to the answer string
#             answer_string += cont_string

#     # Add the bottom border
#     answer_string += top_or_bottom_border[:len(top_or_bottom_border)-1]

#     return answer_string

src = inspect.getsource(frame_printing_solution)

# print(src)
# print("========================")
# src = src.encode('unicode_escape').decode()
# src = src.encode('latin1', 'backslashreplace').decode('unicode_escape')
# print(src)
# print("========================")

# src = src.encode('unicode_escape').decode()
# print(src)
# src = src.replace(r'\n', '')

explainer = Analysis() 
feedback = explainer.get_feedback(src)
print(feedback)