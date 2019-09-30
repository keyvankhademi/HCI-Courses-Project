from django.db import models

# Create your models here.


class University(models.Model):
    name = models.CharField(max_length=100, verbose_name="University Name", unique=True)


class Course(models.Model):
    name = models.CharField(max_length=500, verbose_name="Course Name", null=False, blank=True)
    code = models.CharField(max_length=100, verbose_name="Course Code", null=False, blank=True)
    university = models.ForeignKey(University, verbose_name="University", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Course Description", null=False, blank=True)

    url = models.URLField(verbose_name="Most Recent Course Website", null=True)
    prerequisites = models.CharField(verbose_name="Course Prerequisites", max_length=500, null=True)
    core_for_major = models.BooleanField(verbose_name="Core for Major?", null=False)
    last_taught = models.DateField(verbose_name="Last Taught")
    instructor = models.CharField(verbose_name="Most Recent Instructor", max_length=100, null=False, blank=True)
    learning_goals = models.TextField(verbose_name="Learning outcome/goals", null=False, blank=True)

    equivalent = models.ManyToManyField('self', symmetrical=True, blank=True)

    class Meta:
        unique_together = ['code', 'university']


class Criteria(models.Model):
    name = models.CharField(verbose_name="Criteria Name", max_length=100, null=False, blank=True)
    weight = models.FloatField(verbose_name="Criteria Weight")
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'course']


class Topic(models.Model):
    week = models.IntegerField(verbose_name="Number of the Week in Which This Topic Is Taught", null=False)
    description = models.CharField(max_length=500, verbose_name="Topic Description")
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['week', 'course']
