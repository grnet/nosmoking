from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect

from django.core.urlresolvers import reverse

from models import Poll, Institution, Participant, Response, Sign

from forms import DetailForm

SHOW_SIGNATURES_COUNT_LIMIT = 100

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id, user_uuid):
    poll = get_object_or_404(Poll, pk=poll_id)
    participant = get_object_or_404(Participant, unique_id=user_uuid)
    if participant.completed:
        return redirect(reverse('polls:thanks',
                                args=(poll.id,
                                      user_uuid,)))     
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
    if participant.completed:
        return redirect(reverse('polls:thanks',
                                args=(poll.id,
                                      user_uuid,)))     
    institution_list = Institution.objects.all().order_by('name')
    if request.method == 'POST':
        participant.completed = True
        to_delete = Sign.objects.filter(participant=participant)
        to_delete.delete()        
        sign = Sign()
        sign.participant = participant
        if 'first-name' in request.POST:
            sign.first_name = request.POST['first-name']
        if 'last-name' in request.POST:
            sign.last_name = request.POST['last-name']
        if 'sign-agree' in request.POST:
            sign.agree = True
        if 'sign-disagree' in request.POST:
            sign.agree = False
        if 'sign-no-opinion' in request.POST:
            sign.agree = None
        if 'institution-id' in request.POST:
            institution_id = request.POST['institution-id']
            institution = get_object_or_404(Institution,
                                            pk=institution_id)
            sign.institution = institution
        sign.save()
        participant.save()
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
    signature_count = Sign.objects.all().count()
    participant_count =  Participant.objects.all().count()
    show_signature_count = ((participant_count / signature_count)
                            > SHOW_SIGNATURES_COUNT_LIMIT)
    return render(request, 'polls/thanks.html',                  
                  {
                      'show_signature_count': show_signature_count,
                      'signature_count': signature_count,
                  })

def answer(request, poll_id, user_uuid):
    poll = get_object_or_404(Poll, pk=poll_id)
    participant = get_object_or_404(Participant, unique_id=user_uuid)
    if participant.completed:
        return redirect(reverse('polls:thanks',
                                args=(poll.id,
                                      user_uuid,))) 
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


