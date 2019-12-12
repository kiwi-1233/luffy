from django.db import models
import random
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.

# ---------课程相关的表------------
class CourseCategory(models.Model):
    """课程大类""" # 后端开发-》PYTON ->django
    name = models.CharField(max_length=32,unique=True)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class CourseSubCategory(models.Model):
    """课程子类"""
    category = models.ForeignKey("CourseCategory",on_delete=models.CASCADE)
    name = models.CharField(max_length=32, )
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("category","name")


# 大课程
class BigCourse(models.Model):
    """
    name , pc_cover, h5_cover, recommend_period , service_period , pub_date, 奖学金 ，brief ,mentor_fee
    """
    name = models.CharField(max_length=64,unique=True)
    pc_cover_img = models.ImageField(upload_to="media", blank=True,null=True)
    h5_cover_img = models.ImageField(upload_to="media", blank=True,null=True)
    price = models.FloatField()
    recommend_period = models.IntegerField("推荐学习周期(d)")
    service_period = models.IntegerField("导师服务周期")
    brief = models.TextField(max_length=512)
    #teachers = models.ManyToManyField("Teacher")
    pub_date = models.DateField()
    study_num = models.PositiveIntegerField(default=random.randint(1,100))
    scholarship = models.IntegerField(default=50000,verbose_name="奖学金")

    def __str__(self):
        return self.name



# 课程表
class Course(models.Model):
    """

    name, image, price,video_hours, brief , teacher , course_type , level, pub_date , study_num
    attach_path , recommend_period,order , sub_category
    """
    name = models.CharField(max_length=64,unique=True)
    course_type_choices = ((0,"免费课"),(1,"实战"),(2,"大课模块"))
    course_type = models.SmallIntegerField(choices=course_type_choices)
    category = models.ForeignKey("CourseSubCategory",verbose_name="课程分类",on_delete=models.CASCADE)
    big_course = models.ForeignKey("BigCourse",blank=True,null=True,on_delete=models.CASCADE)
    pc_cover_img = models.ImageField(upload_to="media", blank=True,null=True)
    h5_cover_img = models.ImageField(upload_to="media", blank=True,null=True)
    price = models.FloatField()
    video_hours = models.IntegerField("时长(h)")
    brief = models.TextField(max_length=512)
    #teacher = models.ForeignKey("Teacher")
    level_choices = ((0,"初级"),(1,"进阶"),(2,"高级"))
    level = models.SmallIntegerField(choices=level_choices)
    pub_date = models.DateField()
    study_num = models.PositiveIntegerField(default=random.randint(1,100))
    attach_path = models.CharField(max_length=128,blank=True,null=True) #
    recommend_period = models.PositiveIntegerField()
    order = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    status_choices = ((0,"下线"),(1,"上线"))
    status = models.BooleanField(choices=status_choices)
    def __str__(self):
        return self.name

    # def save(self, *args,**kwargs):
    #     pass


