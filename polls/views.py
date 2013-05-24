from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404

from django.core.urlresolvers import reverse

from models import Poll, Institution

from forms import DetailForm

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.question_set.all()
    form = DetailForm(questions=questions)
    return render(request, 'polls/detail.html',
                  {
                      'poll': poll,
                      'form': form,
                  })

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})    

def sign(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    institution_list = Institution.objects.all().order_by('name')
    return render(request, 'polls/sign.html',
                  {
                      'poll': poll,
                      'institution_list': institution_list
                  })
        
def answer(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.question_set.all()
    if request.method == 'POST':
        form = DetailForm(request.POST, questions=questions)
        if form.is_valid():
            for a in form.answers():
                print a
            return HttpResponseRedirect(reverse('polls:sign',
                                                args=(poll.id,)))
    else:
        form = ContactForm()
    return render(request, 'polls/detail.html',
                  {
                      'poll': poll,
                      'form': form,
                  })


