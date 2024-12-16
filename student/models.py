
from django.db import models
from django.contrib.auth.hashers import check_password, make_password
import re 


from .storage_backends import NoLockingFileSystemStorage  # Import your custom storage backend


class StudentCredentials(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)  # Store hashed passwords

    def __str__(self):
        return self.email
        
    """
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # Prevent double hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    """
    
    @classmethod
    def getStudent(cls, email, password):
        try:
            student = cls.objects.get(email=email)
            if check_password(password, student.password):
                return {"success": True, "student": student}
            else:
                return {"success": False, "password": "Password is incorrect"}
        except cls.DoesNotExist:
            return {"success": False, "email": "Email does not exist register first "}

    @classmethod
    def getStudentInfo(cls, email ):
        try:
            student = cls.objects.get(email=email)
            return {"success": True, "student": student}
           
        except cls.DoesNotExist:
            return {"success": False, "message": "Email does not exist"}


    @classmethod
    def addStudent(cls, name, email, phone, password):
        if cls.objects.filter(email=email).exists():
            return "Student exists"
        student = cls.objects.create(name=name, email=email, phone=phone, password= make_password( password ) )
        return student  # Return the student object or a success message

    @classmethod
    def getAllStudents(cls):
        return list(cls.objects.values('name', 'email', 'phone'))


class StudentDetails(models.Model):
    applicationId = models.CharField(max_length=10, unique=True)
    motherName = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    email = models.OneToOneField(
        StudentCredentials,  
        on_delete=models.CASCADE, 
        to_field='email',
        related_name='details'
    )
    nationality = models.CharField(max_length=15)
    category = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=400)
    marksOf10th = models.DecimalField(max_digits=5, decimal_places=2)
    marksOf12th = models.DecimalField(max_digits=5, decimal_places=2)
    schoolOf10th = models.CharField(max_length=200)
    collegeOf12th = models.CharField(max_length=200)

    def __str__(self):
        return self.applicationId

    @classmethod
    def insertStudent(cls, **kwargs):
        # Retrieve the StudentCredentials instance by email
        student_credentials = StudentCredentials.objects.filter(email=kwargs.get('email')).first()

        if not student_credentials:
            return "Student does not exist"
            
        # Check if a StudentDetails instance already exists for this email
        if cls.objects.filter(email=student_credentials).exists():
            return "Student details already exist for this email"

        kwargs.pop('email' , None )
        # Now, create the StudentDetails instance with the StudentCredentials object
        student = cls.objects.create(
            email=student_credentials , # Pass the StudentCredentials instance, not the email string
            **kwargs
        )

        return {'success': True, 'student': student}


    @classmethod
    def getPrevApplicationId(cls):
        last_student = cls.objects.order_by('-id').first()
        if last_student :
            return last_student.applicationId
        else :
            return 0 
     

    @classmethod
    def studentExists(cls, email):
        
        if cls.objects.filter(email=email).exists() :
            return True
        else : 
            return False 

    @classmethod
    def getApplicantId(cls , email ):
        if cls.objects.filter(email = email).exists():
            return cls.objects.values('applicationId').get(email = email )
        else :
            return None 
            
            
    @classmethod
    def getStudentInfo(cls, email):
        try:
          if cls.objects.filter(email = email ).exists():
            student =  cls.objects.get(email=email)
            return {"success": True, "student": student}
          else :
            return { 'success' : False , "message" : "student not exist"  }
        except cls.DoesNotExist:
            return {"success": False , "message": "Student Does Not Exits" }







