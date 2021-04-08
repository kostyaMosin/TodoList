from django.db.models import QuerySet
from django.test import TestCase

from todolist.forms import TaskForm
from todolist.models import ToDoTask


class ViewTestCase(TestCase):
    def setUp(self):
        self.task_1 = ToDoTask.objects.create(content='Task', priority='1', rating=1)
        self.task_2 = ToDoTask.objects.create(content='Task', priority='2', rating=2)
        self.task_3 = ToDoTask.objects.create(content='Task', priority='3', rating=3)

    def test_view_create_and_todo_list_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIsInstance(form, TaskForm)
        self.assertIn('data', response.context)
        data = response.context['data']
        self.assertIsInstance(data, QuerySet)

    def test_view_create_and_todo_list_post(self):
        content = 'My first task'
        priority = '3'
        response = self.client.post('/', {'content': content, 'priority': priority})
        self.assertRedirects(response, '/', 302, fetch_redirect_response=False)
        task = ToDoTask.objects.filter(content=content).first()
        response = self.client.get('/')
        data = response.context['data']
        self.assertIn(task, data)
        self.assertIsInstance(data, QuerySet)
        self.assertEqual(task.content, data[3].content)
        self.assertEqual(task.priority, data[3].priority)
        self.assertEqual(task.rating, data[3].rating)
        self.assertEqual(task.rating, 4)

    def test_view_create_and_todo_list_form_is_not_valid(self):
        content, priority = '', '3'
        response = self.client.post('/', {'content': content, 'priority': priority})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertFormError(response, 'form', 'content', 'This field is required.')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIsInstance(form, TaskForm)
        self.assertIn('data', response.context)
        data = response.context['data']
        self.assertIsInstance(data, QuerySet)

    def test_view_edit_task_get(self):
        response = self.client.get(f'/edit/{self.task_1.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertIn('task', response.context)
        task_out = response.context['task']
        self.assertIsInstance(task_out, ToDoTask)
        self.assertEqual(self.task_1.content, task_out.content)
        self.assertEqual(self.task_1.rating, task_out.rating)
        self.assertEqual(self.task_1.priority, task_out.priority)
        self.assertNotIn('form', response.context)

    def test_view_edit_task_post(self):
        content, priority = 'My task', '3'
        response = self.client.post(f'/edit/{self.task_1.pk}', {'content': content, 'priority': priority})
        self.assertRedirects(response, '/', 302, fetch_redirect_response=False)
        response = self.client.get(f'/edit/{self.task_1.pk}')
        self.assertIn('task', response.context)
        task_out = response.context['task']
        self.assertIsInstance(task_out, ToDoTask)
        self.assertEqual(task_out.content, content)
        self.assertEqual(task_out.rating, 1)
        self.assertEqual(task_out.priority, priority)
        self.assertNotIn('form', response.context)

    def test_edit_task_form_is_not_valid(self):
        content, priority = '', '1'
        response = self.client.post(f'/edit/{self.task_1.pk}', {'content': content, 'priority': priority})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertIn('form', response.context)
        self.assertIn('task', response.context)
        task = response.context['task']
        form = response.context['form']
        self.assertFormError(response, 'form', 'content', 'This field is required.')
        self.assertIsInstance(task, ToDoTask)
        self.assertIsInstance(form, TaskForm)

    def test_edit_task_404(self):
        response = self.client.get('/edit/failure')
        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        response = self.client.post(f'/delete/{self.task_1.pk}')
        self.assertRedirects(response, '/', 302, fetch_redirect_response=False)
        task_list = ToDoTask.objects.all()
        self.assertNotIn(self.task_1, task_list)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('data', response.context)
        data = response.context['data']
        self.assertIsInstance(data, QuerySet)
        self.assertNotIn(self.task_1, data)

    def test_delete_task_404(self):
        response = self.client.get('/delete/failure')
        self.assertEqual(response.status_code, 404)

    def test_view_complete_task(self):
        response = self.client.post(f'/complete/{self.task_1.pk}')
        self.assertRedirects(response, '/', 302, fetch_redirect_response=False)
        task = ToDoTask.objects.get(pk=self.task_1.pk)
        self.assertEqual(task.complete, True)
        response = self.client.get('/')
        data = response.context['data']
        self.assertIn(task, data)
        task_list = ToDoTask.objects.filter(complete=False)
        self.assertNotIn(self.task_1, task_list)

    def test_view_complete_task_404(self):
        response = self.client.get('/complete/failure')
        self.assertEqual(response.status_code, 404)

    def test_view_up_rating_task(self):
        response = self.client.post(f'/move/{self.task_2.pk}', {'button': 'Up'})
        self.assertRedirects(response, '/', 302, fetch_redirect_response=False)
        task_1 = ToDoTask.objects.get(pk=self.task_1.pk)
        task_2 = ToDoTask.objects.get(pk=self.task_2.pk)
        response = self.client.get('/')
        data = response.context['data']
        self.assertIn(task_1, data)
        self.assertIn(task_2, data)
        self.assertEqual(self.task_1.rating, task_2.rating)
        self.assertEqual(self.task_2.rating, task_1.rating)

    def test_view_up_rating_task_is_on_top(self):
        task_1_rating_in = self.task_1.rating
        response = self.client.post(f'/move/{self.task_1.pk}', {'button': 'Up'})
        self.assertRedirects(response, '/', 302, fetch_redirect_response=False)
        task_1 = ToDoTask.objects.get(pk=self.task_1.pk)
        task_1_rating_out = task_1.rating
        self.assertEqual(task_1_rating_in, task_1_rating_out)
        response = self.client.get('/')
        data = response.context['data']
        self.assertIn(task_1, data)

    def test_view_down_rating_task(self):
        response = self.client.post(f'/move/{self.task_1.pk}', {'button': 'Down'})
        self.assertRedirects(response, '/', 302, fetch_redirect_response=False)
        task_1 = ToDoTask.objects.get(pk=self.task_1.pk)
        task_2 = ToDoTask.objects.get(pk=self.task_2.pk)
        response = self.client.get('/')
        data = response.context['data']
        self.assertIn(task_1, data)
        self.assertIn(task_2, data)
        self.assertEqual(self.task_1.rating, task_2.rating)
        self.assertEqual(self.task_2.rating, task_1.rating)

    def test_view_down_rating_task_is_on_top(self):
        task_3_rating_in = self.task_3.rating
        response = self.client.post(f'/move/{self.task_3.pk}', {'button': 'Down'})
        self.assertRedirects(response, '/', 302, fetch_redirect_response=False)
        task_3 = ToDoTask.objects.get(pk=self.task_3.pk)
        task_3_rating_out = task_3.rating
        self.assertEqual(task_3_rating_in, task_3_rating_out)
        response = self.client.get('/')
        data = response.context['data']
        self.assertIn(task_3, data)

    def test_view_move_rating_task_404(self):
        response = self.client.get('/move/failure')
        self.assertEqual(response.status_code, 404)

    def test_view_sort_by_priority(self):
        response = self.client.get(f'/sort/{self.task_1.priority}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sort.html')
        self.assertIn('data', response.context)
        data = response.context['data']
        self.assertIn(self.task_1, data)
        self.assertIsInstance(data, QuerySet)
        self.assertEqual(data[0].priority, self.task_1.priority)



