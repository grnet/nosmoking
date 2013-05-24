from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404

from django.core.urlresolvers import reverse

from models import Poll, Institution, Participant, Response

from forms import DetailForm

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id, user_uuid):
    poll = get_object_or_404(Poll, pk=poll_id)
    participant = get_object_or_404(Participant, unique_id=user_uuid)
    questions = poll.question_set.all()
    form = DetailForm(questions=questions)
    return render(request, 'polls/detail.html',
                  {
                      'poll': poll,
                      'user_uuid': user_uuid,
                      'form': form,
                  })

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})    

def sign(request, poll_id, user_uuid):
    poll = get_object_or_404(Poll, pk=poll_id)
    participant = get_object_or_404(Participant, unique_id=user_uuid)    
    institution_list = Institution.objects.all().order_by('name')
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('polls:thanks',
                                            args=(poll.id,
                                                  user_uuid,)))
    return render(request, 'polls/sign.html',
                  {                      
                      'poll': poll,
                      'user_uuid': user_uuid,
                      'institution_list': institution_list,
                  })

def thanks(request, poll_id, user_uuid):
    participant = get_object_or_404(Participant, unique_id=user_uuid)        
    return render(request, 'polls/thanks.html')
    
def answer(request, poll_id, user_uuid):
    poll = get_object_or_404(Poll, pk=poll_id)
    participant = get_object_or_404(Participant, unique_id=user_uuid)    
    questions = poll.question_set.all()
    if request.method == 'POST':
        form = DetailForm(request.POST, questions=questions)
        if form.is_valid():
            to_delete = Response.objects.filter(participant=participant)
            to_delete.delete()
            for choice_id in form.answers():
                response = Response(participant=participant,
                                    choice_id=choice_id)
                response.save()
            return HttpResponseRedirect(reverse('polls:sign',
                                                args=(poll.id,
                                                      user_uuid,)))
    else:
        form = DetailForm(questions=questions)
    return render(request, 'polls/detail.html',
                  {
                      'poll': poll,
                      'form': form,
                      'user_uuid': user_uuid,
                  })


