import pandas as pd
import secrets  # For generating random passwords
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import Student, StudentGroup
from django.contrib.auth.hashers import make_password  # For hashing passwords

def upload_students(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            uploaded_file = request.FILES['file']

            try:
                # Read the Excel file using pandas
                df = pd.read_excel(uploaded_file, header=None)

                # Extract general information (filiere, annee, semestre)
                infos = df.iloc[3, 3]
                infos_split = [x.strip() for x in str(infos).split(';')]
                filiere = infos_split[0] if len(infos_split) > 0 else None
                annee = infos_split[1] if len(infos_split) > 1 else None
                semestre = infos_split[2] if len(infos_split) > 2 else None

                if not filiere or not annee or not semestre:
                    messages.error(request, "Filiere, annee, or semester information is missing in the file.")
                    return redirect('upload_students')

                # Create or get the StudentGroup
                group, created = StudentGroup.objects.get_or_create(filiere=filiere, year=annee)

                # Process student data
                for index, row in df.iloc[4:].iterrows():
                    nom_prenom = row[3]
                    email = row[5] if len(row) > 5 else ""

                    if pd.isna(nom_prenom):
                        messages.error(request, f"Error: Empty 'Nom Prenom' at row {index + 1}. Skipping.")
                        continue

                    # Generate a random password
                    random_password = secrets.token_urlsafe(8)  # Generate an 8-character random password
                    hashed_password = make_password(random_password)  # Hash the password

                    # Create a new student
                    Student.objects.create(
                        name=nom_prenom,
                        email=email,
                        student_id=f"ID-{index + 1}",  # Generate a unique ID
                        password_hash=hashed_password,  # Save the hashed password
                        group=group
                    )

                    # Log the generated password (for sending to the user)
                    print(f"Generated password for {nom_prenom}: {random_password}")

                messages.success(request, "Students uploaded successfully!")
                return redirect('upload_students')

            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = UploadFileForm()

    return render(request, 'upload_students.html', {'form': form})