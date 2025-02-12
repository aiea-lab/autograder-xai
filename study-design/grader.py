import sys
import inspect
from studyExplainer import Analysis
import datetime

from practical import frame_printing, frame_printing_solution

STUDENT_FUNCTION = frame_printing
# STUDENT_FUNCTION = frame_printing_solution

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
            return ret_str + "correct answer"
        else:
            self.log_message += f"{self.case_number}-FAIL|"
            # Offer only error-based explanation here
            ret_str += "incorrect answer"
            feedback_str = self.error_based_feedback(case_ans)
            return ret_str + feedback_str
    
    def error_based_feedback(self, case_ans):
        """ Given student answer, return targeted feedback. """

        """
        ## my notes:
        check cases:
        * can tell them how to do newlines if not the expected number of newlines in the output
        * if any lines have different lengths, point that out
        * no empty lines are allowed
        * if there are some asterisks but not the proper amount on any given line, then can hint to them about how to calc it
        * give them weird stuff like punctuation or extra newlines in the input to mess them up?
        * make sure not to add an extra newline to the very last line, check for that
        * when they get a case wrong, show it to them.
        """

        return "\nError-based feedback dummy str"
        

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

    # Check answers and offer error-based exp
    case1_str = "Hello World in a Frame"
    case1_sol = """*********\n* Hello *\n* World *\n* in    *\n* a     *\n* Frame *\n*********"""
    print(g.test(case1_str, case1_sol))

    case2_str = "Fresh Apples For Sale"
    case2_sol = """**********\n* Fresh  *\n* Apples *\n* For    *\n* Sale   *\n**********"""
    print(g.test(case2_str, case2_sol))
    
    case3_str = "Hello   World   Spaced   Frame"
    case3_sol = """**********\n* Hello  *\n* World  *\n* Spaced *\n* Frame  *\n**********"""
    print(g.test(case3_str, case3_sol))
    
    case4_str = "A Few Words Here \n And There Work Things Out"
    case4_sol = """**********\n* A      *\n* Few    *\n* Words  *\n* Here   *\n* And    *\n* There  *\n* Work   *\n* Things *\n* Out    *\n**********"""  
    print(g.test(case4_str, case4_sol))

    # Write result
    g.log_result()
    g.clear_log_message()
    
    # Offer structural exp
    structural_feedback_str = g.structural_exp()
    print(structural_feedback_str)


if (__name__ == '__main__'):
    sys.exit(main())