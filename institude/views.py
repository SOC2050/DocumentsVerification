from django.shortcuts import render , redirect 

from student.models import StudentCredentials , StudentDetails , StudentDocuments 

# Create your views here.


def instituteDashboard(request):
    def documentStatus(docs):
        dic = {}
        for value in docs.values():
            if value.get("verified") == "rejected":
                dic[value['name']] = "rejected"
            elif value.get("verified") == "approved":
                dic[value['name']] = "approved"
            elif value.get("verified") == "pending":
                dic[value['name']] = "pending"

        if "rejected" in dic.values():
            return "rejected"
        elif all(status == "approved" for status in dic.values()):
            return "approved"
        else:
            return "pending"

    if request.session.get('login', False):
        section = request.GET.get('section', '').strip()
        email = request.GET.get('email', '').strip()

        print(f"Section: {section}")  # Debugging

        # Default response
        response = render(request, 'institude/instituteDashboard.html')

        if section == "allApplication":
            print("Inside allApplication section")  # Debugging
            allStudent = StudentCredentials.getAllStudents()
            for student in allStudent:
                id = StudentDetails.getApplicantId(student['email'])
                if id:
                    student['id'] = id.get('applicationId')
                    doc = StudentDocuments.getAllDocuments(student['email'])
                    if doc['success']:
                        stddocs = doc['documents']
                        student['status'] = documentStatus(stddocs)

            filtered_students = [student for student in allStudent if 'id' in student and student['id'] is not None]
            response = render(request, "institude/instituteDashboard.html", 
                              {'section': section, 'students': filtered_students})

        elif section == "studentApplication":
            print("Inside studentApplication section")  # Debugging
            studentBasicDetails = StudentCredentials.getStudentInfo(email)
            studentApplicationDetails = StudentDetails.getStudentInfo(email)
            docs = StudentDocuments.getAllDocuments(email)
            if docs['success']:
                finalSubmition = documentStatus(docs['documents'])
                
            print(docs['documents'])
            studentPhoto = StudentDocuments.getPhotoAndSignature(email)
            if studentBasicDetails['success'] and studentApplicationDetails['success']:
                values = {
                    'photo': studentPhoto['photo'] if studentPhoto['success'] else '',
                    'applicationId': studentApplicationDetails['student'].applicationId,
                    'applicantName': studentBasicDetails['student'].name,
                    'email': studentBasicDetails['student'].email,
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
   
                    # Other student details...
                }
                response = render(request, 'institude/instituteDashboard.html', 
                                  {'section': section, 'values': values, 'docs': docs['documents'] ,     'finalSubmition': finalSubmition})

        elif section == "updateDocs":
            
            """
            print("Inside student  update  section")  # Debugging
            studentBasicDetails = StudentCredentials.getStudentInfo(email)
            studentApplicationDetails = StudentDetails.getStudentInfo(email)
            docs = StudentDocuments.getAllDocuments(email)
            if docs['success']:
                finalSubmition = documentStatus(docs['documents'])
            """
            studentBasicDetails = StudentCredentials.getStudentInfo(email)
            studentPhoto = StudentDocuments.getPhotoAndSignature(email)
            
            if studentBasicDetails['success'] :
                
                values = {
                    'photo': studentPhoto['photo'] if studentPhoto['success'] else '',
                    'applicantName': studentBasicDetails['student'].name,
                    'email': studentBasicDetails['student'].email,
                    'contactNumber': studentBasicDetails['student'].phone ,
                }



          
            docsInfo = {}
            fields = [
             'marksheetOf10th', 'marksheetOf12th',
            'cetScoreCard', 'schoolLC', 'collegeLC', 'casteCertificate',
            'casteValidityCertificate', 'domicileCertificate', 'incomeCertificate',
            'nonCreamyLayerCertificate', 'aadharCard'
            ]
            
            for name in fields :
                
                #print(name)
                data = request.POST.get( name , '' )
                #print(data)
                datareason = ''
                if data != '' and data =="rejected" :
                   
                    datareason = request.POST.get( f'{name}_reason' , '' )
                    
                docsInfo[ f'{ name }Verified']=  data 
                docsInfo[f'{ name }Reason']= datareason



            
            # Create a list of keys to remove (to avoid modifying the dictionary while iterating)
            keys_to_remove = []

            # Loop through the dictionary in pairs of verified and reason fields
            for key, value in docsInfo.items():
                if key.endswith('Verified') and value == '':
     
                    base_name = key[:-8]  
                    keys_to_remove.extend([key, f"{base_name}Reason"])

         
            for key in keys_to_remove:
               docsInfo.pop(key, None)  # Use `pop` with `None` to avoid KeyError if the key is not found

            print(docsInfo)
            
            StudentDocuments.updateStatus( email , docsInfo )
            
            documents = StudentDocuments.getAllDocuments(email)
            if documents['success']:
                finalSubmition = documentStatus(documents['documents'])
                

            
            
            response = render( request , 'institude/instituteDashboard.html' , { 'section' : 'updateDocs' , 'values':values  ,'docs' : documents['documents']    , 'formStatus' :  finalSubmition  })



        return response
    return redirect('home')

"""
# Example usage:
# Assume we know the email of the student document to be updated and have a dictionary of updates
email = "student@example.com"
updates = {
    'photoAndSignatureVerified': 'approved',
    'marksheetOf10thVerified': 'rejected',
    'marksheetOf10thReason': 'Incorrect document uploaded.',
    'aadharCardVerified': 'approved'
}

StudentDocuments.update_verified_and_reason_fields(email, updates)
"""

