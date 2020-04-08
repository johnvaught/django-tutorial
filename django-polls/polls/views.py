from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from hashids import Hashids
from .models import Question, Choice, get_pk_from_hashid


def index(request):
    latest_questions_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_question_list': latest_questions_list})


def detail(request, question_hashid):
    question = Question.objects.filter(pub_date__lte=timezone.now(), pk=get_pk_from_hashid(question_hashid)).first()
    if question:
        return render(request, 'polls/detail.html', {'question': question})
    else:
        raise Http404("Poll does not exist.")


def results(request, question_hashid):
    question = Question.objects.filter(pub_date__lte=timezone.now(), pk=get_pk_from_hashid(question_hashid)).first()
    if question:
        return render(request, 'polls/results.html', {'question': question})
    else:
        raise Http404("Poll does not exist.")


def vote(request, question_hashid):
    print(request.POST)
    question = get_object_or_404(Question, pk=get_pk_from_hashid(question_hashid))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "Please select a choice."})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data.  This prevents data from being posted twice if a
        # user hits the Back (do they mean refresh?) button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.get_hashid_from_pk(),)))


"""
Class based views.
"""
# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """ Return the last five published question. """
#         return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
