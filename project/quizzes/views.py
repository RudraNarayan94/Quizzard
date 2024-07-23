from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import QuizModel, QuestionModel, ChoiceModel,ParticipationModel
from .forms import QuizForm, QuestionForm, ChoiceForm

# Create your views here.
@login_required
def create_quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quizzes/create_quiz.html', {'form': form})


def add_question_view(request, quiz_id):
    quiz = get_object_or_404(QuizModel, id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_choices', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'quizzes/add_question.html', {'quiz': quiz, 'form': form})


def add_choices_view(request, question_id):
    question = get_object_or_404(QuestionModel, id=question_id)
    ChoiceFormSet = modelformset_factory(ChoiceModel, form=ChoiceForm, extra=3)

    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST)
        if formset.is_valid():
            choices = formset.save(commit=False)
            for choice in choices:
                choice.question = question
                choice.save()
            if 'add_question' in request.POST:
                return redirect('add_question', quiz_id=question.quiz.id)
            else:
                question.quiz.no_of_questions = question.quiz.questions.count()
                question.quiz.save()
                return redirect('quiz_detail', quiz_id=question.quiz.id)
    else:
        formset = ChoiceFormSet(queryset=ChoiceModel.objects.none())
    return render(request, 'quizzes/add_choices.html', {'question': question, 'formset': formset})

def quiz_detail_view(request, quiz_id):
    quiz = get_object_or_404(QuizModel, id=quiz_id)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})


@login_required
def participate_in_quiz_view(request, quiz_id):
    quiz = get_object_or_404(QuizModel, id=quiz_id)
    if request.method == 'POST':
        score = 0
        for question in quiz.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                choice = ChoiceModel.objects.get(id=selected_choice_id) 
                if choice.is_correct:
                    score += 1 
        ParticipationModel.objects.create(user=request.user, quiz=quiz, score=score) 
        return redirect('quiz_result', quiz_id=quiz.id) 
    return render(request, 'quizzes/participate.html', {'quiz': quiz})

def quiz_result_view(request, quiz_id):
    quiz = get_object_or_404(QuizModel, id=quiz_id)
    participation = ParticipationModel.objects.filter(user=request.user, quiz=quiz).first() 

    leaderboard = ParticipationModel.objects.filter(quiz=quiz).order_by('-score')

    return render(
        request, 
        'quizzes/quiz_result.html', 
        {
            'quiz': quiz,
            'participation': participation,
            'leaderboard': leaderboard, 
        }
    )