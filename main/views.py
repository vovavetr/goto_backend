from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from datetime import datetime
from main.models import Question,Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'main/index.html', context)

def detail(request, question_id):
    q = Question.objects.get(id=question_id)
    context={'question':q}
    return render(request, 'main/detail.html', context)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(question.id,)))
def long_test_form(request):
    if request.method=="POST":
        question_text=request.POST['question_text']
        long_text = request.POST['long']
        q=Question()
        q.long_text=long_text
        q.question_text=question_text
        q.pub_date = datetime.now()
        q.save()
        return HttpResponseRedirect(reverse('detail', args=(q.id,)))
    return render(request, "main/form.html",{})