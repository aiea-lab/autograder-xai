import sys
import inspect

# from ipynb.fs.full.practical import frame_printing
from ipynb.fs.full.practical import frame_printing, frame_printing_solution

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
        """ Takes in student src code and matches it against the expected ruleset."""
        student_src = inspect.getsource(frame_printing)

        print(f"\n\n=====================\n{student_src}\n=====================\n\n")

        # student_src = inspect.getsource(frame_printing)

        """ Provides structural feedback only if test cases fail. """
        # If all test cases pass, no need for structural feedback
        case_results = [
            self.test(case1_str, case1_sol),
            self.test(case2_str, case2_sol),
            self.test(case3_str, case3_sol)
        ]

        if all("correct answer" in result for result in case_results):
            return "\n- No structural issues detected. Function works correctly!"

        # If cases fail, analyze the student's function
        feedback = "\n== Structural Feedback =="

        if "split" not in student_src:
            feedback += "\n- The function should split the input string into words."

        if "max" not in student_src or "key=len" not in student_src:
            feedback += "\n- The function should determine the longest word length using max(..., key=len)."

        if "*" not in student_src:
            feedback += "\n- The function should generate a border using '*' characters."

        if "for" not in student_src:
            feedback += "\n- A loop is needed to iterate through words and format them correctly."

        return feedback if feedback != "\n== Structural Feedback ==" else "\n- Code structure looks good!"


        # need to hook in the main explanation stuff here too
        # probably worth partially rewriting too, since it's gotten pretty messy.
        # update or make a new 'explainer.py' file to be included just for this exercise.
        # return "\n== structural feedback dummy str"


def main():
    g = Grader()

    global case1_str, case1_sol, case2_str, case2_sol, case3_str, case3_sol

    case1_str = "Hello World in a Frame"
    case1_sol = """*********\n* Hello *\n* World *\n* in    *\n* a     *\n* Frame *\n*********"""

    case2_str = "Hello   World   Spaced   Frame"
    case2_sol = """**********\n* Hello  *\n* World  *\n* Spaced *\n* Frame  *\n**********"""

    case3_str = "A Few Words Here \n And There Work Things Out"
    case3_sol = """**********\n* A      *\n* Few    *\n* Words  *\n* Here   *\n* And    *\n* There  *\n* Work   *\n* Things *\n* Out    *\n**********"""


    incorrect_cases = [
        # Missing Border
        ("Hello Frame", "Hello  \nFrame  "),
        
        # Wrong Padding (Spacing Issue)
        ("Wide Frame", "********\n* Wide *\n*Frame *\n********"),

        # Extra Newline at the End
        ("Extra Line", "********\n* Extra *\n* Line  *\n********\n"),

        # Case Sensitivity Mistake
        ("Hello World", "**********\n* hello  *\n* world  *\n**********"),

        # Incorrect Border Length
        ("Frame Test", "*******\n* Frame *\n* Test *\n*******"),

        # Words Not on Separate Lines
        ("Hello World Frame", "***************\n* Hello World Frame *\n***************")
    ]

    # Run correct test cases
    print(g.test(case1_str, case1_sol))
    print(g.test(case2_str, case2_sol))
    print(g.test(case3_str, case3_sol))

    # Run incorrect test cases

    print("\n\n")
    for i, (case_input, expected_output) in enumerate(incorrect_cases, start=4):
        print( f"{g.test(case_input, expected_output)}\n" )

    # Run structural analysis only if needed
    print(g.structural_exp())

if (__name__ == '__main__'):
    sys.exit(main())

