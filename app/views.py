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
        students = cursor.fetchall()

    result_dict = {'records': students}

    return render(request,'app/index.html',result_dict)

# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students WHERE student_id = %s", [id])
        student = cursor.fetchone()
    result_dict = {'student': student}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def login(request):
    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM students WHERE email = %s AND pass = %s", [request.POST['email'], request.POST['pass']])
            student = cursor.fetchone()
            ## No customer with same id
            if student == None:
                return redirect('register')    
            else:
                return redirect('index')
    return render(request,'app/login.html')


# Create your views here.
def register(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM students WHERE email = %s", [request.POST['email']])
            student = cursor.fetchone()
            ## No customer with same id
            if student == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO students VALUES (%s, %s, %s, %s, %s)"
                        , [request.POST['student_id'], request.POST['first_name'] ,request.POST['last_name'], request.POST['email'], request.POST['pass']])
                return redirect('index')    
            else:
                status = 'Account under %s exist' % (request.POST['email'])


    context['status'] = status
 
    return render(request, "app/register.html", context)

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
            cursor.execute("UPDATE students SET first_name = %s, last_name = %s, email = %s, time_availability = %s, location_id = %s WHERE student_id = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['time_availability'] , request.POST['location_id'], id ])
            status = 'Student edited successfully!'
            cursor.execute("SELECT * FROM students WHERE student_id = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)

# Select all customrs from cetrain id
def myCalculators(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM calculators cal WHERE cal.owner_id = %s", [id])
        calculator = cursor.fetchall()
        cursor.execute("SELECT cal.serial_number, cal.calc_type FROM loan l, calculators cal WHERE l.borrower_id = %s AND l.owner_id = cal.owner_id", [id])
        loaned = cursor.fetchall()
        result_dict = {'calculators': calculator, 'loaned': loaned}

    return render(request,'app/myCalculators.html',result_dict)

def editAvailability(request, id):
    context ={}

    with connection.cursor() as cursor:
        cursor.execute('SELECT serial_number, availability FROM calculators WHERE calculators.serial_number = %s', [id])
        spec_avail = cursor.fetchall()
        

    spec_status = ''
    # save the data from the form

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE calculators SET availaibilty = %s WHERE calculators.serial_number = %s",[request.POST['availability']], id)
            spec_status = 'Availability edited successfully!'
            cursor.execute("SELECT serial_no, availaibility, owner_id FROM calculators WHERE calculator.serial_number = %s", [id])
            spec_avail = cursor.fetchone()


    context["spec_avail"] = spec_avail
    context["status"] = spec_status
 
    return render(request, "app/editAvailability.html")

# view hot locations
def hot(request):
    """Shows the main page"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT s.time_availability, COUNT (*) FROM students s GROUP BY s.time_availability ORDER BY COUNT DESC LIMIT 5;")
        timings = cursor.fetchall()
        cursor.execute("SELECT * FROM locations l, (SELECT s1.location_id, COUNT (*) as count FROM students s1 GROUP BY s1.location_id) as hot_location WHERE l.location_id = hot_location.location_id ORDER BY hot_location.count DESC;")
        locations = cursor.fetchall()
    result_dict = {'student_timings': timings,
                  'student_locations': locations}
    return render(request,'app/hot.html',result_dict)

def addCalculator(request, id):
    """Adds a calculator to id"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT serial_number FROM calculators WHERE calculators.serial_number = %s", [request.POST['serial_number']])
            serial_number = cursor.fetchone()
            ## No customer with same id
            if serial_number == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO calculators VALUES (%s, %s, %s, %s, %s, %s)"
                        , [request.POST['serial_number'], request.POST['calc_type'], request.POST['price'],
                           request.POST['calc_condition'] , request.POST['availability'], [id]])
                return redirect('index')
            else:
                status = 'Calculator with serial number %s already exists' % (request.POST['serial_number'])


    context['status'] = status
 
    return render(request, "app/addCalculator.html", context)

# find calculators
def findCalculators(request):
    """Shows the main page"""
    #with connection.cursor() as cursor:
    return render(request,'app/findCalculators.html')