class StudentDocuments(models.Model):
    email = models.OneToOneField(
        StudentCredentials, 
        on_delete=models.CASCADE, 
        to_field='email', 
        related_name='documents'
    )

    photoAndSignature = models.ImageField(upload_to='documents/photos/', storage=NoLockingFileSystemStorage())
    marksheetOf10th = models.ImageField(upload_to='documents/10th_marksheets/', storage=NoLockingFileSystemStorage())
    marksheetOf12th = models.ImageField(upload_to='documents/12th_marksheets/', storage=NoLockingFileSystemStorage())
    cetScoreCard = models.ImageField(upload_to='documents/cet_scorecards/', storage=NoLockingFileSystemStorage())
    schoolLC = models.ImageField(upload_to='documents/school_lcs/', storage=NoLockingFileSystemStorage())
    collegeLC = models.ImageField(upload_to='documents/college_lcs/', storage=NoLockingFileSystemStorage())
    casteCertificate = models.ImageField(upload_to='documents/caste_certificates/', storage=NoLockingFileSystemStorage())
    casteValidityCertificate = models.ImageField(upload_to='documents/caste_validity_certificates/', storage=NoLockingFileSystemStorage())
    domicileCertificate = models.ImageField(upload_to='documents/domicile_certificates/', storage=NoLockingFileSystemStorage())
    incomeCertificate = models.ImageField(upload_to='documents/income_certificates/', storage=NoLockingFileSystemStorage())
    nonCreamyLayerCertificate = models.ImageField(upload_to='documents/non_creamy_layer_certificates/', storage=NoLockingFileSystemStorage())
    aadharCard = models.ImageField(upload_to='documents/aadhar_cards/', storage=NoLockingFileSystemStorage())


    photoAndSignatureVerified = models.CharField( max_length= 10 , default='pending')
    marksheetOf10thVerified = models.CharField(max_length=10 , default='pending')
    marksheetOf12thVerified = models.CharField(max_length=10 , default='pending')
    cetScoreCardVerified = models.CharField(max_length=10, default='pending')
    schoolLCVerified = models.CharField(max_length=10 , default='pending')
    collegeLCVerified = models.CharField(max_length=10 , default='pending' )
    casteCertificateVerified = models.CharField(max_length=10 , default='pending')
    casteValidityCertificateVerified = models.CharField( max_length= 10 , default='pending' )
    domicileCertificateVerified = models.CharField(max_length= 10 , default='pending')
    incomeCertificateVerified = models.CharField( max_length= 10 , default='pending')
    nonCreamyLayerCertificateVerified = models.CharField(max_length=10 , default='pending')
    aadharCardVerified = models.CharField(max_length=10 , default='pending')



    photoAndSignatureReason = models.CharField( max_length= 1000 , default='')
    marksheetOf10thReason = models.CharField(max_length=1000 , default='')
    marksheetOf12thReason = models.CharField(max_length=1000 , default='')
    cetScoreCardReason = models.CharField(max_length=1000 , default='')
    schoolLCReason = models.CharField(max_length=1000 , default='')
    collegeLCReason = models.CharField(max_length=1000 , default='' )
    casteCertificateReason = models.CharField(max_length=1000 , default='')
    casteValidityCertificateReason = models.CharField( max_length= 1000 , default='' )
    domicileCertificateReason = models.CharField(max_length= 1000 , default='')
    incomeCertificateReason = models.CharField( max_length= 1000 , default='')
    nonCreamyLayerCertificateReason = models.CharField(max_length=1000 , default='')
    aadharCardReason = models.CharField(max_length=1000 , default='')



    def __str__(self):
        return self.email.name

    @classmethod
    def getPhotoAndSignature(cls, email):
        try:
            studentDocuments = cls.objects.get(email=email)
            photo = getattr(studentDocuments, "photoAndSignature", None)
            if photo:
                return {'success': True, 'photo': photo.url}
            else:
                return {'success': False, 'message': "Photo and signature not uploaded."}
        except cls.DoesNotExist:
            return {'success': False, 'message': "Student does not exist."}



    @classmethod
    def getAllDocuments(cls, email):
       
        def formatKey(input_string):
            # Insert a space before each capital letter (excluding the first one)
            formatted = re.sub(r'(?<!\d)(\d)', r' \1', input_string, count=1)
            # Insert a space before each capital letter (excluding the first one)
            formatted = re.sub(r'(?<!^)(?=[A-Z])', ' ', formatted)
            #formatted = re.sub(r'(?<!^)(?=[A-Z0-9])', ' ', input_string)
            # Capitalize the first letter of each word
            formatted = formatted.title()
            return formatted

        try:
            studentDocuments = cls.objects.get(email=email)
            documentDict = {}

            for field in cls._meta.fields:
    
                if field.name != 'photoAndSignature' and field.name != 'email':
                    documentValue = getattr(studentDocuments, field.name, None)
                    if isinstance(field, (models.ImageField, models.FileField)):
                        documentDict[ formatKey(field.name) ] = {
                            'name' : field.name ,
                            'url': documentValue.url if documentValue else None,  # Add URL if exists
                            'verified': getattr(studentDocuments, f'{field.name}Verified', None),  # Add verified status
                            'reason': getattr(studentDocuments , f'{field.name}Reason' , None ),
                        }

                    else:
                        pass

            return {'success': True, 'documents': documentDict}

        except cls.DoesNotExist:
            return {'success': False, 'message': "Student does not exist."}


    @classmethod
    def insertDocuments(cls, email, **kwargs):
        try:
            # Retrieve the StudentCredentials instance by email
            student_credentials = StudentCredentials.objects.filter(email=email).first()

            if not student_credentials:
                return {'success': False, 'message': f"Student with email {email} does not exist."}

            student_document, created = cls.objects.update_or_create(
                email=student_credentials,
                defaults=kwargs
            )
            return {'success': True, 'student': student_document}

        except Exception as e:
            return {'success': False, 'message': f"Error: {str(e)}"}


    @classmethod
    def updateDocument(cls, email, documentName, document):
        try:
            student_documents = cls.objects.get(email=email)
            if hasattr(student_documents, documentName):
                setattr(student_documents, documentName, document)
                student_documents.save()
                return f"{documentName} updated successfully."
            else:
                return f"{documentName} does not exist in the model."
        except cls.DoesNotExist:
            return "Student documents not found."




    @classmethod
    def insertPhotoAndSignature(cls, email, photo):
        try:
    
            student_credentials = StudentCredentials.objects.filter(email=email).first()
            if not student_credentials:
                return f"StudentCredentials not found for email: {email}"

            existing_document = cls.objects.filter(email=email).first()

            if existing_document:
                existing_document.photoAndSignature = photo
                existing_document.save()
                return f"Document updated successfully. Debug Info: {er}"
            else:
              
                if not photo or not hasattr(photo, 'file'):
                    return f"Invalid photo input: {type(photo)}"
                if not hasattr(photo, 'name'):
                    return "Photo is missing a valid name."

                student = cls.objects.create(email=student_credentials, photoAndSignature=photo)
                return  "inserted"
        except Exception as e:
            import traceback
            traceback_str = traceback.format_exc()
            return f"An error occurred. Debug Info: {er}\nError: {str(e)}\nTraceback:\n{traceback_str}"




    @classmethod
    def updateStatus(cls, email, updates):
        """
        Updates the verified and reason fields for a StudentDocuments instance directly in the database.

        Args:
            email (str): The email identifying the StudentDocuments instance to be updated.
            updates (dict): A dictionary containing field names as keys and their new values as values.
        """
        # Filter the StudentDocuments object by email
        obj = cls.objects.filter(email__email=email)

        if not obj.exists():
            raise ValueError(f"No StudentDocuments object found for email: {email}")

        # Update fields directly in the database
        obj.update(**updates)




