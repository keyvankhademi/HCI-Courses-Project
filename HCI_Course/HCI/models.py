from django.db import models

# Create your models here.


class University(models.Model):
    name = models.CharField(max_length=100, name="University Name", verbose_name="University Name")


class Course(models.Model):
    name = models.CharField(max_length=500, name="Course Name", verbose_name="Course Name", null=False, blank=True)
    code = models.CharField(max_length=100, name="Course Code", verbose_name="Course Code", null=False, blank=True)
    university = models.ForeignKey(University, name="University", verbose_name="University", on_delete=models.CASCADE)
    description = models.TextField(name="Course Description", verbose_name="Course Description", null=False, blank=True)

    url = models.URLField(name="Course Website", verbose_name="Most Recent Course Website", null=True)
    prerequisites = models.CharField(name="Course Prerequisites", verbose_name="Course Prerequisites", max_length=500, null=True)
    core_for_major = models.BooleanField(name="Core for Major?", verbose_name="Core for Major?", null=False)
    last_taught = models.DateField(name="Last Taught", verbose_name="Last Taught")
    instructor = models.CharField(name="Instructor", verbose_name="Most Recent Instructor", max_length=100, null=False, blank=True)
    learning_goals = models.TextField(name="Learning Goals", verbose_name="Learning outcome/goals", null=False, blank=True)

    equivalent = models.ManyToManyField('self', symmetrical=True)


class Criteria(models.Model):
    name = models.CharField(name="Criteria Name", verbose_name="Criteria Name", max_length=100, null=False, blank=True)
    weight = models.FloatField(name="Criteria Weight", verbose_name="Criteria Weight")
    course = models.ForeignKey(Course, name="Course", verbose_name="Course", on_delete=models.CASCADE)


class Topic(models.Model):
    week = models.IntegerField(name="Number of the Week", verbose_name="Number of the Week in Which This Topic Is Taught", null=False)
    description = models.CharField(max_length=500, name="Topic Description", verbose_name="Topic Description")

