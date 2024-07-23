from django import forms
from .models import QuizModel,QuestionModel,ChoiceModel

class QuizForm(forms.ModelForm):
    class Meta:
        model = QuizModel
        fields = ['quiz_picture','title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ['text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = ChoiceModel
        fields = ['text','is_correct']
