from todolist.models import ToDoTask


def rating_generator():
    last_task = ToDoTask.objects.filter().order_by('-rating').first()
    rating = last_task.rating if last_task else 0
    return rating + 1
