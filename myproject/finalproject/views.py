# Create your views here.
#from django import http
from django import template
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from google.appengine.ext import db

from myproject.finalproject import djangoforms
from myproject.finalproject import models

import datetime
from google.appengine.api import users

def home(request):
    q = models.Question.all().order('-date_modified')
    count = q.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }

    return render_to_response('finalproject/index.html', {
        'questions': q,
        'count': count,
        'context': context,
    }, template.RequestContext(request))

class QuestionForm(djangoforms.ModelForm):
    class Meta:
        model = models.Question
        exclude = ["short_question", "date_modified"]

def question_form(request, question_id=None):
    q = models.Question.all().order('-date_modified')
    count = q.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }

    if request.method == 'POST':
        # The form was submitted.
        if question_id:
            # Fetch the existing Question and update it from the form.
            question = models.Question.get_by_id(int(question_id))
            question.short_question = question.question_text[:500]
            form = QuestionForm(request.POST, instance=question)
        else:
            # Create a new Question based on the form.
            form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.short_question = question.question_text[:500]
            question.put()
            return HttpResponseRedirect('/questions')
        # else fall through to redisplay the form with error messages

    else:
        # The user wants to see the form.
        if question_id:
            # Show the form to edit an existing Question.
            question = models.Question.get_by_id(int(question_id))
            question.short_question = question.question_text[:500]
            form = QuestionForm(instance=question)
        else:
            # Show the form to create a new Question.
            form = QuestionForm()

    return render_to_response('finalproject/question_form.html', {
        'questions': q,
        'count': count,
        'question_id': question_id,
        'form': form,
        'context': context,
    }, template.RequestContext(request))

def add_question_login_form(request):
    q = models.Question.all().order('-date_modified')
    count = q.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }

    if user:
        if request.method == 'POST':
            # The form was submitted.
            # Create a new Question based on the form.
            form = QuestionForm(request.POST)

            if form.is_valid():
                question = form.save(commit=False)
                question.short_question = question.question_text[:500]
                question.date_created = question.date_created + datetime.timedelta(hours=-5)
#               question.date_modified = question.date_modified + datetime.timedelta(hours=-5)
                question.date_modified = current_time
                question.put()
                return HttpResponseRedirect('/questions')
            # else fall through to redisplay the form with error messages

        else:
            # The user wants to see the form.
            # Show the form to create a new Question.
            form = QuestionForm()

        return render_to_response('finalproject/question_form.html', {
            'questions': q,
            'count': count,
            'form': form,
            'context': context,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/login_form.html', {
            'context': context,
            'questions': q,
            'count': count,
        }, template.RequestContext(request))

def edit_question_login_form(request, question_id=None):
    q = models.Question.all().order('-date_modified')
    count = q.count()
    current_time = datetime.datetime.now() + datetime.timedelta(hours=-5)
    user = users.get_current_user()
    login_url = users.create_login_url(request.path)
    logout_url = users.create_logout_url(request.path)
    context = {
        'current_time': current_time,
        'user': user,
        'login_url': login_url,
        'logout_url': logout_url,
    }

    if user:
        if request.method == 'POST':
            # The form was submitted.
            if question_id:
                # Fetch the existing Question and update it from the form.
                question = models.Question.get_by_id(int(question_id))
                question.short_question = question.question_text[:500]
                form = QuestionForm(request.POST, instance=question)
            else:
                # Create a new Question based on the form.
                form = QuestionForm(request.POST)

            if form.is_valid():
                question = form.save(commit=False)
                question.short_question = question.question_text[:500]
                #question.date_modified = question.date_modified + datetime.timedelta(hours=-5)
                question.date_modified = current_time
                question.put()
                return HttpResponseRedirect('/questions')
            # else fall through to redisplay the form with error messages

        else:
            # The user wants to see the form.
            if question_id:
                # Show the form to edit an existing Question.
                question = models.Question.get_by_id(int(question_id))
                question.short_question = question.question_text[:500]
                form = QuestionForm(instance=question)
            else:
                # Show the form to create a new Question.
                form = QuestionForm()

        return render_to_response('finalproject/question_form.html', {
            'questions': q,
            'count': count,
            'question_id': question_id,
            'form': form,
            'context': context,
        }, template.RequestContext(request))

    else:
        return render_to_response('finalproject/login_form.html', {
            'context': context,
            'questions': q,
            'count': count,
        }, template.RequestContext(request))
