# Generated by Django 2.0.6 on 2019-12-10 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('mobile', models.CharField(max_length=11, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False, help_text='决定着用户是否可登录管理后台', verbose_name='staff status')),
                ('is_admin', models.BooleanField(default=False)),
                ('uid', models.CharField(max_length=64, unique=True)),
                ('wx_openid', models.CharField(blank=True, max_length=128, null=True)),
                ('alipay_card', models.CharField(blank=True, max_length=128, null=True, verbose_name='支付宝账户')),
                ('gender', models.SmallIntegerField(choices=[(0, '保密'), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('id_card', models.CharField(blank=True, max_length=32, null=True, verbose_name='身份证号或护照号')),
                ('name', models.CharField(default='', max_length=32, verbose_name='真实姓名')),
                ('head_img', models.CharField(default='/static/frontend/head_portrait/logo@2x.png', max_length=256, verbose_name='个人头像')),
                ('role', models.SmallIntegerField(choices=[(0, '学员'), (1, '导师'), (2, '讲师'), (3, '管理员'), (4, '班主任')], default=0, verbose_name='角色')),
                ('coin_balance', models.PositiveIntegerField(default=0, verbose_name='贝里余额')),
                ('source', models.SmallIntegerField(choices=[(0, '自主注册'), (1, '用户邀请')], default=0)),
                ('memo', models.TextField(blank=True, default=None, help_text='json格式存储', null=True, verbose_name='备注')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BigCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('pc_cover_img', models.ImageField(blank=True, null=True, upload_to='media')),
                ('h5_cover_img', models.ImageField(blank=True, null=True, upload_to='media')),
                ('price', models.FloatField()),
                ('recommend_period', models.IntegerField(verbose_name='推荐学习周期(d)')),
                ('service_period', models.IntegerField(verbose_name='导师服务周期')),
                ('brief', models.TextField(max_length=512)),
                ('pub_date', models.DateField()),
                ('study_num', models.PositiveIntegerField(default=5)),
                ('scholarship', models.IntegerField(default=50000, verbose_name='奖学金')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='活动名称')),
                ('brief', models.TextField(blank=True, null=True, verbose_name='优惠券介绍')),
                ('using_range', models.SmallIntegerField(choices=[(0, '全场通用'), (1, '实战小课专用'), (2, '学位课专用')], default=0, verbose_name='使用范围')),
                ('coupon_type', models.SmallIntegerField(choices=[(0, '代金券'), (1, '满减券'), (2, '折扣券')], default=0, verbose_name='券类型')),
                ('money_equivalent_value', models.FloatField(verbose_name='等值货币')),
                ('off_percent', models.PositiveSmallIntegerField(blank=True, help_text='只针对折扣券，例7.9折，写.79', null=True, verbose_name='折扣百分比')),
                ('minimum_consume', models.PositiveIntegerField(default=0, help_text='仅在满减券时填写此字段', verbose_name='最低消费')),
                ('object_id', models.PositiveIntegerField(blank=True, help_text='可以把优惠券跟课程绑定', null=True, verbose_name='绑定课程')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='数量(张)')),
                ('open_date', models.DateField(verbose_name='优惠券领取开始时间')),
                ('close_date', models.DateField(verbose_name='优惠券领取结束时间')),
                ('valid_begin_date', models.DateField(verbose_name='有效期开始时间')),
                ('coupon_valid_days', models.PositiveIntegerField(help_text='自券被领时开始算起', verbose_name='优惠券有效期（天）')),
                ('status', models.SmallIntegerField(choices=[(0, '上线'), (1, '下线')], default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='CouponRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=64, unique=True, verbose_name='唯一优惠码')),
                ('status', models.SmallIntegerField(choices=[(0, '未使用'), (1, '已使用'), (2, '已过期')], default=0)),
                ('get_time', models.DateTimeField(blank=True, help_text='用户领取时间', null=True, verbose_name='领取时间')),
                ('used_time', models.DateTimeField(blank=True, null=True, verbose_name='使用时间')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='生成时间')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Coupon')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('course_type', models.SmallIntegerField(choices=[(0, '免费课'), (1, '实战'), (2, '大课模块')])),
                ('pc_cover_img', models.ImageField(blank=True, null=True, upload_to='media')),
                ('h5_cover_img', models.ImageField(blank=True, null=True, upload_to='media')),
                ('price', models.FloatField()),
                ('video_hours', models.IntegerField(verbose_name='时长(h)')),
                ('brief', models.TextField(max_length=512)),
                ('level', models.SmallIntegerField(choices=[(0, '初级'), (1, '进阶'), (2, '高级')])),
                ('pub_date', models.DateField()),
                ('study_num', models.PositiveIntegerField(default=67)),
                ('attach_path', models.CharField(blank=True, max_length=128, null=True)),
                ('recommend_period', models.PositiveIntegerField()),
                ('order', models.PositiveSmallIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(choices=[(0, '下线'), (1, '上线')])),
                ('big_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.BigCourse')),
            ],
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('order', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('brief', models.TextField()),
                ('pub_date', models.DateField()),
                ('order', models.PositiveSmallIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('video_time', models.CharField(max_length=32)),
                ('section_type', models.SmallIntegerField(choices=[(0, '视频'), (1, '文档')], default=0)),
                ('vid', models.CharField(max_length=128)),
                ('free_trail', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('enabled', models.BooleanField(default=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.CourseChapter')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('order', models.PositiveSmallIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.CourseCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='作业题目')),
                ('order', models.PositiveSmallIntegerField(help_text='同一课程的每个作业之前的order值间隔1-2个数', verbose_name='作业顺序')),
                ('homework_type', models.SmallIntegerField(choices=[(0, '作业'), (1, '模块通关考核')], default=0)),
                ('requirement', models.TextField(verbose_name='作业需求')),
                ('score_point', models.TextField(max_length=1024, verbose_name='踩分点')),
                ('recommend_period', models.PositiveSmallIntegerField(default=7, verbose_name='推荐完成周期(天)')),
                ('scholarship_value', models.PositiveSmallIntegerField(verbose_name='为该作业分配的奖学金(贝里)')),
                ('note', models.TextField(blank=True, null=True)),
                ('enabled', models.BooleanField(default=True, help_text='本作业如果后期不需要了，不想让学员看到，可以设置为False')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.CourseChapter')),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.SmallIntegerField(blank=True, choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'), (40, 'C-'), (-1, 'D'), (0, 'N/A'), (-100, 'COPY')], null=True, verbose_name='分数')),
                ('mentor_comment', models.TextField(blank=True, null=True, verbose_name='导师批注')),
                ('status', models.SmallIntegerField(choices=[(0, '待批改'), (1, '已通过'), (2, '不合格')], default=0, verbose_name='作业状态')),
                ('submit_num', models.SmallIntegerField(default=0, verbose_name='提交次数')),
                ('note', models.TextField(blank=True, help_text='选填，后期还可加补', null=True, verbose_name='备注')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='作业提交日期')),
                ('check_date', models.DateTimeField(blank=True, null=True, verbose_name='作业批改日期')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后一次修改日期')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Homework')),
                ('mentor', models.ForeignKey(limit_choices_to={'role': 1}, on_delete=django.db.models.deletion.CASCADE, related_name='my_stu_homework_record', to=settings.AUTH_USER_MODEL, verbose_name='导师')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=64, unique=True)),
                ('pay_type', models.SmallIntegerField(choices=[(0, '支付宝'), (1, '微信'), (2, '贝理')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')),
                ('paid_time', models.DateTimeField(blank=True, null=True, verbose_name='实际付款时间')),
                ('actual_amount', models.FloatField(verbose_name='实际支付')),
                ('status', models.SmallIntegerField(choices=[(0, '待支付'), (1, '支付成功'), (2, '超时取消（用户自主）'), (3, '超时取消（系统自动）'), (4, '已退款')])),
                ('third_party_order_num', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='SubOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=64, unique=True)),
                ('object_id', models.IntegerField()),
                ('acutal_price', models.FloatField(verbose_name='实际价格')),
                ('original_price', models.FloatField(verbose_name='原价')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')),
                ('paid_time', models.DateTimeField(blank=True, null=True, verbose_name='实际付款时间')),
                ('status', models.SmallIntegerField(choices=[(0, '待支付'), (1, '支付成功'), (2, '超时取消（用户自主）'), (3, '超时取消（系统自动）'), (4, '已退款')])),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Order')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.CourseSubCategory', verbose_name='课程分类'),
        ),
        migrations.AddField(
            model_name='couponrecord',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Order', verbose_name='关联订单'),
        ),
        migrations.AlterUniqueTogether(
            name='homework',
            unique_together={('chapter', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='coursesubcategory',
            unique_together={('category', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='coursechapter',
            unique_together={('course', 'name')},
        ),
    ]
