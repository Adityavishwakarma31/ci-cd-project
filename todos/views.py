from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Todo
from .forms import TodoForm


def todo_list(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task added successfully.')
            return redirect('todo_list')
    else:
        form = TodoForm()

    todos = Todo.objects.all()
    total = todos.count()
    completed_count = todos.filter(completed=True).count()
    pending_count = total - completed_count

    context = {
        'form': form,
        'todos': todos,
        'total': total,
        'completed_count': completed_count,
        'pending_count': pending_count,
    }
    return render(request, 'todos/todo_list.html', context)


def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    messages.success(request, 'Task deleted.')
    return redirect('todo_list')


def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/edit_todo.html', {'form': form, 'todo': todo})
