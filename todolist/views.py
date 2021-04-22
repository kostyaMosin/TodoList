from django.shortcuts import render, redirect, get_object_or_404

from todolist.forms import TaskForm
from todolist.models import ToDoTask
from todolist.rating_generator import rating_generator


def view_create_task_and_todo_list(request):
    if request.method == 'GET':
        context = {
            'form': TaskForm(),
            'data': ToDoTask.objects.filter().order_by('rating'),
        }
        return render(request, 'index.html', context)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            data = {'content': cd['content'], 'priority': cd['priority'], 'rating': rating_generator()}
            ToDoTask.objects.create(**data)
            return redirect('index')
        context = {
            'form': form,
            'data': ToDoTask.objects.filter().order_by('rating'),
        }
        return render(request, 'index.html', context)


def view_edit_task(request, pk):
    task = get_object_or_404(ToDoTask, id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            task.content = cd['content']
            task.priority = cd['priority']
            task.save()
            return redirect('index')
        return render(request, 'edit.html', {'form': form, 'task': task})
    return render(request, 'edit.html', {'form': TaskForm(), 'task': task})


def view_delete_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(ToDoTask, id=pk)
        task.delete()
        return redirect('index')


def view_complete_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(ToDoTask, id=pk)
        task.complete = True
        task.save()
        return redirect('index')


def view_sort_by_priority(request, priority):
    context = {
        'data': ToDoTask.objects.filter(priority=priority).order_by('rating'),
    }
    return render(request, 'sort.html', context)


def view_move_rating_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(ToDoTask, id=pk)
        button = request.POST['button']
        task_near = None
        if button == 'Up':
            task_high = ToDoTask.objects.filter(rating__lt=task.rating).order_by('-rating').first()
            if task_high is not None:
                task_near = task_high
            else:
                return redirect('index')
        if button == 'Down':
            task_low = ToDoTask.objects.filter(rating__gt=task.rating).order_by('rating').first()
            if task_low is not None:
                task_near = task_low
            else:
                return redirect('index')
        task.rating, task_near.rating = task_near.rating, task.rating
        task.save()
        task_near.save()
        return redirect('index')
