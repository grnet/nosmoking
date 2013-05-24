from django import forms
from django.forms.widgets import RadioSelect

class DetailForm(forms.Form):

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(DetailForm, self).__init__(*args, **kwargs)
         
        for i, question in enumerate(questions):
            question_label = question.question_text
            question_choices = [(c.id, c.choice_text)
                                for c in question.choice_set.all()]
            self.fields['question_%s' % i] = forms.ChoiceField(
                label=question_label,
                choices=question_choices,
                widget=RadioSelect)

    def answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('question_'):
                yield (value)
