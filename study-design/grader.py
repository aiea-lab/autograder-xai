import sys

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
        case_ans = frame_printing(case_str)
        # case_ans = frame_printing_solution(case_str)

        ret_str = f"== Case {self.c}: "
        if case_ans == case_sol:
            # Nothing more to be said, answer was correct.
            return ret_str + "correct answer"
        else:
            # Ping explanation stuff.
            ret_str =+ "incorrect answer"

            feedback_str = self.feedback(case_ans)
    
    def feedback(self, case_ans):
        """ Given student answer, return targeted feedback. """

        """
        ## my notes:
        check cases:
        * can tell them how to do newlines if not the expected number of newlines in the output
        * if any lines have different lengths, point that out
        * no empty lines
        * if not the proper length of asterisks on any given line, then can hint to them about how to calc it
        * give them weird stuff like punctuation or extra newlines in the input to mess them up?
        * make sure not to add an extra newline to the very last line
        * when they get a case wrong, we should tell them what it was
        """

        # also need to hook in the main explanation stuff here too
        # just copy it in here


def main():
    g = Grader()

    case1_str = "Hello World in a Frame"
    case1_sol = """*********\n* Hello *\n* World *\n* in    *\n* a     *\n* Frame *\n*********"""
    print(g.test(case1_str, case1_sol))
    
    case2_str = "Hello   World   Spaced   Frame"
    case2_sol = """**********\n* Hello  *\n* World  *\n* Spaced *\n* Frame  *\n**********"""
    print(g.test(case2_str, case2_sol))
    
    case3_str = "A Few Words Here \n And There Work Things Out"
    case3_sol = """**********\n* A      *\n* Few    *\n* Words  *\n* Here   *\n* And    *\n* There  *\n* Work   *\n* Things *\n* Out    *\n**********"""  
    print(g.test(case3_str, case3_sol))

if (__name__ == '__main__'):
    sys.exit(main())