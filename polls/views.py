from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice
from django.template import loader
from django.urls import reverse
from django.utils import timezone
# Create your views here.
def IndexView(request): #display the latest 5 questions posted on the website, display is hardcoded in the view
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    template=loader.get_template('polls/index.html')
    context={
        'latest_question_list':latest_question_list,
    }
    return HttpResponse(template.render(context,request))

def detail(request, question_id):
    try:
        question=Question.objects.filter(pub_date__lte=timezone.now()).get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist or has not been published yet')
    return render(request,'polls/detail.html',{'question':question})


def options(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))

def results(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request,'polls/results.html',{'question':question})
