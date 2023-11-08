#!/usr/bin/env python3

import math
import os
import shutil
import sys
import importlib

from cse40.style import Style
# import ^ and then replace the flake8 commands, with Style() from above. 
from cse40.assignment import Assignment
from cse40.question import Question

from explain import Explainer
explainer = Explainer("CSE 140", "PA1")

class Q1(Question):
    """
    Buy several fruit normally.
    """

    def score_question(self, submission):
        cost = buyLotsOfFruit.buyLotsOfFruit([
            ('apples', 2.0),
            ('pears', 3.0),
            ('limes', 4.0)
        ])

        if (not math.isclose(cost, 12.25)):
            feedback = explainer.get_feedback("some_info", default = "buyLotsOfFruit gave %s, which is not 12.25" % str(cost))
            self.fail(feedback)
            return

        self.full_credit()

class Q2(Question):
    """
    Shop smart.
    """

    def score_question(self, submission):
        shop1 = shop.FruitShop('shop1', {
            'apples': 2.0,
            'oranges': 1.0
        })

        shop2 = shop.FruitShop('shop2', {
            'apples': 1.0,
            'oranges': 5.0
        })

        shops = [shop1, shop2]

        order1 = [('apples', 1.0), ('oranges', 3.0)]
        ans1 = shopSmart.shopSmart(order1, shops)

        order2 = [('apples', 3.0)]
        ans2 = shopSmart.shopSmart(order2, shops)

        if (ans1 != shop1):
            feedback1 = explainer.get_feedback("some_info", default = "shopSmart.shopSmart([('apples', 1.0), ('oranges', 3.0)], shops)') returned %s" % str(ans1))
            self.fail(feedback1)
            return

        if (ans2 != shop2):
            feedback2 = explainer.get_feedback("some_info", default = "shopSmart.shopSmart([('apples', 3.0)], shops)') returned %s" % str(ans2))
            self.fail(feedback2)
            return

        self.full_credit()

def prepare_submission(submission_dir):
    # Add the student's submission directory so import will go correctly.
    sys.path.insert(0, submission_dir)
    
    global buyLotsOfFruit
    global shop
    global shopSmart

    import buyLotsOfFruit
    import shop
    import shopSmart

    # Reloads the global modules when grade.py is run multiple times in tests.py.
    # importlib can only reload if a module is already defined, so the first import
    # will import the modules (but not really. the previous global modules haven't gotten
    # overwritten yet), then it'll get reloaded (this will clear the global module), then
    # the new modules will get imported.
    importlib.reload(buyLotsOfFruit)
    importlib.reload(shopSmart)

    import buyLotsOfFruit
    import shop
    import shopSmart


def main(submission_dir):
    """
    This will also return the score for unit testing (for now).
    """
    print(submission_dir)
    prepare_submission(submission_dir)

    questions = [
        Q1("Q1", 1),
        Q2("Q2", 1),
        # TODO(eriq): Make this work for a directory.
        Style(os.path.join(submission_dir, "shopSmart.py"), max_points = 0),
    ]

    assignment = Assignment('Project 0: Tutorial', questions)
    score = assignment.grade(None)
    print(assignment.report())
    return score

def _load_args(args):
    executable = args.pop(0)
    if (len(args) != 1 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s <submission dir>" % (executable), file = sys.stderr)
        sys.exit(1)

    submission_dir = os.path.abspath(args.pop(0))

    return submission_dir

if (__name__ == '__main__'):
    main(_load_args(sys.argv))
