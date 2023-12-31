# Generated by Django 4.2.5 on 2023-10-06 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("courses", "0004_alter_course_professor"),
        ("enrollments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enrollment",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="courses.course"
            ),
        ),
        migrations.AlterField(
            model_name="enrollment",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="users.student"
            ),
        ),
    ]