# 章节表
class CourseChapter(models.Model):
    """
    章节表， name, course, brief , pub_date, order , date
    """
    course = models.ForeignKey("Course",on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    brief = models.TextField()
    pub_date = models.DateField()
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%s-%s" %(self.course,self.name)

    class Meta:
        unique_together = ("course","name")


class Homework(models.Model):
    """
    chapter, title, requirement, score_point, coin, recommend_period,date,
    """
    chapter = models.ForeignKey("CourseChapter", on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name="作业题目")
    order = models.PositiveSmallIntegerField("作业顺序", help_text="同一课程的每个作业之前的order值间隔1-2个数")
    homework_type_choices = ((0, '作业'), (1, '模块通关考核'))
    homework_type = models.SmallIntegerField(choices=homework_type_choices, default=0)
    requirement = models.TextField(verbose_name="作业需求")
    score_point = models.TextField(max_length=1024, verbose_name="踩分点")
    recommend_period = models.PositiveSmallIntegerField("推荐完成周期(天)", default=7)
    scholarship_value = models.PositiveSmallIntegerField("为该作业分配的奖学金(贝里)")
    note = models.TextField(blank=True, null=True)
    enabled = models.BooleanField(default=True, help_text="本作业如果后期不需要了，不想让学员看到，可以设置为False")

    class Meta:
        unique_together = ("chapter", "title")

    def __str__(self):
        return "%s - %s" % (self.chapter, self.title)



#  课时表
class CourseSection(models.Model):
    """
    name, chapter , video_time, section_type , date , free_trail, vid
    """
    name = models.CharField(max_length=64)
    chapter = models.ForeignKey("CourseChapter", on_delete=models.CASCADE)
    video_time = models.CharField(max_length=32)
    section_type_choices = ((0,"视频"),(1,"文档"))
    section_type = models.SmallIntegerField(choices=section_type_choices,default=0)
    vid = models.CharField(max_length=128)
    free_trail = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name




# ----------学习记录、作业、提问、评论-------------

# 小课 报名
class EnrolledCourse(models.Model):
    """
    account , course, enrolled_date, valid_begin_date, valid_end_date ,
    """
    account = models.ForeignKey("Account",on_delete=models.CASCADE)
    course = models.ForeignKey("Course", limit_choices_to=~Q(course_type=2),on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    valid_begin_date = models.DateField(verbose_name="有效期开始自")
    valid_end_date = models.DateField(verbose_name="有效期结束至")
    status_choices = ((0, '已开通'), (1, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=0)

    def __str__(self):
        return "%s:%s" % (self.account, self.course)


# 大课报名
class EnrolledBigCourse(models.Model):
    """
    account, big_course, enrolled_date, valid_begin_date, valid_end_date, mentor , init_scholorship ,mentor_fee.

    """
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    big_course = models.ForeignKey("BigCourse", on_delete=models.CASCADE)
    mentor_service_period = models.PositiveSmallIntegerField(verbose_name="服务周期(days)")  # 在这也纪录服务周期是为了防止后面课程服务期延长影响现有的学员周期 计算
    enrolled_date = models.DateTimeField(auto_now_add=True)
    valid_begin_date = models.DateField(verbose_name="有效期开始自", blank=True, null=True)  # 开通第一个模块时，再添加课程有效期，2年
    valid_end_date = models.DateField(verbose_name="有效期结束至", blank=True, null=True)
    status_choices = (
        (0, '在学中'),
        (1, '休学中'),
        (2, '已毕业'),
        (3, '超时结业'),
        (4, '报名成功(未开始学习)'),
        (5, '已放弃学习'),
        (6, '休学申请中'),
    )
    study_status = models.SmallIntegerField(choices=status_choices, default=4)
    mentor = models.ForeignKey("Account", verbose_name="导师", related_name='my_students',
                               blank=True, null=True, limit_choices_to={'role': 1}, on_delete=models.CASCADE)
    mentor_fee_balance = models.PositiveIntegerField("导师费用余额", help_text="这个学员的导师费用，每有惩罚，需在此字段同时扣除")
    initial_scholarship = models.IntegerField("初始奖学金")

    def __str__(self):
        return "%s:%s" % (self.account, self.big_course)

    class Meta:
        unique_together = ('account', 'big_course')


# 作业记录
class HomeworkRecord(models.Model):
    """
    homework,  submit_time, account , mentor, mentor_review, review_time,score ,
    obj.homeworkrecord_set
    [linux_chapter1,python_chaper2]

    homework->chapter->course->big_course

    homework->enrolled_bigcourse->big_course
    homework->enrolled_bigcourse->account

    直接关联enrolled_bigcourse的好处：
    1. 缩短查询路径
    2. 自动帮助完成了是否有权限交作业的逻辑验证

    """
    #account = models.ForeignKey("Account",)
    account = models.ForeignKey("EnrolledBigCourse",on_delete=models.CASCADE)
    homework = models.ForeignKey("Homework", on_delete=models.CASCADE)
    score_choices = ((100, 'A+'),(90, 'A'),
                     (85, 'B+'),(80, 'B'),
                     (70, 'B-'),(60, 'C+'),
                     (50, 'C'),(40, 'C-'),
                     (-1, 'D'),(0, 'N/A'),
                     (-100, 'COPY'),
                     )
    score = models.SmallIntegerField(verbose_name="分数", choices=score_choices, null=True, blank=True)
    mentor = models.ForeignKey("Account", related_name="my_stu_homework_record", limit_choices_to={'role': 1},
                               verbose_name="导师", on_delete=models.CASCADE)
    # 导师
    mentor_comment = models.TextField(verbose_name="导师批注", blank=True, null=True)
    status_choice = (
        (0, '待批改'),
        (1, '已通过'),
        (2, '不合格'),
    )
    status = models.SmallIntegerField(verbose_name='作业状态', choices=status_choice, default=0)
    submit_num = models.SmallIntegerField(verbose_name='提交次数', default=0)
    note = models.TextField(verbose_name="备注", blank=True, null=True, help_text="选填，后期还可加补")
    score_level_status = ((0, '优秀'), (1, '非常优秀'), (2, '教科书级别优秀'))
    date = models.DateTimeField("作业提交日期", auto_now_add=True)
    check_date = models.DateTimeField("作业批改日期", null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后一次修改日期")

    # homework_path = models.CharField(verbose_name='作业路径', max_length=256,blank=True,null=True) 作业路径可以动态拿到，没必要存
    # /data/big_course_id/account_id/homeworkrecord_id/ 动态路径例子
    def __str__(self):
        return "%s " % (self.homework)

    # class Meta:
    #     unique_together = ("homework", "student")
    #


# 提问表

# 评论表





# 订单

# 总订单表
class Order(models.Model):
    """
    order_num,pay_type, crate_time, paid_time,original_amount,  actual_amount , status,  third_party_order_num
    """
    account = models.ForeignKey("Account",on_delete=models.CASCADE)
    order_num = models.CharField(max_length=64, unique=True)
    pay_type_choices = ((0,"支付宝"),(1,"微信"),(2,"贝理"))
    pay_type = models.SmallIntegerField(choices=pay_type_choices)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="订单创建时间")
    paid_time = models.DateTimeField(blank=True,null=True,verbose_name="实际付款时间")
    actual_amount = models.FloatField("实际支付")
    status_choices = (
        (0,"待支付"),
        (1,"支付成功"),
        (2,"超时取消（用户自主）"),
        (3,"超时取消（系统自动）"),
        (4,"已退款"),
    )
    status = models.SmallIntegerField(choices=status_choices)
    third_party_order_num = models.CharField(max_length=128)

    def __str__(self):
        return "%s-%s" %(self.order_num,self.actual_amount)
    # 13

# 子订单
class SubOrder(models.Model):
    """
    order, content_type , account, actual_price, original_price, date , status,
    """
    #order_id
    order = models.ForeignKey("Order",on_delete=models.CASCADE)
    order_num = models.CharField(max_length=64, unique=True)
    #account = models.ForeignKey("Account",on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE) # bigcoure
    object_id = models.IntegerField() # 存实际关联到表里的具体的某条记录  # bigcourse --> python, 4
    content_object = GenericForeignKey('content_type', 'object_id')
    acutal_price = models.FloatField("实际价格")
    original_price = models.FloatField("原价")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="订单创建时间")
    paid_time = models.DateTimeField(blank=True,null=True,verbose_name="实际付款时间")
    status_choices = (
        (0,"待支付"),
        (1,"支付成功"),
        (2,"超时取消（用户自主）"),
        (3,"超时取消（系统自动）"),
        (4,"已退款"),
    )
    status = models.SmallIntegerField(choices=status_choices)

    def __str__(self):
        return "%s" % self.order


# 优惠券
class Coupon(models.Model):
    """
    nme ,
    coupon_type ,满减卷， 通用券，折扣券，
    using_range  , 专题， 大课，全场通用
    领取有效期1-20 25
    valid_days 7
    valid_begin_date 12.9
    valid_end_date  12.31
    coupon_nums
    account
    minmum_consume
    discount_val  0.8
    money_enquilent_value 等值货币
    """
    name = models.CharField(max_length=64, verbose_name="活动名称")
    brief = models.TextField(blank=True, null=True, verbose_name="优惠券介绍")
    using_range_choices = ((0, "全场通用",), (1, "实战小课专用",), (2, "学位课专用",),)
    using_range = models.SmallIntegerField(choices=using_range_choices, verbose_name="使用范围", default=0)
    coupon_type_choices = ((0, '代金券'), (1, '满减券'), (2, '折扣券'))
    coupon_type = models.SmallIntegerField(choices=coupon_type_choices, default=0, verbose_name="券类型")
    money_equivalent_value = models.FloatField(verbose_name="等值货币")
    off_percent = models.PositiveSmallIntegerField("折扣百分比", help_text="只针对折扣券，例7.9折，写.79", blank=True, null=True)
    minimum_consume = models.PositiveIntegerField("最低消费", default=0, help_text="仅在满减券时填写此字段")
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField("绑定课程", blank=True, null=True, help_text="可以把优惠券跟课程绑定")
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField("数量(张)", default=1)
    open_date = models.DateField("优惠券领取开始时间")
    close_date = models.DateField("优惠券领取结束时间")
    valid_begin_date = models.DateField(verbose_name="有效期开始时间")
    #valid_end_date = models.DateField(verbose_name="有效结束时间", blank=True, null=True)
    coupon_valid_days = models.PositiveIntegerField(verbose_name="优惠券有效期（天）", help_text="自券被领时开始算起")
    status_choices = ((0, "上线"), (1, "下线"))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def content_type_name(self):
        if self.content_type:
            return self.content_type.model

    def __str__(self):
        return "%s(%s)" % (self.get_coupon_type_display(), self.name)

    def save(self, *args, **kwargs):
        if self.coupon_valid_days == 0:
            raise ValueError("coupon_valid_days 有效期不能为0")
        if self.close_date < self.open_date:
            raise ValueError("close_date 优惠券领取结束时间必须晚于 open_date优惠券领取开始时间 ")
        if self.using_range == 0:
            if self.content_type or self.object_id:
                raise ValueError("使用范围不限的优惠券，不可以绑定课程")

        super(Coupon, self).save(*args, **kwargs)


class CouponRecord(models.Model):
    """
    account, coupon , get_time, use_time, status, coupon_code
    """
    coupon = models.ForeignKey("Coupon", on_delete=models.CASCADE)
    number = models.CharField("唯一优惠码",max_length=64, unique=True)
    account = models.ForeignKey("Account", blank=True, null=True, verbose_name="使用者", on_delete=models.CASCADE)
    status_choices = ((0, '未使用'), (1, '已使用'), (2, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    get_time = models.DateTimeField(blank=True, null=True, verbose_name="领取时间", help_text="用户领取时间")
    used_time = models.DateTimeField(blank=True, null=True, verbose_name="使用时间")
    order = models.ForeignKey("Order", blank=True, null=True, verbose_name="关联订单", on_delete=models.CASCADE)  # 一个订单可以有多个优惠券
    date = models.DateTimeField(auto_now_add=True, verbose_name="生成时间")

    def __str__(self):
        return '%s-%s-%s-%s' % (self.coupon, self.account, self.number, self.status)


# 积分相关

# 邀请、分享

# 账号、权限

# 题库

import hashlib
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class AccountManager(BaseUserManager):
    def create_user(self,mobile, email,name , password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            mobile=mobile,
            password=password,
            email=email,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            mobile= mobile,
            password=password,
            email=email,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """
    name , role, image, coin, wx_id, id_card, date , city , sex, age, uid,

    """
    mobile = models.CharField(max_length=11,unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(verbose_name='staff status', default=False, help_text='决定着用户是否可登录管理后台')
    is_admin = models.BooleanField(default=False)
    uid = models.CharField(max_length=64, unique=True)  # 随机自动生成, 与第3方交互用户信息时，用这个uid,以避免泄露敏感用户信息
    wx_openid = models.CharField(max_length=128, blank=True, null=True)
    alipay_card = models.CharField(max_length=128, blank=True, null=True, verbose_name="支付宝账户")
    gender_choices = ((0, '保密'), (1, '男'), (2, '女'))
    gender = models.SmallIntegerField(choices=gender_choices, default=0, verbose_name="性别")
    id_card = models.CharField(max_length=32, blank=True, null=True, verbose_name="身份证号或护照号")
    name = models.CharField(max_length=32, default="", verbose_name="真实姓名")
    head_img = models.CharField(max_length=256, default='/static/frontend/head_portrait/logo@2x.png',
                                verbose_name="个人头像")
    role_choices = ((0, '学员'), (1, '导师'), (2, '讲师'), (3, '管理员'), (4, '班主任'))
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="角色")
    coin_balance = models.PositiveIntegerField(default=0, verbose_name="贝里余额")  # 每发生一笔积分交易，此处要变更，此字段为唯一准确值
    source_choices = ((0,'自主注册'),(1,'用户邀请'))
    source = models.SmallIntegerField(choices=source_choices,default=0)
    memo = models.TextField('备注', blank=True, null=True, default=None, help_text="json格式存储")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")


    objects = AccountManager()

    USERNAME_FIELD = 'mobile' # 用户名字段
    REQUIRED_FIELDS = ['email',"name"] # 在crete_superuser时必填字段

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        if not self.pk: # first time create this user
            # This code only happens if the objects is not in the database yet. Otherwise it would have pk
            m = hashlib.md5()
            m.update(str(self.mobile).encode(encoding="utf-8")) # username 是唯一址，所以把它做成唯一的uid是可以的
            self.uid = m.hexdigest()
        super(Account, self).save(*args, **kwargs)
