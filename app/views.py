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
                cursor.execute("DELETE FROM calculator cal WHERE cal.owner = %s", [request.POST['id']]) # Delete calculator entry

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers ORDER BY customerid")
        customers = cursor.fetchall()

    result_dict = {'records': customers}

    return render(request,'app/index.html',result_dict)

# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
                return redirect('index')    
            else:
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
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
        cursor.execute('SELECT serial_number, availaibility FROM calculators WHERE calculators.owner_id = %s', [id])
        spec_avail = cursor.fetchall()
        

    spec_status = ''
    # save the data from the form

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE calculators SET availaibilty = %s WHERE calculators.owner_id = %s",[request.POST['availability']], id)
            spec_status = 'Customer edited successfully!'
            cursor.execute("SELECT serial_no, availaibility FROM calculator WHERE calculator.owner_id = %s", [id])
            spec_avail = cursor.fetchone()


    context["spec_avail"] = spec_avail
    context["status"] = spec_status
 
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
