
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.db.models import F
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list":latest_question_list
    } 
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # try: 
        # question = Question.objects.get(pk=question_id) 
    # except Question.DoesNotExist:
        # raise Http404("Question doesn't exist")
    
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", { "question": question })


def results(request, question_id):
    toString= str(question_id)
    question = get_object_or_404(Question, pk=question_id)
    print(question.question_text)
    return render(request,"polls/results.html", {"question":question})



def vote(request, question_id):
   # traer la pregunta
   # hacer un trair + raise
   # traer la eleccion elegida POST["choice"] 

   question = get_object_or_404(Question, pk=question_id)
   try:
    selected_choice = question.choice_set.get(pk=request.POST["choice"])
   except (KeyError, Choice.DoesNotExist):
       return render(request, "polls/detail.html", {
           "question": question,
           "error_message": "you didn´t select a choice"
       })
   else:
       selected_choice.votes = F("votes") + 1
       selected_choice.save()       
       return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
    