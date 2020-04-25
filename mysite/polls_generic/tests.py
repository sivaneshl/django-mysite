from django.test import TestCase
from polls import tests


class QuestionModelTests(tests.QuesionModelTests):
    super(tests.QuesionModelTests)


class QuestionIndexViewTests(tests.QuestionIndexViewTests):
    super(tests.QuestionIndexViewTests)


class QuestionDetailViewTests(tests.QuestionDetailViewTests):
    super(tests.QuestionDetailViewTests)

# To test the coverage of tests
# coverage run --source='.' manage.py test myapp
# coverage report

