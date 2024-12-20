# Generated by Django 5.1.3 on 2024-12-03 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0002_studentdetails_studentdocuments"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentdocuments",
            name="aadharCardVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="casteCertificateVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="casteValidityCertificateVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="cetScoreCardVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="collegeLCVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="domicileCertificateVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="incomeCertificateVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="marksheetOf10thVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="marksheetOf12thVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="nonCreamyLayerCertificateVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="photoAndSignatureVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studentdocuments",
            name="schoolLCVerified",
            field=models.BooleanField(default=False),
        ),
    ]
