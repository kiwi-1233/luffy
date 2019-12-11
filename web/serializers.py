# from rest_framework import serializers
# from web import models


# class CourseSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = models.Course
#         fields = "__all__"

# class CourseChapterSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = models.CourseChapter
#         fields="__all__"
#         depth = 2

from rest_framework import serializers
from web import models

class HomeworkSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Homework
        fields = "__all__"
        depth = 3

class CourseChapterSerializers(serializers.ModelSerializer):

    class Meta:
        model=models.CourseChapter
        fields = "__all__"