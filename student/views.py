from django.shortcuts import redirect, render 
from django.http import HttpResponse , HttpResponseRedirect
from .models import StudentCredentials , StudentDetails , StudentDocuments 
from django.core.exceptions import ValidationError
from decimal import Decimal , InvalidOperation
# from django.shortcuts import render, redirect
from django.urls import reverse
import string

def StudentRegisteration(request):
    
    def isValidName(name):
        name=name.strip()
  
        if len(name) < 8 : 
            return "Not a Proper Name format !"
        if name.count(" ") == 0 :
            return"looking like you missed middle name ! "
        if name.count(" ") < 2:
            return "looking like you missed sirname !"
        words = name.split()
    
        for word in words:
            if len(word) < 2:
                return "Name at least contain 2 letters !"
    
        return "Valid Name"

   

    def isValidPassword(password):
        
        feedback = []
    
        if password.count( " ") > 0 :
            feedback.append("Password do not contain white spaces")
            return feedback
        
        has_uppercase = any(char.isupper() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special_symbol = any(char in string.punctuation for char in password)

        if len(password) < 6:
            feedback.append("Password must be at least 6 characters long.")

        if not has_uppercase:
            feedback.append("Password must contain at least one uppercase letter.")

        if not has_digit:
            feedback.append("Password must contain at least one digit.")

        if not has_special_symbol:
            feedback.append("Password must contain at least one special character.")
        
        if feedback:
            return feedback
        return "Valid Password"


    errors = {}
    registred = request.session.get('registred', False)
    form_data = {
        'name': '',
        'email': '',
        'phone': '',
        'password': '',
        'confirm_password': '',
    }

    if request.method == 'POST':
        # Populate form data from POST request
        form_data = {key: request.POST.get(
            key, '').strip() for key in form_data}

        # Validation logic
        if not form_data['name']:
            errors['name'] = 'Name is required.'
        else :
             name = isValidName( form_data['name'] )
             if name != "Valid Name" :
                 errors['name'] = name 
                 
        if not form_data['email']:
            errors['email'] = 'Email is required.'
        elif '@' not in form_data['email'] or '.' not in form_data['email']:
            errors['email'] = 'Enter a valid email.'
        elif StudentCredentials.objects.filter(email=form_data['email']).exists():
            errors['email'] = 'Email Already Present, Use Another Email'

        if not form_data['phone']:
            errors['phone'] = 'Phone number is required.'
        elif not form_data['phone'].isdigit() or len(form_data['phone']) != 10:
            errors['phone'] = 'Enter a valid 10-digit phone number.'
        if not form_data['password']:
            errors['password'] = [ 'Password is required.' ]
        else :
            pas = isValidPassword( form_data['password'] )
            
            if pas != "Valid Password" :
                errors['password'] = pas 
                
        if not form_data['confirm_password']:
            errors['confirm_password'] = 'Confirm Password is required.'
        elif form_data['password'] != form_data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match.'

        if not errors:
            # Saving data into StudentCredentials table

            StudentCredentials.addStudent(
                form_data['name'], form_data['email'], form_data['phone'], form_data['password'])
            request.session['registred'] = True
           
            url = reverse('login')
            return redirect(url)
    """
    if registred:
        request.session['registred'] = False
        return render(request, 'student/registeration.html', {
            'form_data': {key: '' for key in form_data},
            'errors': {},
            'registred': True,
        })
    """
    
    return render(request, 'student/registeration.html', {
        'form_data': form_data,
        'errors': errors,
        'registred': False,
    })


def StudentDashboard(request):
    
    def documentStatus(docs):
        dic = {}
   
        for value in docs.values():
     
            if value.get("verified") == "rejected":
                dic[value['name']] = "rejected"
            elif value.get("verified") == "approved":
                dic[value['name']] = "approved"
            elif value.get("verified") == "pending":
                dic[value['name']] = "pending"
    
        print(dic)
        if "rejected" in dic.values():
            return  "rejected"
        elif all(status == "approved" for status in dic.values()):
            return  "approved"
        else :
           return  "pending"
    
    
    def hasRejectedDocument(docs):
        result = False
        for value in docs.values():
            if value.get("verified") == "rejected":
                result = True
                break
       
        return result

    if request.session.get('login',False) :
        values = None
        docs = None 
        rejected = False
        finalSubmition = False
     
       
               
        email = request.session.get("Email" , '' )
        section = request.GET.get('section' , '').strip()
       
        studentPhoto = StudentDocuments.getPhotoAndSignature( email )
        photo = studentPhoto['photo'] if studentPhoto['success'] else '' 
        response= render(request , 'student/studentdashboard.html' , {  'values' : { 'photo' : photo  }  , 'section' : "board"  , 'currStudent' : True    }  )

        if section == "application" or section == "report":
            
            studentBasicDetails = None 
            studentApplicationDetails = None 
            
            if values== None : 
                studentBasicDetails = StudentCredentials.getStudentInfo( email )
                studentApplicationDetails = StudentDetails.getStudentInfo( email )
        
            # Check if student data is available
            if values == None and  studentBasicDetails['success'] and studentApplicationDetails['success']:

                values = {
                    'photo' : studentPhoto['photo'] if studentPhoto['success'] else '' , 
                    'applicationId': studentApplicationDetails['student'].applicationId ,
                    'applicantName': studentBasicDetails['student'].name  ,
                    'email': studentBasicDetails['student'].email ,
                    'contactNumber': studentBasicDetails['student'].phone ,
                    'motherName': studentApplicationDetails['student'].motherName ,
                    'dob': studentApplicationDetails['student'].dateOfBirth ,
                    'nationality': studentApplicationDetails['student'].nationality ,
                    'category': studentApplicationDetails['student'].category ,
                    'gender': studentApplicationDetails['student'].gender ,
                    'address': studentApplicationDetails['student'].address ,
                    'marks10': studentApplicationDetails['student'].marksOf10th ,
                    'marks12': studentApplicationDetails['student'].marksOf12th ,
                    'school10': studentApplicationDetails['student'].schoolOf10th ,
                    'college12': studentApplicationDetails['student'].collegeOf12th
                }
        
            response =  render(request , 'student/studentdashboard.html' , { 'section' : section , 'values': values , 'currStudent' : True  })
        
        elif section == "updatedocuments" :
            docStatus = None 
            
            if docs == None :
                doc = StudentDocuments.getAllDocuments( email )
                if doc['success'] :
                    docs = doc['documents']
                    docStatus = documentStatus( docs )
                    
            response = render(request , 'student/studentdashboard.html' , {  'values' : { 'photo' : photo  }  , 'section' : section , 'docs':docs , 'currStudent' : True , 'finalSubmition' : docStatus })

        elif section == "updateCurrentDocs" :
            
            doc = StudentDocuments.getAllDocuments( email )
            docsInfo = {}
            errors = {}
            fields = [
             'marksheetOf10th', 'marksheetOf12th',
            'cetScoreCard', 'schoolLC', 'collegeLC', 'casteCertificate',
            'casteValidityCertificate', 'domicileCertificate', 'incomeCertificate',
            'nonCreamyLayerCertificate', 'aadharCard'
            ]
            
           
            for field in fields:
                file = request.FILES.get(field)
               
                if file:
                    docsInfo[field] = file
                else:
                    pass
                    #errors[field] = f"{field.replace('_', ' ').capitalize()} is required."

            # Check if there are no errors
            print(docsInfo)
            if not errors:
                #uploaded_files['email'] = request.session.get('Email', '')
                print("inserting in db ")
                # Call the model method to insert documents
                result = StudentDocuments.insertDocuments( request.session.get('Email' , '' ) , **docsInfo )

                if result['success'] :
                    doc = StudentDocuments.getAllDocuments( email )
                    response = render(request , 'student/studentdashboard.html' , {  'values' : { 'photo' : photo  }     ,    'section' : 'updatedocuments' ,  'docs':doc['documents'] , 'currStudent' : True , 'finalSubmition' :'uploaded'  })

            else :
                
                response = render(request , 'student/studentdashboard.html' , {  'values' : { 'photo' : photo  }     ,  'section' : 'updatedocuments' ,  'docs':doc['documents'] , 'currStudent' : True , 'finalSubmition' :'docNot'  })

            
            
            
            
            
            
            
            
        if section== "report" :
            docStatus = None 
            
            if docs == None :
                doc = StudentDocuments.getAllDocuments( email )
                if doc['success'] :
                    docs = doc['documents']
                    docStatus = documentStatus( docs )
                    
        
            response = render(request , 'student/studentdashboard.html' , { 'section' : section , 'values': values , 'docs':docs , 'currStudent' : True , 'finalSubmition' : docStatus  })

       
        #return render(request , 'student/studentdashboard.html' , { 'section' : section , 'values': values , 'docs':docs , 'currStudent' : True , 'finalSubmition' : False  })
        return response 
    return redirect('home')
       


def StudentApplication(request):
    if request.session.get("login", False):
        # Retrieve student credentials and application ID
        currentStudent = StudentCredentials.getStudentInfo(request.session.get("Email", ''))
        currentStudentD = StudentDetails.getPrevApplicationId()

        # Data for categories and gender
        std = {
            'category': {
                0: "Open",
                1: "Obc",
                2: "Nt-c",
                3: "Sc",
                4: "St"
            },
            'gender': {
                0: "Male",
                1: "Female",
                2: "Bisexual"
            }
        }

        # Check if student data is available
        if currentStudent['success']:
            std["name"] = currentStudent['student'].name
            std['email'] = currentStudent['student'].email
            std['phone'] = currentStudent['student'].phone

        # Generate application ID
        if currentStudentD == 0:
            std['id'] = "AP10001"
        else:
            std['id'] = currentStudentD[0:2] + (str(int(currentStudentD[2:]) + 1))

        # Default form values
        values = {
            'applicationId': std['id'],
            'applicantName': std["name"],
            'email': std['email'],
            'contactNumber': std['phone'],
            'motherName': "",
            'dob': "",
            'nationality': "",
            'category': "",
            'gender': "",
            'address': "",
            'marks10': "",
            'marks12': "",
            'uploadImage': None,
            'school10': "",
            'college12': ""
        }

        errors = {}
        
        def ttod( e ,  t ):
            try:
               return Decimal(t)
            except InvalidOperation :
               error[e] = "Invalid Number or Input"

        if request.method == "POST":
            # Retrieve form data
            motherName = request.POST.get("motherName", "").strip()
            dob = request.POST.get("dob", "").strip()
            nationality = request.POST.get("nationality", "").strip()
            category = request.POST.get("category", "").strip()
            gender = request.POST.get("gender", "").strip()
            address = request.POST.get("address", "").strip()
            marks10 = ttod("marks10" , request.POST.get("marks10", "").strip())
            marks12 = ttod( "marks12"  ,  request.POST.get("marks12", "").strip() )
            uploadImage = request.FILES.get("uploadImage", None)
            school10 = request.POST.get("school10", "").strip()
            college12 = request.POST.get("college12", "").strip()

            # Validate form data
            if not motherName:
                errors["motherName"] = "Mother's name is required."
            if not dob:
                errors["dob"] = "Date of birth is required."
            if not nationality:
                errors["nationality"] = "Nationality is required."
            if not category:
                errors["category"] = "Category is required."
            if not gender:
                errors["gender"] = "Gender is required."
            if not address:
                errors["address"] = "Address is required."
         
            if not school10:
                errors["school10"] = "School name for 10th is required."
            if not college12:
                errors["college12"] = "College name for 12th is required."

            # If errors are found, re-render the form with the existing data and error messages
            if errors:
                return render(request, "student/application.html", {
                    'errors': errors,
                    'values': values
                })
                
                
            if not errors :

                studentData = {
                     'applicationId': std['id']  ,
                     'motherName':  motherName ,
                     'dateOfBirth': dob ,
                     'email': std['email'] ,  
                     'nationality': nationality ,
                     'category': category ,
                     'gender':  gender ,
                     'address': address ,
                     'marksOf10th': marks10 ,
                     'marksOf12th': marks12 ,
                     'schoolOf10th': school10 ,
                     'collegeOf12th': college12 ,
                }

            result1 = StudentDetails.insertStudent(**studentData)

            result2 =  StudentDocuments.insertPhotoAndSignature( std['email'] , uploadImage )

            if result1 and result2 == "inserted" :
                  msg = "Application has Been Submitted Successfully"
                  return redirect("UploadDocuments")
            else :
                return HttpResponse(result2)


        return render(request, "student/application.html", {
            'values': values,
            'errors': errors
        })
    else:
        return redirect('home')




def uploadDocuments(request):
    errors = {}
    uploaded_files = {}

    if request.method == 'POST':
        # Collect all required fields
        required_fields = [
            "marksheetOf10th", "marksheetOf12th",
            "cetScoreCard", "schoolLC", "collegeLC",
            "casteCertificate", "casteValidityCertificate", "domicileCertificate",
            "incomeCertificate", "nonCreamyLayerCertificate", "aadharCard"
        ]

        for field in required_fields:
            file = request.FILES.get(field)
            if file:
                uploaded_files[field] = file
            else:
                errors[field] = f"{field.replace('_', ' ').capitalize()} is required."

        # Check if there are no errors
        if not errors:
            #uploaded_files['email'] = request.session.get('Email', '')

            # Call the model method to insert documents
            result = StudentDocuments.insertDocuments( request.session.get('Email' , '' ) , **uploaded_files)

            
            if result['success']:
                return redirect('StudentDashboard')
            else:
                errors['general'] = result['message']
                return HttpResponse(errors['general'])

    return render(request, 'student/documentform.html', {
        'form': errors,
        'uploaded_files': uploaded_files
    })
