import sys
import inspect

# from ipynb.fs.full.practical import frame_printing
from ipynb.fs.full.practical import *

class Grader():
    def __init__(self):
        self.c = 0
    """
    Do the basic test cases.
    """
    def test(self, case_str, case_sol):
        """ Given student code, test and return answer """
        self.c += 1
        case_ans = frame_printing_solution(case_str)
        # case_ans = frame_printing_solution(case_str)

        ret_str = f"== Case {self.c}: "
        if case_ans == case_sol:
            # Nothing more to be said, answer was correct.
            return ret_str + "correct answer"
        else:
            ret_str += "incorrect answer"

            # Offer only error-based explanation here
            feedback_str = self.error_based_feedback(case_ans, case_sol)
            return ret_str + feedback_str
    
    def error_based_feedback(self, case_ans, case_sol):
        """ Given student answer, return targeted feedback. """
        feedback = ""
        case_ans_lines = case_ans.split("\n")
        case_sol_lines = case_sol.split("\n")

        if len(case_ans_lines) != len(case_sol_lines):
            feedback += f"\n- Incorrect number of lines (Expected {len(case_sol_lines)}, got {len(case_ans_lines)})"

        for i, (ans_line, sol_line) in enumerate(zip(case_ans_lines, case_sol_lines)):
            if len(ans_line) != len(sol_line):
                feedback += f"\n- Line {i+1} has incorrect length (Expected {len(sol_line)}, got {len(ans_line)})"
            elif ans_line != sol_line:
                feedback += f"\n- Line {i+1} has incorrect characters: Expected '{sol_line}', got '{ans_line}'"

        if case_ans.endswith("\n") and not case_sol.endswith("\n"):
            feedback += "\n- Extra newline at the end of output"
        
        if "*" not in case_ans:
            feedback += "\n- Missing asterisks in the frame"
        
        return feedback if feedback else "\n- Output format incorrect, but specific issue not identified"
        

    def structural_exp(self):
        """ Analyzes student function structure manually. """
        student_src = inspect.getsource(frame_printing)
        
        feedback = "\n== Structural Feedback ==\n"
        if "split" not in student_src:
            feedback += "- Missing string splitting (words should be extracted from the input).\n"
        
        if "max(" not in student_src:
            feedback += "- Longest word calculation is incorrect or missing.\n"
        
        if "for" not in student_src:
            feedback += "- Loop structure is missing (words must be processed individually).\n"
        
        if "*" not in student_src:
            feedback += "- Border creation is missing or incorrect.\n"
        
        if feedback == "\n== Structural Feedback ==\n":
            feedback += "No structural issues detected.\n"
        
        return feedback


# def main():
#     g = Grader()

#     # Check answers and offer error-based exp
#     case1_str = "Hello World in a Frame"
#     case1_sol = """*********\n* Hello *\n* World *\n* in    *\n* a     *\n* Frame *\n*********"""
#     print(g.test(case1_str, case1_sol))
    
#     case2_str = "Hello   World   Spaced   Frame"
#     case2_sol = """**********\n* Hello  *\n* World  *\n* Spaced *\n* Frame  *\n**********"""
#     print(g.test(case2_str, case2_sol))
    
#     case3_str = "A Few Words Here \n And There Work Things Out"
#     case3_sol = """**********\n* A      *\n* Few    *\n* Words  *\n* Here   *\n* And    *\n* There  *\n* Work   *\n* Things *\n* Out    *\n**********"""  
#     print(g.test(case3_str, case3_sol))
    
#     # Check answers and offer error-based exp
#     case1_str = "Hello World in a Frame"
#     case1_sol = """*********
# * Hello *
# * World *
# * in    *
# * a     *
# * Frame *
# *********"""
#     print(g.test(case1_str, case1_sol))
    
#     case2_str = "Hello   World   Spaced   Frame"
#     case2_sol = """**********
# * Hello  *
# * World  *
# * Spaced *
# * Frame  *
# **********"""
#     print(g.test(case2_str, case2_sol))
    
#     case3_str = "A Few Words Here \n And There Work Things Out"
#     case3_sol = """**********
# * A      *
# * Few    *
# * Words  *
# * Here   *
# * And    *
# * There  *
# * Work   *
# * Things *
# * Out    *
# **********"""  
#     print(g.test(case3_str, case3_sol))

#     # Offer structural exp
#     structural_feedback_str = g.structural_exp()
#     print(structural_feedback_str)



#     # Offer structural exp
#     structural_feedback_str = g.structural_exp()
#     print(structural_feedback_str)


def main():
    g = Grader()

    test_cases = [
        # Basic test case with normal words
        ("Hello World in a Frame", 
        """*********
* Hello *
* World *
* in    *
* a     *
* Frame *
*********"""),
        
        # Words with extra spaces in between (should still be framed correctly)
        ("Hello   World   Spaced   Frame", 
        """**********
* Hello  *
* World  *
* Spaced *
* Frame  *
**********"""),
        
        # Words split across multiple lines
        ("A Few Words Here \n And There Work Things Out", 
        """**********
* A      *
* Few    *
* Words  *
* Here   *
* And    *
* There  *
* Work   *
* Things *
* Out    *
**********"""),

        
        # Single word input should still be framed
        ("Hello", 
        """*******
* Hello *
*******"""),

        # Single-character words should be framed correctly
        ("A B C D", 
        """*****
* A *
* B *
* C *
* D *
*****"""),

        # Words with inconsistent spacing (should ignore extra spaces)
        ("Hello   World  Again", 
        """*********
* Hello  *
* World  *
* Again  *
*********"""),

        # Input contains punctuation marks (should be framed like words)
        ("Hello, World!", 
        """***********
* Hello,  *
* World!  *
***********"""),

        # Numbers should be framed correctly
        ("123 4567 89", 
        """********
* 123  *
* 4567 *
* 89   *
********"""),

        # Longest word in the middle, checking border size calculation
        ("Short Midway Extraordinarily Long", 
        """******************
* Short         *
* Midway        *
* Extraordinarily *
* Long          *
******************"""),

        # Multi-line input (should frame each word separately)
        ("Line1\nLine2 Line3\nLine4", 
        """********
* Line1 *
* Line2 *
* Line3 *
* Line4 *
********"""),

        # Edge Case: Empty string input (should return only the border)
        ("", 
        """**
**"""),

        # Edge Case: Single space input (should return only the border)
        (" ", 
        """**
**"""),

        # Edge Case: Extremely long single word (should not break)
        ("Supercalifragilisticexpialidocious", 
        """**************************************
* Supercalifragilisticexpialidocious *
**************************************"""),

        # Special characters should be framed correctly like words
        ("! @ # $ % ^ & *", 
        """*******
* ! *
* @ *
* # *
* $ *
* % *
* ^ *
* & *
* * *
*******""")
    ]


    for i, (case_str, case_sol) in enumerate(test_cases, 1):
        # print(f"== Running Test Case {i}: {case_str[:30]} ==")
        print(f"\n== Running Test Case {i}: ")
        print(f"\t{g.test(case_str, case_sol)}")


    structural_feedback_str = g.structural_exp()
    print(f"\t{structural_feedback_str}")



if (__name__ == '__main__'):
    sys.exit(main())

