# from django.db import models
# from hospital.models import Doctor, Patient
#
# class Appointment(models.Model):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     appointment_date = models.DateTimeField()
#     symptoms = models.TextField()
#     status = models.CharField(max_length=15, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
#
#     def __str__(self):
#         return f"Appointment with Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"
#
