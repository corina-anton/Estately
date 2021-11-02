# About:
Estately is a mock real estate application where users can rent and buy living or commercial spaces, as well as post their own properties. At the moment, the application incorporates a custom authentication system, a search functionality and an account dashboard where users can update their details and change their password. Also, there are custom authorisation checks put in place to limit users' access to specific functionalities and actions (e.g., visitors can not access the dashboard unless they are logged in).

# What I am working on:
+ more account management functionalities: delete account, change email
+ a bookmark functionalities to save favourite posts
+ statistics for each property (e.g., the number of people that viewed the announcement)

# Things I have learned / consolidated:
+ implementing a custom authentication system, as well as the role of cookies and sessions in this process
+ implementing custom authorisation checks to limit access to specific users
+ making use of Django’s Object-Relational Mapper (ORM) to communicate with the database; revise here: [Django ORM (Querysets)](https://tutorial.djangogirls.org/en/django_orm/)
+ creating relationships between tables in a database (many-to-many, one-to-many, one-to-one)
+ how to create, read, update or delete a database entry
+ using the Django Form class to instantiate, process, and render forms
+ implement custom data validation based on the logic / architecture of the application
+ using Django’s file access APIs to allow users to upload their own images and save them to the database

# Key takeaways / Things to remember:

### The difference between `filter()`, `get()` and `exists()` methods
1. **The `filter()` method**<br>
It is in fact a **QuerySet**. QuerySets allow you to read the data from the database, filter it and order it based on given parameters.<br>
In SQL terms, a QuerySet equates to a SELECT statement, and a filter is a limiting clause such as WHERE or LIMIT. For example: `Entry.objects.filter(pub_date__year=2006)` is equivalent to `Entry.objects.all().filter(pub_date__year=2006)`.<br>
The `filter()` method will return a **new QuerySet** containing **all the objects** that match the given lookup parameters.

2. **The `get()` method**<br>
The `get()` method *does not* return a QuerySet but they still query the the database each time they’re called.<br>
It will return returns the **value** of the item with the specified key.<br>
If `get()` doesn’t find any object, it raises a  [Model.DoesNotExist](https://docs.djangoproject.com/en/3.2/ref/models/class/#django.db.models.Model.DoesNotExist) exception.<br>
If `get()` finds more than one object, it raises a [Model.MultipleObjectsReturned](https://docs.djangoproject.com/en/3.2/ref/models/class/#django.db.models.Model.MultipleObjectsReturned) exception.<br>

3. **The `QuerySet.exists()` method**
The `QuerySet.exists()` method is applied **ON** a QuerySet, meaning you ask the model: *are there any instances matching this query?* Note that you’re **NOT** yet attempting to retrieve any specific instance, you only check if it exists.<br>
The `exists()` method will return a **boolean**: true if there is at least one result, false otherwise.<br><br>

A good rule of thumb is to use `get()` when you want to get a specific unique object, and `filter()` when you want to get all the objects that match your lookup parameters.
