

from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404

from .models import Doctor, Speciality


# Create your views here.

def home(request):
    s = Speciality.objects.all()  # Query all specialties (or doctors) and pass to the template
    context = {'s': s}
    return render(request, 'home.html', context)  # Render the home page for non-logged-in users







def contact(request):
    return render(request,'contact.html')

from .models import Doctor
def view_doctor(request):
    if not request.user.is_staff:
        return redirect('login_view')
    doc=Doctor.objects.all()
    d={'doc':doc}
    return render(request,'view_doctor.html',d)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doctor, Speciality

def add_doctor(request):
    # Fetch all specializations from the database
    specialities = Speciality.objects.all() # gets all the medical specialties from the database (like cardiology, dermatology) to show in a dropdown list in the form.

    if request.method == 'POST':
        try:
            # Fetching data from the form
            name = request.POST.get('name')
            speciality_id = request.POST.get('speciality')
            contact = request.POST.get('contact')

            # Check if all fields are filled
            if not name or not speciality_id or not contact:
                messages.error(request, 'All fields are required!')
                return redirect('add_doctor')  # Redirect back to the form if fields are missing

            # Get the specialization object
            speciality = Speciality.objects.get(id=speciality_id) #gets the full Speciality object from the database using its ID.



            # Create and save the new doctor object
            doctor = Doctor(name=name, speciality=speciality, mobile=contact)
            doctor.save()

            # Show a success message (optional, but can be helpful)
            messages.success(request, 'Doctor added successfully!')

            # Redirect to the 'view_doctor' page after successful submission
            return redirect('hospital:view_doctor')  # This will take the user to the doctor list page

        except Exception as e:
            # Catch any exception and show the error message
            messages.error(request, 'Something went wrong. Please try again.')

            # Redirect to the same page to display the error message
            return redirect('hospital:add_doctor')
    return render(request, 'add_doctor.html', {'specialities': specialities})





# View for deleting a doctor
def delete_doctor(request, id):
    try:
        # Get the doctor to be deleted
        doctor = Doctor.objects.get(id=id)
        doctor.delete()  # Delete the doctor from the database

        messages.success(request, "Doctor deleted successfully!")  # Success message
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor not found. Please try again.")  # Error message if doctor doesn't exist

    return redirect('hospital:view_doctor')  # Redirect back to the doctor list page (or any other page)

from .models import Patient
def view_patient(request):
    if not request.user.is_staff:
        return redirect('login_view')
    pat=Patient.objects.all()
    p={'pat':pat}
    return render(request,'view_patient.html',p)


def delete_patient(request, id):
    try:
        # Get the doctor to be deleted
        patient = Patient.objects.get(id=id)
        patient.delete()  # Delete the patient from the database

        messages.success(request, "Patient deleted successfully!")  # Success message
    except Patient.DoesNotExist:
        messages.error(request, "Patient not found. Please try again.")  # Error message if patient doesn't exist

    return redirect('hospital:view_patient')  # Redirect back to the patient list page (or any other page)



from .models import Patient

def add_patient(request):

    if request.method == 'POST':
        try:
            # Fetching data from the form
            name = request.POST.get('name')
            gender=request.POST.get('gender')
            mobile = request.POST.get('mobile')
            address=request.POST.get('address')
            email=request.POST.get('email')
            dob=request.POST.get('dob')

            # Check if all fields are filled
            if not name  or not gender or not mobile or not address or not email or not dob :
                messages.error(request, 'All fields are required!')
                return redirect('add_patient')  # Redirect back to the form if fields are missing


            # Create and save the new patient object
            patient = Patient(name=name, gender=gender, mobile=mobile, address=address,email=email,dob=dob)
            patient.save()

            # Show a success message (optional, but can be helpful)
            messages.success(request, 'Patient added successfully!')

            # Redirect to the 'view_patient' page after successful submission
            return redirect('hospital:view_patient')  # This will take the user to the patient list page

        except Exception as e:
            # Catch any exception and show the error message
            messages.error(request, 'Something went wrong. Please try again.')

            # Redirect to the same page to display the error message
            return redirect('hospital:add_patient')

    return render(request, 'add_patient.html')


from .models import Appointment, Doctor, Patient


def add_appointment(request):
    if not request.user.is_staff:
        return redirect('login_view')

    if request.method == 'POST':
        doctor_id = request.POST['doctor']
        patient_id = request.POST['patient']
        date = request.POST['date']
        time = request.POST['time']

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)


            # Create and save the new appointment
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                date=date,
                time=time
            )

            messages.success(request, "Appointment added successfully!")
            return redirect('hospital:view_appointment')  # Redirect to appointments list view

        except Doctor.DoesNotExist:
            messages.error(request, "Doctor not found!")
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found!")

    # Get all doctors and patients to show in the form
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    specialities = Speciality.objects.all()

    return render(request, 'add_appointment.html', {'doctors': doctors, 'patients': patients, 'specialities': specialities })


from .models import Appointment

def view_appointment(request):
    if not request.user.is_staff:
        return redirect('login_view')

    appointments = Appointment.objects.select_related('doctor', 'patient', 'doctor__speciality').all()

    return render(request, 'view_appointment.html', {
        'appointments': appointments
    })



from django.http import JsonResponse
from .models import Doctor

def get_doctors_by_speciality(request):
    if request.method == "GET" :  #checks if the request is a GET request (like when you search or ask for info from the server).
        speciality_id = request.GET.get('speciality_id') #It tries to get the specialty ID that was passed in the URL.
        doctors = Doctor.objects.filter(speciality_id=speciality_id) #finds all doctors in the database who belong to that specialty.



        doctor_data = [] #This creates a clean list (dictionary list) of each doctor’s
        for doctor in doctors:
            doctor_data.append({
                'id': doctor.id,
                'name': doctor.name,
            })

        return JsonResponse({'doctors': doctor_data}) #Instead of giving a full HTML page, the server just sends data — like a list of doctors — in JSON format.

    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment

def delete_appointment(request, id):
    # Ensure the user is authenticated and has permission to delete
    if not request.user.is_staff:
        return redirect('login_view')

    # Fetch the appointment using the provided ID
    appointment = get_object_or_404(Appointment, id=id)

    # Delete the appointment
    appointment.delete()

    # Redirect to the appointments list with a success message
    return redirect('hospital:view_appointment')

def appointment_success(request):
    return render(request,'appointment_success.html')