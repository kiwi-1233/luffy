from django.conf import settings
settings.configure()
import django
django.setup()

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

class Comment(object):
    def __init__(self, name,age,mobile):
        self.name = name
        self.age = age
        self.mobile = mobile

comment = Comment(name='Hf',age='22',mobile='18875707124')

class CommentSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.CharField()
    mobile = serializers.CharField()


    def create(self,validated_data):
        return Comment(**validated_data)

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.age = validated_data.get('age',instance.age)
        instance.mobile = validated_data.get('mobile',instance.mobile)
        return instance
dic = {
    'name':'GY',
    'age':'22',
    'mobile':'11111111111'
}

serializer = CommentSerializer(instance=comment,data=dic)
print(serializer.is_valid())
print(serializer.save())
print(comment.__dict__)
