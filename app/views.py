from urllib import request
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

# Create your views here.
def index(request):
    """Shows the main page"""
    if request.session.has_key('username'):
        username = request.session['username']
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE email = %s", [request.POST['id']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students ORDER BY first_name, last_name")
        students = cursor.fetchall()
        cursor.execute("SELECT s.admin_rights FROM students s WHERE s.email = %s", [username])
        test_admin = cursor.fetchone() 
    result_dict = {'records': students, 
                   'username': username,
                   'admin': test_admin}
    return render(request,'app/index.html',result_dict)

def homepage(request):
    """Shows the main page"""
    
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        if request.session.has_key('username'):
            username = request.session['username']
        cursor.execute("SELECT s.first_name FROM students s WHERE s.email = %s", [username])
        user_name = cursor.fetchone()
        cursor.execute("SELECT s.email FROM students s WHERE s.email = %s", [username])
        email = cursor.fetchone()
        cursor.execute("SELECT COUNT (*) FROM students s")
        num_of_users = cursor.fetchone()
        cursor.execute("SELECT COUNT (*) FROM calculators c")
        num_of_calculators = cursor.fetchone()
        cursor.execute("SELECT location_name FROM locations l, hot_location hl WHERE l.location_id = hl.location_id ORDER BY hl.count DESC FETCH FIRST 1 ROWS ONLY;")
        hottest_location = cursor.fetchone()
        cursor.execute("SELECT s.admin_rights FROM students s WHERE s.email = %s", [username])
        test_admin = cursor.fetchone()
    
    result_dict = {'name':user_name,
                   'admin': test_admin,
                   'email': email,
                   'user': num_of_users,
                  'calculator': num_of_calculators,
                  'location': hottest_location}
    
    return render(request,'app/homepage.html', result_dict)

# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students WHERE email = %s", [id])
        student = cursor.fetchone()
    result_dict = {'student': student}

    return render(request,'app/view.html',result_dict)

def login(request):
    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("CREATE OR REPLACE VIEW hot_location AS SELECT s.location_id, COUNT (*) as count FROM students s GROUP BY s.location_id;")
            cursor.execute("SELECT * FROM students WHERE email = %s AND pass = %s", [request.POST['email'], request.POST['pass']])
            student = cursor.fetchone()
            ## No customer with same id
            if student == None:
                return redirect('register')    
            else:
                request.session['username'] = request.POST['email']
                cursor.execute("SELECT s.admin_rights FROM students s WHERE s.email = %s", [request.POST['email']])
                admin = cursor.fetchone()
                if admin == True:
                    return redirect('index')
                else:
                    return redirect('homepage')
    return render(request,'app/login.html')

"""
# Admin login backup
def login(request):
    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM admin_account WHERE email = %s AND pass = %s", [request.POST['email'], request.POST['pass']])
            admin_account = cursor.fetchone()
            ## No customer with same id
            if admin_account == None:
                return redirect('register')    
            else:
                return redirect('index')
    return render(request,'app/login.html')
"""

