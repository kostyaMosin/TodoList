ToDoList
---------

A Django URL Shortener based on python [ToDoList](https://github.com/kostyaMosin/ToDoList).

Django-Todolist is a todolist web application with the most basic features of most web apps.


Setup
-----

````
git clone https://github.com/kostyaMosin/TodoList.git
cd TodoList
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
````

First run
---

````
cd TodoList
python manage.py migrate
python manage.py createsuperuser 
````


Run
---

It will listen on :8000
````
python manage.py runserver
````


Author
------

Kostya Mosin <kostyaMosin93@gmail.com>

References
----------

- First accreditation project at the school of programming [TeachMeSkills](https://teachmeskills.by/)
