from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Evaluation


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=50)

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        return User.objects.create(email, email, password)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('email', instance.email)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class EvaluationSerializer(serializers.Serializer):
    id= serializers.ReadOnlyField()
    remote_id = serializers.IntegerField()
    candidate_name = serializers.CharField(max_length=20)
    job_title = serializers.CharField(max_length=20)
    interviewer_name = serializers.CharField(max_length=20)
    interview_date = serializers.DateField()
    communication = serializers.IntegerField()
    problem_solving = serializers.IntegerField()
    conflict_resolution = serializers.IntegerField()
    teamwork = serializers.IntegerField()
    work_experience = serializers.IntegerField()
    educational_background = serializers.IntegerField()
    leadership = serializers.IntegerField()
    comments = serializers.CharField(max_length=300)
    total = serializers.IntegerField()

    def create(self, validated_data):
        '''remote_id = validated_data['remote_id']
        candidate_name = validated_data['candidate_name']
        job_title = validated_data['job_title']
        interviewer_name = validated_data['interviewer_name']
        interview_date = validated_data['interview_date']
        communication = validated_data['communication']
        problem_solving = validated_data['problem_solving']
        conflict_resolution = validated_data['conflict_resolution']
        teamwork = validated_data['teamwork']
        work_experience = validated_data['work_experience']
        educational_background = validated_data['educational_background']
        leadership = validated_data['leadership']
        comments = validated_data['comments']
        total = validated_data['total'] '''

        return Evaluation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
        '''instance.remote_id = validated_data.get('remote_id', instance.remote_id)
        instance.candidate_name = validated_data.get('candidate_name', instance.candidate_name)
        instance.job_title = validated_data.get('job_title', instance.job_title)
        instance.interviewer_name = validated_data.get('interviewer_name', instance.interviewer_name)
        instance.interview_date = validated_data.get('interview_date', instance.interview_date)
        instance.communication = validated_data.get('communication', instance.communication)
        instance.problem_solving = validated_data.get('problem_solving', instance.problem_solving)
        instance.conflict_resolution = validated_data.get('conflict_resolution', instance.conflict_resolution)
        instance.teamwork = validated_data.get('teamwork', instance.teamwork)
        instance.work_experience = validated_data.get('work_experience', instance.work_experience)
        instance.educational_background = validated_data.get('educational_background', instance.educational_background)
        instance.leadership = validated_data.get('leadership', instance.leadership)
        instance.comments = validated_data.get('candidate_name', instance.comments)

        instance.save()
        return instance'''


