# Generated by Django 4.2.4 on 2023-08-31 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_profile_reg_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_or_video',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='reg_no',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_type',
            field=models.CharField(choices=[('Alumini', 'Alumini'), ('Student', 'Student'), ('Club', 'Club'), ('Faculty', 'Faculty'), ('Unverified', 'Unverified')], default='Unverified', max_length=100),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_school',
            field=models.CharField(choices=[('SCOPE', 'School of Computer Science and Engineering-SCOPE'), ('SAS', 'School of Advanced Sciences-SAS'), ('SSL', 'School of Social Sciences and Languages-SSL'), ('SENSE', 'School of Electronics Engineering-SENSE'), ('SELECT', 'School of Electrical Engineering-SELECT'), ('SMEC', 'School of Mechanical Engineering-SMEC'), ('SCE', 'School of Civil Engineering-SCE'), ('VITBS', 'VIT Business School-VITBS'), ('VITSOL', 'VIT School of Law-VITSOL'), ('VFIT', 'VIT Fashion Institute of Technology-VFIT'), ('Other Organization', 'Other Organization'), ('Unauthorized', 'Unauthorized')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='program',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='following',
            name='request_status',
            field=models.CharField(choices=[('Followed', 'Followed'), ('Unfollow', 'Unfollow'), ('Blocked', 'Blocked')], default='Followed', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='education_level',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.URLField(null=True),
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='services.post')),
            ],
        ),
    ]
