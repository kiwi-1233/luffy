from django.contrib import admin
from web import models
# Register your models here.
admin.site.register(models.CourseCategory)
admin.site.register(models.CourseSubCategory)
admin.site.register(models.BigCourse)
admin.site.register(models.Course)
admin.site.register(models.CourseChapter)
admin.site.register(models.Homework)
admin.site.register(models.CourseSection)
admin.site.register(models.HomeworkRecord)
admin.site.register(models.Order)
admin.site.register(models.SubOrder)
admin.site.register(models.Coupon)
admin.site.register(models.CouponRecord)
admin.site.register(models.EnrolledBigCourse)
admin.site.register(models.EnrolledCourse)
admin.site.register(models.Account)

