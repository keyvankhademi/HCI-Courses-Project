from django.contrib.auth.models import User
from django.db import models
import string
import random


# Create your models here.


def generate_slug():
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for i in range(10))


CATEGORY_CHOICES = {
    ('Human-Computer Interaction', 'Human-Computer Interaction'),
    ('Computational Mathematics', 'Computational Mathematics'),
}


class University(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, verbose_name="University Name", unique=True, null=False, blank=False)
    short_name = models.CharField(max_length=100, verbose_name="University Short Name", null=False, blank=False)

    def __str__(self):
        return str(self.name)


class Course(models.Model):
    slug = models.CharField(max_length=10, default=generate_slug, verbose_name="Slug", null=False, blank=False,
                            editable=False, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=500, verbose_name="Course Name", null=False, blank=True)
    code = models.CharField(max_length=100, verbose_name="Course Code", null=False, blank=True)
    university = models.ForeignKey(University, verbose_name="University", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Course Description", null=False, blank=True)
    category = models.CharField(max_length=500, verbose_name="Category Name", choices=CATEGORY_CHOICES, null=False,
                                blank=False)

    url = models.URLField(verbose_name="Most Recent Course Website", null=True, blank=True)
    prerequisites = models.CharField(verbose_name="Course Prerequisites", max_length=500, null=True, blank=True)
    core_for_major = models.BooleanField(verbose_name="Core for Major?", null=False)
    last_taught = models.DateField(verbose_name="Last Taught", null=True, blank=True)
    instructor = models.CharField(verbose_name="Most Recent Instructor", max_length=100, null=False, blank=True)
    learning_goals = models.TextField(verbose_name="Learning outcome/goals", null=False, blank=True)
    complete = models.BooleanField(verbose_name="Is it complete", default=False)
    verified = models.BooleanField(verbose_name="Is it verified", default=False)

    equivalent = models.ManyToManyField('self', symmetrical=True, blank=True)

    def __str__(self):
        return "{} ({}) in {}".format(self.name, self.code, self.university)

    class Meta:
        unique_together = ['code', 'university']


class Criteria(models.Model):
    name = models.CharField(verbose_name="Criteria Name", max_length=100, null=False, blank=True)
    weight = models.FloatField(verbose_name="Criteria Weight")
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} in {}".format(self.name, self.weight, self.course.name)

    class Meta:
        unique_together = ['name', 'course']


class Topic(models.Model):
    week = models.IntegerField(verbose_name="Number of the Week in Which This Topic Is Taught", null=False)
    description = models.CharField(max_length=800, verbose_name="Topic Description")
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)

    def __str__(self):
        return "topic of week {} for {}".format(self.week, self.course.name)

    class Meta:
        unique_together = ['week', 'course']
