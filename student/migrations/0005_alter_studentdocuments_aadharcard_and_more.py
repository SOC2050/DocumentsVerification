# Generated by Django 5.1.3 on 2024-12-04 15:48

import student.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0004_remove_studentdetails_fullname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentdocuments",
            name="aadharCard",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/aadhar_cards/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="casteCertificate",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/caste_certificates/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="casteValidityCertificate",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/caste_validity_certificates/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="cetScoreCard",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/cet_scorecards/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="collegeLC",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/college_lcs/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="domicileCertificate",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/domicile_certificates/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="incomeCertificate",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/income_certificates/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="marksheetOf10th",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/10th_marksheets/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="marksheetOf12th",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/12th_marksheets/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="nonCreamyLayerCertificate",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/non_creamy_layer_certificates/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="photoAndSignature",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/photos/",
            ),
        ),
        migrations.AlterField(
            model_name="studentdocuments",
            name="schoolLC",
            field=models.ImageField(
                storage=student.storage_backends.NoLockingFileSystemStorage(),
                upload_to="documents/school_lcs/",
            ),
        ),
    ]
