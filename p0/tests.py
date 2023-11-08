import unittest
import grade
import os
import sys

def skiptest(args):
    pass


class TestP0(unittest.TestCase):

    def test_solution(self):
        """
        I think what we will want to do here is set the solution to the 'solution/' dir.

        I also changed grade.main to return the score value.  But the whole script has to run to get the right path...
        """
        # dir = os.path.abspath("solution/")
        # print("Where am I", os.getcwd())
        score1 = grade.main(os.path.abspath("solution/")) # check that this is 0
        # score.txt open
        file = open('solution/score.txt','r')
        # read score
        answer_key = int(file.readline())
        file.close()
        self.assertEqual(score1, answer_key)

    def test_minimum_points(self):
        # dir = os.path.abspath("minimum_points/")
        score = grade.main(os.path.abspath("tests/minimum_points/")) # check that this is 0
        file = open('tests/minimum_points/score.txt','r')
        # read score
        answer_key = int(file.readline())
        file.close()
        self.assertEqual(score, answer_key)

if __name__ == '__main__':
    unittest.main()
