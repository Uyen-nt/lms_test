from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, AnswerOption, StudentQuizAttempt, StudentAnswer
from .forms import QuizForm, QuestionForm, AnswerOptionForm, QuizAnswerForm
from module_group.models import ModuleGroup
from django.contrib.auth.decorators import login_required
from django.db import transaction


def quiz_list(request):
    module_groups = ModuleGroup.objects.all()
    quizzes = Quiz.objects.select_related('course').all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes, 'module_groups': module_groups})

def quiz_add(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz:quiz_list')
        else:
            # Nếu form không hợp lệ, in lỗi ra để kiểm tra
            print(form.errors)  # Có thể dùng logging thay vì print
    else:
        form = QuizForm()
    return render(request, 'quiz_form.html', {'form': form})

def quiz_edit(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz:quiz_list')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz_form.html', {'form': form})

def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz:quiz_list')
    return render(request, 'quiz_confirm_delete.html', {'quiz': quiz})

def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    module_groups = ModuleGroup.objects.all()
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions, 'module_groups': module_groups})

def question_add(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('quiz:quiz_detail', pk=quiz.id)
    else:
        form = QuestionForm()
    return render(request, 'question_form.html', {'quiz': quiz, 'form': form})

def question_edit(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz = get_object_or_404(Quiz, id=question.quiz.id)  # Lấy quiz từ question

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('quiz:quiz_detail', pk=quiz.id)  # Sử dụng quiz.id
    else:
        form = QuestionForm(instance=question)

    return render(request, 'question_form.html', {'quiz': quiz, 'form': form})

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    quiz_id = question.quiz.id
    if request.method == 'POST':
        question.delete()   
        return redirect('quiz:quiz_detail', pk=question.quiz.id)
    return render(request, 'question_confirm_delete.html', {'question': question})



def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answer_options = AnswerOption.objects.filter(question=question)
    context = {
        'question': question,
        'answer_options': answer_options
    }
    return render(request, 'question_detail.html', context)


def answer_option_add(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)

    if request.method == 'POST':
        for i in range(4):
            option_text = request.POST.get(f'option_text_{i}')
            is_correct = request.POST.get(f'is_correct_{i}', False) == 'on'
            if option_text:  # Kiểm tra xem option_text có giá trị không
                AnswerOption.objects.create(question=question, option_text=option_text, is_correct=is_correct)

         # Lưu câu trả lời True/False
        true_text = request.POST.get('option_true')
        is_correct_true = request.POST.get('is_correct_true', False) == 'on'
        if true_text:
            AnswerOption.objects.create(question=question, option_text=true_text, is_correct=is_correct_true)

        false_text = request.POST.get('option_false')
        is_correct_false = request.POST.get('is_correct_false', False) == 'on'
        if false_text:
            AnswerOption.objects.create(question=question, option_text=false_text, is_correct=is_correct_false)
            
        return redirect('quiz:question_detail', pk=question.pk)

    return render(request, 'answer_option_form.html', {'question': question, 'options_range': range(4)})


def answer_option_edit(request, pk):
    option = get_object_or_404(AnswerOption, pk=pk)
    if request.method == 'POST':
        form = AnswerOptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            return redirect('quiz:question_detail', pk=option.question.id)
    else:
        form = AnswerOptionForm(instance=option)
    return render(request, 'answer_option_form.html', {'form': form})

def answer_option_delete(request, pk):
    option = get_object_or_404(AnswerOption, pk=pk)
    if request.method == 'POST':
        question_id = option.question.id
        option.delete()
        return redirect('quiz:question_detail', pk=question_id)
    return render(request, 'answer_option_confirm_delete.html', {'option': option})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Lấy tất cả các câu hỏi trong quiz

    if request.method == 'POST':
        # Khi người dùng gửi form (submit quiz)
        with transaction.atomic():
            # Tạo một lần thử quiz mới cho học sinh
            attempt = StudentQuizAttempt.objects.create(user=request.user, quiz=quiz, score=0.0)

            total_score = 0
            for question in questions:
                selected_option_id = request.POST.get(f'question_{question.id}')  # Lấy lựa chọn được chọn cho câu hỏi
                selected_option = AnswerOption.objects.get(id=selected_option_id) if selected_option_id else None

                # Lưu câu trả lời của học sinh
                StudentAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=selected_option
                )

                # Kiểm tra nếu lựa chọn đúng, cộng điểm
                if selected_option and selected_option.is_correct:
                    total_score += question.points

            # Cập nhật điểm tổng của lần thử
            attempt.score = total_score
            attempt.save()

            return redirect('quiz:quiz_result', quiz_id=quiz.id, attempt_id=attempt.id)  # Chuyển tới trang kết quả sau khi nộp bài

    # Render trang quiz với câu hỏi và lựa chọn
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})


@login_required
def quiz_result(request, quiz_id, attempt_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(StudentQuizAttempt, id=attempt_id, user=request.user)
    student_answers = StudentAnswer.objects.filter(attempt=attempt)

    return render(request, 'quiz_result.html', {
        'quiz' : quiz,
        'attempt': attempt,
        'student_answers': student_answers,
    })
