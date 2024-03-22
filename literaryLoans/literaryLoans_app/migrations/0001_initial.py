# Generated by Django 4.2.11 on 2024-03-22 14:22

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('phone_no', models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone Number')),
                ('isOnboarded', models.BooleanField(default=False, verbose_name='isOnboarded')),
                ('rating_asLender', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('rating_asBorrower', models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True)),
                ('total_rating_asLender', models.IntegerField(blank=True, null=True)),
                ('total_rating_asBorrower', models.IntegerField(blank=True, null=True)),
                ('addressLine1', models.CharField(blank=True, max_length=1024, null=True)),
                ('addressLine2', models.CharField(blank=True, max_length=1024, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='State')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='Country')),
                ('picture', models.CharField(blank=True, max_length=255, null=True, verbose_name='Image')),
                ('password', models.CharField(blank=True, max_length=255, null=True, verbose_name='Password')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='Description')),
                ('status', models.CharField(choices=[('0', 'available'), ('1', 'out of stock')], default='0', max_length=1)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.IntegerField(default=0)),
                ('author', models.CharField(max_length=255)),
                ('available', models.BooleanField(default=True)),
                ('book_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('total_book_rating', models.IntegerField(default=0)),
                ('condition_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('total_condition_rating', models.IntegerField(default=0)),
                ('image', models.CharField(default='', max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='', max_length=1023)),
            ],
        ),
        migrations.CreateModel(
            name='Rented',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('rent_date', models.DateField(default=datetime.date.today)),
                ('return_date', models.DateField(default=datetime.date.today)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rented_books', to='literaryLoans_app.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrower_rented_books', to=settings.AUTH_USER_MODEL)),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lender_rented_books', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'Accepted')], default='0', max_length=1)),
                ('quantity', models.IntegerField(default=0)),
                ('request_date', models.DateField(default=datetime.date.today)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_requests', to='literaryLoans_app.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_requests_as_borrower', to=settings.AUTH_USER_MODEL)),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_requests_as_lender', to=settings.AUTH_USER_MODEL)),
                ('rented_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rented', to='literaryLoans_app.rented')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'Accepted'), ('2', 'Rejected')], default='0', max_length=1)),
                ('quantity', models.IntegerField(default=0)),
                ('request_date', models.DateField(default=datetime.date.today)),
                ('return_date', models.DateField(default=datetime.date.today)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_requests', to='literaryLoans_app.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrower_borrow_requests', to=settings.AUTH_USER_MODEL)),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lender_borrow_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='literaryLoans_app.book')),
                ('genre_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='literaryLoans_app.genre')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_genre', to='literaryLoans_app.genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='lender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_lender', to=settings.AUTH_USER_MODEL),
        ),
    ]
