from django.db import models

from django.db.models import CharField



class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/images', blank=True, null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):

    name=models.CharField(max_length=20)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    mobile = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name



from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)


    name = models.CharField(max_length=20)

    gender = models.CharField(max_length=10)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    mobile = models.BigIntegerField(null=True, blank=True)
    address=models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)  # Adding email
    dob = models.DateField(null=True, blank=True)  # Optional: To track Date of Birth


    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()


    def __str__(self):
        return self.doctor.name+"__"+self.patient.name
