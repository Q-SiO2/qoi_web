from django.db import models

# Groups = Filière + Year
class StudentGroup(models.Model):
    filiere = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.filiere} - {self.year}"

# Student table
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name

# Staff & Admin tables
class Professor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Subject table (linked to prof)
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

# Sessions (class sessions with QR)
class Session(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    encoded_data = models.TextField(null=True, blank=True)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} on {self.session_date}"

# Attendance logs
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    scanned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'session')

    def __str__(self):
        return f"{self.student.name} - {self.status}"
