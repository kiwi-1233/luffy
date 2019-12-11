from django.shortcuts import render

# Create your views here.
from  rest_framework.viewsets import ModelViewSet
from web.serializers import HomeworkSerializers,CourseChapterSerializers
from web import models


# class CourseViewSet(ModelViewSet):
#     queryset = models.Course.objects.all()
#     serializer_class = CourseSerializers

# class CourseChapterViewSet(ModelViewSet):
#     queryset = models.CourseChapter.objects.all()
#     serializer_class = CourseChapterSerializers


class HomeWorkChapterViewSet(ModelViewSet):
    queryset = models.Homework.objects.all()
    serializer_class = HomeworkSerializers

class CourseChapterViewSet(ModelViewSet):
    queryset = models.CourseChapter.objects.all()
    serializer_class = CourseChapterSerializers