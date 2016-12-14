from django.db import models

# Create your models here.


class Evaluation(models.Model):
    remote_id = models.IntegerField(unique=True)
    candidate_name = models.CharField(max_length=20)
    job_title = models.CharField(max_length=20)
    interviewer_name = models.CharField(max_length=20)
    interview_date = models.DateField()
    communication = models.PositiveSmallIntegerField()
    problem_solving = models.PositiveSmallIntegerField()
    conflict_resolution = models.PositiveSmallIntegerField()
    teamwork = models.PositiveSmallIntegerField()
    work_experience = models.PositiveSmallIntegerField()
    educational_background = models.PositiveSmallIntegerField()
    leadership = models.PositiveSmallIntegerField()
    comments = models.TextField()
    total = models.IntegerField()

    def __str__(self):
        return self.candidate_name



