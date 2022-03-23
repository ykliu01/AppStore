from urllib import request
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def index(request):
    """Shows the main page"""

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE student_id = %s", [request.POST['id']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students ORDER BY student_id")
        customers = cursor.fetchall()

    result_dict = {'records': customers}

    return render(request,'app/Login.html',result_dict)

# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students WHERE student_id = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'stud': student}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def login(request):
    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM students WHERE student_id = %s", [request.POST['student_id']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                return redirect('login')    
            else:
                return redirect('index')


# Create your views here.
def register(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM students WHERE student_id = %s", [request.POST['student_id']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s)"
                        , [request.POST['email'], request.POST['student_id'], request.POST['pass'],
                           request.POST['first_name'] , request.POST['last_name'], request.POST['dob'])
                return redirect('index')    
            else:
                status = 'Username %s taken' % (request.POST['student_id'])


    context['status'] = status
 
    return render(request, "app/Register.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students WHERE student_id = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE students SET first_name = %s, last_name = %s, email = %s, dob = %s, WHERE student_id = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Student edited successfully!'
            cursor.execute("SELECT * FROM students WHERE student_id = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)

# view hot locations
def hot(request):
    """Shows the main page"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT s.time, COUNT (*) FROM test_students s GROUP BY s.time ORDER BY COUNT DESC LIMIT 5;")
        timings = cursor.fetchall()
        cursor.execute("SELECT * FROM locations l, (SELECT s1.location_id, COUNT (*) as count FROM test_students s1 GROUP BY s1.location_id) as hot_location WHERE l.location_id = hot_location.location_id ORDER BY hot_location.count DESC;")
        locations = cursor.fetchall()
    result_dict = {'student_timings': timings,
                  'student_locations': locations}
    return render(request,'app/hot.html',result_dict)
