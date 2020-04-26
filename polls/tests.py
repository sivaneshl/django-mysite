import sys
from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse, resolve
from .models import Question, Choice


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the number of `days`
    offset to now (negative for questions published in the past, positive for questions
    that are yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuesionModelTests(TestCase):

    def test_was_published_recenly_with_future_question(self):
        """
        was_published_recently returns False for all questions
        whose pub_date is in the future
        """
        future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently returns True for all questions
        whose pub_date is within last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        app_name = self.__module__.split('.')[0]
        response = self.client.get(reverse(app_name+':index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        Questions with pub_date in the past are displayed in the page
        """
        create_question(question_text='Past question.', days=-30)
        # get the app name dynamically to toggle between `polls` and `polls_generic` without hardcoding
        app_name = self.__module__.split('.')[0]
        # might as well use `polls:index` or `polls_generic:index`
        response = self.client.get(reverse(app_name + ':index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_questions(self):
        """
        Questions with pub_date in the future are not displayed in the page
        """
        create_question(question_text='Future Question.', days=30)
        app_name = self.__module__.split('.')[0]
        response = self.client.get(reverse(app_name + ':index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past questions and future questions exist, only the past questions are displayed
        """
        create_question(question_text='Future Question.', days=30)
        create_question(question_text='Past Question.', days=-30)
        app_name = self.__module__.split('.')[0]
        response = self.client.get(reverse(app_name + ':index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])

    def test_two_past_questions(self):
        """
        The question index page should display multiple questions
        """
        create_question(question_text='Past Question 1.', days=-10)
        create_question(question_text='Past Question 2.', days=-20)
        app_name = self.__module__.split('.')[0]
        response = self.client.get(reverse(app_name + ':index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past Question 1.>', '<Question: Past Question 2.>'])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with pub_date in future returns a 404 not found error
        """
        future_question = create_question(question_text='Future Question.', days=30)
        app_name = self.__module__.split('.')[0]
        url = reverse(app_name+':detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with pub_date in the past displays the question text
        """
        past_question = create_question(question_text='Past Question.', days=-10)
        app_name = self.__module__.split('.')[0]
        url = reverse(app_name+':detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