# Create your views here.
def register(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if email is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM students WHERE email = %s", [request.POST['email']])
            student = cursor.fetchone()
            ## No student with same email
            if student == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO students VALUES (%s, %s, %s, %s)"
                        , [request.POST['email'], request.POST['first_name'] ,request.POST['last_name'], request.POST['pass']])
                return redirect('login')    
            else:
                status = 'Email %s taken' % (request.POST['email'])


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
        cursor.execute("SELECT * FROM students WHERE email = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE students SET first_name = %s, last_name = %s, time_availability = %s, location_id = %s WHERE email = %s"
                    , [request.POST['first_name'], request.POST['last_name'],
                        request.POST['time_availability'] , request.POST['location_id'], id ])
            status = 'Student edited successfully!'
            cursor.execute("SELECT * FROM students WHERE email = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)

# Select all customrs from cetrain id
def myCalculators(request, id):
    
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM calculators WHERE brand = %s AND serial_number = %s", [request.POST['brand'], request.POST['serial_number']])
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM calculators cal WHERE cal.email = %s", [id])
        calculator = cursor.fetchall()
        cursor.execute("SELECT cal.serial_number, cal.calc_type FROM loan l, calculators cal WHERE l.borrower_email = %s AND l.owner_email = cal.email", [id])
        loaned = cursor.fetchall()
        result_dict = {'calculators': calculator, 'loaned': loaned, 'student_email':id}

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
            cursor.execute("UPDATE calculators SET availability = %s WHERE calculators.serial_number = %s",[request.POST['availability'], id])
            spec_status = 'Availability edited successfully!'
            cursor.execute("SELECT serial_number, availability, email FROM calculators WHERE calculators.serial_number = %s", [id])
            spec_avail = cursor.fetchone()
            return redirect('homepage')


    context["spec_avail"] = spec_avail
    context["status"] = spec_status
 
    return render(request, "app/editAvailability.html")

# view hot locations
def hot(request):
    """Shows the main page"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT s.time_availability, COUNT (*) FROM students s GROUP BY s.time_availability ORDER BY COUNT DESC LIMIT 5;")
        timings = cursor.fetchall()
        cursor.execute("SELECT * FROM locations l, hot_location hl WHERE l.location_id = hl.location_id ORDER BY hl.count DESC;")
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
                cursor.execute("INSERT INTO calculators VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        ,[request.POST['brand'] , request.POST['serial_number'], request.POST['calc_type'], request.POST['price'],
                           request.POST['calc_condition'] , request.POST['availability'], id])
                return redirect('homepage')

            else:
                status = 'Calculator with serial number %s already exists' % (request.POST['serial_number'])


    context['status'] = status
 
    return render(request, "app/addCalculator.html", context)

# find calculators
def findCalculators(request):
    result_dict={}

    if request.POST:      
        with connection.cursor() as cursor:
            select_statement = "SELECT c.calc_type, c.brand, c.serial_number, c.price, c.calc_condition, l.location_name, s.time_availability, s.first_name, s.last_name, s.email FROM calculators c, students s, locations l WHERE c.availability='available' AND c.email = s.email AND l.location_id=s.location_id AND (CAST(%s as INTEGER)-s.time_availability<=59) AND l.location_name = %s AND c.calc_type=%s"
            user_input = (request.POST['s.time_availability'], request.POST['l.location_name'], request.POST['c.calc_type'])
            cursor.execute(select_statement,user_input)
            available_calculators = cursor.fetchall()    

        result_dict = {'Results':available_calculators}
        return render(request, 'app/findCalculators.html', result_dict)
    return render(request,'app/findCalculators.html', result_dict)

def findCalculators_time(request):
    result_dict={}
    if request.POST:
        with connection.cursor() as cursor:
            select_statement="SELECT c.calc_type, c.brand, c.serial_number, c.price, c.calc_condition, l.location_name, s.time_availability, s.first_name, s.last_name, s.email FROM calculators c, students s, locations l WHERE c.availability='available' AND c.email = s.email AND l.location_id=s.location_id AND ((CAST(%s as INTEGER)-s.time_availability) BETWEEN 0 AND 59) ORDER by s.time_availability ASC"
            user_input = [request.POST['s.time_availability']]
            cursor.execute(select_statement,user_input)
            available_calculators = cursor.fetchall() 
        result_dict = {'Results':available_calculators}
        return render(request, 'app/findCalculators_time.html', result_dict)
    return render(request,'app/findCalculators_time.html', result_dict)


def findCalculators_location(request):
    result_dict={}
    if request.POST:
        with connection.cursor() as cursor:
            select_statement = "SELECT c.calc_type, c.brand, c.serial_number, c.price, c.calc_condition, l.location_name, s.time_availability, s.first_name, s.last_name, s.email FROM calculators c, students s, locations l WHERE c.availability='available' AND c.email = s.email AND l.location_id=s.location_id AND l.location_name = %s ORDER BY l.location_name ASC"
            user_input = [request.POST['l.location_name']]
            cursor.execute(select_statement,user_input)
            available_calculators = cursor.fetchall() 
        result_dict = {'Results':available_calculators}
        return render(request, 'app/findCalculators_location.html', result_dict)
    return render(request,'app/findCalculators_location.html', result_dict)

def findCalculators_type(request):
    result_dict={}
    if request.POST:
        with connection.cursor() as cursor:
            select_statement = "SELECT c.calc_type, c.brand, c.serial_number, c.price, c.calc_condition, l.location_name, s.time_availability, s.first_name, s.last_name, s.email FROM calculators c, students s, locations l WHERE c.availability='available' AND c.email = s.email AND l.location_id=s.location_id AND c.calc_type=%s ORDER BY c.calc_type ASC"
            user_input = [request.POST['c.calc_type']]
            cursor.execute(select_statement,user_input)
            available_calculators = cursor.fetchall() 
        result_dict = {'Results':available_calculators}
        return render(request, 'app/findCalculators_type.html', result_dict)
    return render(request,'app/findCalculators_type.html', result_dict)

def findCalculators_time_loc(request):
    result_dict={}
    if request.POST:
        with connection.cursor() as cursor:
            select_statement = "SELECT c.calc_type, c.brand, c.serial_number, c.price, c.calc_condition, l.location_name, s.time_availability, s.first_name, s.last_name, s.email FROM calculators c, students s, locations l WHERE c.availability='available' AND c.email = s.email AND l.location_id=s.location_id AND ((CAST(%s as INTEGER)-s.time_availability) BETWEEN 0 AND 59) AND l.location_name = %s ORDER BY l.location_name ASC"
            user_input = (request.POST['s.time_availability'], request.POST['l.location_name'])
            cursor.execute(select_statement,user_input)
            available_calculators = cursor.fetchall() 
        result_dict = {'Results':available_calculators}
        return render(request, 'app/findCalculators_time_loc.html', result_dict)
    return render(request,'app/findCalculators_time_loc.html', result_dict)

def findCalculators_time_type(request):
    result_dict={}
    if request.POST:
        with connection.cursor() as cursor:
            select_statement = "SELECT c.calc_type, c.brand, c.serial_number, c.price, c.calc_condition, l.location_name, s.time_availability, s.first_name, s.last_name, s.email FROM calculators c, students s, locations l WHERE c.availability='available' AND c.email = s.email AND l.location_id=s.location_id AND ((CAST(%s as INTEGER)-s.time_availability) BETWEEN 0 AND 59) AND c.calc_type=%s ORDER BY s.time_availability ASC"
            user_input = (request.POST['s.time_availability'],  request.POST['c.calc_type'])
            cursor.execute(select_statement,user_input)
            available_calculators = cursor.fetchall() 
        result_dict = {'Results':available_calculators}
        return render(request, 'app/findCalculators_time_type.html', result_dict)
    return render(request,'app/findCalculators_time_type.html', result_dict)

def findCalculators_loc_type(request):
    result_dict={}
    if request.POST:
        with connection.cursor() as cursor:
            select_statement = "SELECT c.calc_type, c.brand, c.serial_number, c.price, c.calc_condition, l.location_name, s.time_availability, s.first_name, s.last_name, s.email FROM calculators c, students s, locations l WHERE c.availability='available' AND c.email = s.email AND l.location_id=s.location_id AND l.location_name = %s AND c.calc_type=%s ORDER BY l.location_name ASC"
            user_input = (request.POST['l.location_name'], request.POST['c.calc_type'])
            cursor.execute(select_statement,user_input)
            available_calculators = cursor.fetchall() 
        result_dict = {'Results':available_calculators}
        return render(request, 'app/findCalculators_loc_type.html', result_dict)
    return render(request,'app/findCalculators_loc_type.html', result_dict)

def findCalculators_all(request):
    result_dict={}
    with connection.cursor() as cursor:
        select_statement = "SELECT c.calc_type, c.brand, c.serial_number, c.price, c.calc_condition, l.location_name, s.time_availability, s.first_name, s.last_name, s.email FROM calculators c, students s, locations l WHERE c.availability='available' AND c.email = s.email AND l.location_id=s.location_id ORDER BY c.calc_type ASC"
        cursor.execute(select_statement)
        available_calculators = cursor.fetchall() 
    result_dict = {'Results':available_calculators}
    return render(request, 'app/findCalculators_all.html', result_dict)

def borrow(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students WHERE email = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form
    
    if request.POST:
        with connection.cursor() as cursor:
            # generate loan id
            cursor.execute("SELECT MAX(loan_id) FROM loan")
            loan_id = cursor.fetchone()
            
            # get location id
            cursor.execute("SELECT location_id FROM location WHERE location_name == %s")
            location_id = cursor.fetchone()
            
            # get borrower's email
            if request.session.has_key('username'):
                borrower_email = request.session['username']
            
            cursor.execute("INSERT INTO loan VALUES (loan_id, %s, %s, %s, borrower_email, location_id, location_id, %s, %s)"
                        ,[request.POST['loan_time'] , request.POST['return_time'], request.POST['loaner_email'],
                          request.POST['brand'] , request.POST['serial_number'], id])
            
            cursor.execute("UPDATE students SET number_of_transaction += 1 WHERE email = %s"
                    , [request.POST['loaner_email'], id ])
            
            cursor.execute("UPDATE calculators SET availability = 'not available' WHERE brand = %s AND serial_number = %s AND email = %s"
                    , [request.POST['brand'] , request.POST['serial_number'], request.POST['loaner_email'], id ])
            
            status = 'Borrowed successfully! Contact your loaner through their email if you have further queries.'

    context["status"] = status
 
    return render(request, "app/homepage.html", context)


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return HttpResponse("<strong>You are logged out.</strong>")

