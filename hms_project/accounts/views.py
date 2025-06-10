from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username=request.POST.get("username") #(get)Django grabs data that the user submitted through an HTML form (like name, email, password).
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        role = request.POST.get("role")

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            messages.error(request, "username already taken.")
            return redirect("register")

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Save role info to session temporarily (for post-login use)
        request.session["user_role"] = role

        messages.success(request, "Registration successful. Please log in.")
        return redirect("login")  # Make sure this matches your login URL name

    return render(request, "register.html")




from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages





from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from hospital.models import Patient  # import your Patient model
from django.contrib.messages import get_messages
def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Please fill all fields.")
            error = "Please fill all fields."
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    auth_login(request, user)
                    list(get_messages(request))
                    return redirect('admin_dashboard')

                # Check if user is patient
                try:
                    patient = user.patient  # OneToOneField relation from Patient to User
                    auth_login(request, user)
                    list(get_messages(request))
                    return redirect('patient_dashboard')
                except Patient.DoesNotExist:
                    error = "You are not authorized to access this site."
            else:
                error = "Invalid username or password."

    return render(request, "login.html", {"error": error})


from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from hospital.models import Doctor,Patient,Appointment
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login_view')
    doctor=Doctor.objects.all()
    patient=Patient.objects.all()
    appointment=Appointment.objects.all()

    d=0;  #counts the total number of doctors, patients, and appointments by going through each list and adding 1 for each item.
    p=0;
    a=0;
    for i in doctor:
        d+=1
    for i in patient:
        p+=1
    for i in appointment:
        a+=1

    context={'d':d,'p':p,'a':a}#sends the counts to the webpage (admin_dashboard.html) as variables named d, p, and a.
                                #The webpage can then show these numbers to the admin.


    return render(request,'admin_dashboard.html',context)



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from hospital.models import Patient,Speciality  # Assuming Patient is in the same app

from django.contrib.messages import get_messages

def patient_register(request):
    if request.method == 'POST':
        # your existing POST handling code
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        name = request.POST['name']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        address = request.POST['address']
        dob = request.POST['dob']

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        patient = Patient.objects.create(
            user=user,
            name=name,
            gender=gender,
            mobile=mobile,
            address=address,
            email=email,
            dob=dob
        )

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login_view')

    # Clear old messages so they don't appear on fresh GET requests
    list(get_messages(request))

    return render(request, 'patient_register.html')

@login_required
def patient_dashboard(request):
    specialities = Speciality.objects.all()

    if request.method == 'POST':
        speciality_id = request.POST.get('speciality')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')

        try:
            patient = request.user.patient  # assuming OneToOneField
            doctor = Doctor.objects.get(id=doctor_id)

            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=date,
                time=time
            )

            messages.success(request, "Appointment booked successfully.")
            return redirect('hospital:appointment_success')

        except Exception as e:
            messages.error(request, f"Error booking appointment: {str(e)}")

    return render(request, 'patient_dashboard.html', {
        'specialities': specialities
    })
