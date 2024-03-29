# Generated by Django 2.2.2 on 2019-12-11 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20191210_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='决定着用户是否可登录管理后台', verbose_name='staff status'),
        ),
        migrations.AlterField(
            model_name='bigcourse',
            name='study_num',
            field=models.PositiveIntegerField(default=48),
        ),
        migrations.AlterField(
            model_name='course',
            name='study_num',
            field=models.PositiveIntegerField(default=35),
        ),
        migrations.CreateModel(
            name='EnrolledCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_date', models.DateTimeField(auto_now_add=True)),
                ('valid_begin_date', models.DateField(verbose_name='有效期开始自')),
                ('valid_end_date', models.DateField(verbose_name='有效期结束至')),
                ('status', models.SmallIntegerField(choices=[(0, '已开通'), (1, '已过期')], default=0)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(limit_choices_to=models.Q(_negated=True, course_type=2), on_delete=django.db.models.deletion.CASCADE, to='web.Course')),
            ],
        ),
        migrations.CreateModel(
            name='EnrolledBigCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentor_service_period', models.PositiveSmallIntegerField(verbose_name='服务周期(days)')),
                ('enrolled_date', models.DateTimeField(auto_now_add=True)),
                ('valid_begin_date', models.DateField(blank=True, null=True, verbose_name='有效期开始自')),
                ('valid_end_date', models.DateField(blank=True, null=True, verbose_name='有效期结束至')),
                ('study_status', models.SmallIntegerField(choices=[(0, '在学中'), (1, '休学中'), (2, '已毕业'), (3, '超时结业'), (4, '报名成功(未开始学习)'), (5, '已放弃学习'), (6, '休学申请中')], default=4)),
                ('mentor_fee_balance', models.PositiveIntegerField(help_text='这个学员的导师费用，每有惩罚，需在此字段同时扣除', verbose_name='导师费用余额')),
                ('initial_scholarship', models.IntegerField(verbose_name='初始奖学金')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('big_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.BigCourse')),
                ('mentor', models.ForeignKey(blank=True, limit_choices_to={'role': 1}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_students', to=settings.AUTH_USER_MODEL, verbose_name='导师')),
            ],
            options={
                'unique_together': {('account', 'big_course')},
            },
        ),
        migrations.AddField(
            model_name='homeworkrecord',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='web.EnrolledBigCourse'),
            preserve_default=False,
        ),
    ]
