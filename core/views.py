
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from student.models import StudentCredentials , StudentDetails
from institude.models import Institute 

from django.contrib import messages

from django.urls import reverse

def Login(request):
    
   
    login = request.session.get("login", False)
    Email = request.session.get("Email", None)
    Role = request.session.get("Role", None)

    Role_Urls = getattr(settings, "ROLE_REDIRECTION")
    # Check if the user is already logged in
    if request.session.get("login", False):
        redirect_url = Role_Urls.get(request.session.get("Role", False))
        if redirect_url:
            return redirect( redirect_url )  # Redirect to the dashboard

    errors = { "refresh" : 0 }
   
    if request.method == "POST":
        # Retrieve form data
        role = request.POST.get("role")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate student
        result = None
        if role == "Student" :
           result = StudentCredentials.getStudent(email, password)
        elif role == "Administrator" :
           result = Institute.getAdministrator( email , password)
        else :
            errors = {} 
            
        print(role )
        print( email )
        print( password)
        if result["success"]:
            # Set session for authenticated user
            request.session["login"] = True
            request.session["Email"] = email  # Save user email in session
            request.session["Role"] = role

            redirect_url = Role_Urls.get(request.session.get("Role", False))
            if redirect_url:
                return redirect( redirect_url )  # Redirect to the dashboard
            
        else:
            # Get the first key
            key = next(iter(result.keys() - {"success"}), None)
            if key:
                errors[key] = result[key]
            
            print("hi queen")
            if errors['refresh'] > 0 :
                print(key)
                errors[key] = '' 
                
            errors['refresh'] +=1 
            
            print(errors)
            res = render(request , "core/login.html" , {'errors' : errors }   )
            
          
            
            return res 
            
            
    # Render login page with errors (if any)
    if request.session.get('registred') :
        
        context = { 'registred' : request.session.get('registred') }
        
        response = render(request , "core/login.html" , context )
        
        request.session['registred'] = False 
        
        return response 
    
    
    return render(request, "core/login.html", {"errors": errors })











def Logout(request):
    Auth = getattr(settings, "AUTH_REDIRECTION")
    if request.session.get("login", False):
        request.session["login"] = False
        request.session["Role"] = None
        request.session["Email"] = None
        return redirect(Auth.get("login"))


def home(request):
    Auth = getattr(settings, "AUTH_REDIRECTION", {})
    
    currStudent = StudentDetails.studentExists(request.session.get("Email",False))
       

    return render(request, "core/home.html", {
        'currStudent' : currStudent , 
        'StudentDashboard' : 'StudentDashboard',
        'login': request.session.get("login", False),
        'role': request.session.get("Role", False),
        'login_url': Auth.get("login"),
        'register_url': Auth.get("register"),
        'newapplication_url':'StudentApplication',  # Named URL for new application
        'logout_url': Auth.get('logout'),  # Named URL for logout
        'instituteDashboard': 'instituteDashboard',  # Named URL for verification
    })
