import sys
import inspect
from studyExplainer import Analysis
import datetime

from practical import frame_printing

STUDENT_FUNCTION = frame_printing

TEST_CASES = [
        # Case 1: Basic test case with normal words
        ("Hello World in a Frame", 
"""*********
* Hello *
* World *
* in    *
* a     *
* Frame *
*********"""),
        
        # Case 2: Words with extra spaces in between (should still be framed correctly)
        ("Hello   World   Spaced   Frame", 
"""**********
* Hello  *
* World  *
* Spaced *
* Frame  *
**********"""),
        
        # Case 3: Remove words with special characters like '?' and '!'
        ("Extra? Extra! Come Read All About It", 
"""*********
* Come  *
* Read  *
* All   *
* About *
* It    *
*********"""),

        
        # Case 4: Edge Case: Extremely long single word (should not break)
        ("Supercalifragilisticexpialidocious", 
"""**************************************
* Supercalifragilisticexpialidocious *
**************************************"""),

        # Case 5: Numbers should be framed correctly
        ("Call 555 8675 309", 
"""********
* Call *
* 555  *
* 8675 *
* 309  *
********"""),

        # Case 6: Longest word in the middle, checking border size calculation
        ("Short Midway Extraordinarily Long", 
"""*******************
* Short           *
* Midway          *
* Extraordinarily *
* Long            *
*******************"""),

    ]

class Grader():
    def __init__(self):
        self.case_number = 0
        self.log_message = ""
    """
    Do the basic test cases.
    """
    def test(self, case_str, case_sol):
        """ Given student code, test and return answer """
        try:
            self.case_number += 1
            case_ans = STUDENT_FUNCTION(case_str)
        except:
            case_ans = "Failed, implementation error."

        ret_str = f"== Case {self.case_number}: "
        if case_ans == case_sol:
            # Nothing more to be said, answer was correct.
            self.log_message += f"{self.case_number}-PASS|"
            return ret_str + "PASS"
        else:
            self.log_message += f"{self.case_number}-FAIL|"
            # Offer only error-based explanation here
            ret_str += "FAIL"
            feedback_str = self.error_based_feedback(case_ans, case_sol)
            return ret_str + feedback_str
    
    def error_based_feedback(self, case_ans, case_sol):
        """ Given student answer, return targeted feedback. """
        feedback = ""
        case_ans_lines = case_ans.split("\n")
        case_sol_lines = case_sol.split("\n")

        if len(case_ans_lines) != len(case_sol_lines):
            feedback += f"\n\t- Incorrect number of lines (Expected {len(case_sol_lines)}, got {len(case_ans_lines)})"

        for i, (ans_line, sol_line) in enumerate(zip(case_ans_lines, case_sol_lines)):
            # if len(ans_line) != len(sol_line):
            #     feedback += f"\n\t- Line {i+1} has incorrect length (Expected {len(sol_line)}, got {len(ans_line)})"
            if ans_line != sol_line:
                feedback += f"\n\t- Line {i+1} has incorrect characters: Expected '{sol_line}', got '{ans_line}'"

        if case_ans.endswith("\n") and not case_sol.endswith("\n"):
            feedback += "\n\t- Extra newline at the end of output"
        
        if "*" not in case_ans:
            feedback += "\n\t- Missing asterisks in the frame"
        
        return feedback if feedback else "\n\t- Output format incorrect, but specific issue not identified"
        
    def structural_exp(self):
        """ Takes in student src code and matches it against the expected ruleset."""
        student_src = inspect.getsource(STUDENT_FUNCTION)
        exp = Analysis()
        feedback = exp.get_feedback(student_src)
        return feedback

    def log_result(self):
        """Logs the result of the submission to a text file 'log.txt' in the local directory."""
        with open("log.txt", "a") as log:
            log.write(f"{self.log_message}\n")
        
    def clear_log_message(self):
        self.log_message = ""
    
    def timestamp(self):
        # Record timestamp on log
        now = datetime.datetime.now()
        self.log_message = f"{now.strftime('%H %M %S')}: "

def main():
    g = Grader()
    g.timestamp()

    for i, (case_str, case_sol) in enumerate(TEST_CASES, 1):
        ans = g.test(case_str, case_sol)
        print(ans)
        if "FAIL" in ans:
            print(f"  ({len(TEST_CASES)-i} test cases remaining.)")
            break

    g.log_result()
    g.clear_log_message()

    structural_feedback_str = g.structural_exp()
    print(f"\t{structural_feedback_str}")


if (__name__ == '__main__'):
    sys.exit(main())

