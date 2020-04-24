from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        context = {'question': question}
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    # Could also use: `question = get_object_or_404(Question, pk=question_id)`
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is a dictionary-like object that lets you access submitted data by key name.
        # In this case, request.POST['choice'] returns the ID of the selected choice, as a string.
        # request.POST values are always strings.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data. The code checks for
        # KeyError and re-displays the question form with an error message if choice isn’t given.
        return render(request, 'polls.detail.html',
                      {'question': question, 'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()

    # Always return HttpResponseRedirect after successfully dealing with POST data. This prevents data from being
    # posted twice if a user hits back button again.
    return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))
    # HttpResponseRedirect takes a single argument: the URL to which the user will be redirected.
    # We are using the reverse() function in the HttpResponseRedirect constructor. This function helps avoid having to
    # hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the
    # variable portion of the URL pattern that points to that view. In this case, '/polls/3/results/'. This redirected
    # URL will then call the 'results' view to display the final page.

