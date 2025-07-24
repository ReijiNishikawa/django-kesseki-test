# todo/views.py

from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task

def index(request):
    if request.method == 'POST':
        due_at_str = request.POST.get('due_at')
        if due_at_str:
            due_at_parsed = parse_datetime(due_at_str)
            if due_at_parsed:
                due_at_aware = make_aware(due_at_parsed)
            else:
                due_at_aware = None
        else:
            due_at_aware = None

        task = Task(
            title=request.POST['title'],
            due_at=due_at_aware
        )
        task.save()
        return redirect('index')

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')
    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)

def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        task.title = request.POST['title']
        
        due_at_str = request.POST.get('due_at')
        if due_at_str:
            due_at_parsed = parse_datetime(due_at_str)
            if due_at_parsed:
                task.due_at = make_aware(due_at_parsed)
            else:
                task.due_at = None
        else:
            task.due_at = None
            
        task.save()
        return redirect('detail', task_id=task.id)

    context = {
        'task': task,
    }
    return render(request, 'todo/edit.html', context)

def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        task.delete()
        return redirect('index')

    context = {
        'task': task,
    }
    return render(request, 'todo/delete.html', context)