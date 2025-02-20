# Generated by Django 5.1.4 on 2025-01-20 06:23

import autoslug.fields
import core.utils
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid
import versatileimagefield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_category_slug, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediaRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('file', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_user_slug, unique=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=10)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('thana', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('postal_code', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('REMOVED', 'Removed')], default='ACTIVE', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_cart_slug, unique=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MediaRoomConnector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('mediaroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.mediaroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ManyToManyField(through='core.MediaRoomConnector', to='core.mediaroom'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_order_slug, unique=True)),
                ('added_on', models.DateField(default=django.utils.timezone.now)),
                ('delivery_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='NEW', max_length=20)),
                ('review_status', models.CharField(choices=[('REVIEWED', 'Reviewed'), ('NOT_REVIEWED', 'Notreviewed')], default='NOT_REVIEWED', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_organization_slug, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('trade_license', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('thana', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('postal_code', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('REMOVED', 'Removed')], default='ACTIVE', max_length=10)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('logo', models.ManyToManyField(through='core.MediaRoomConnector', to='core.mediaroom')),
            ],
        ),
        migrations.AddField(
            model_name='mediaroomconnector',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.organization'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_product_slug, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('brand', models.CharField(max_length=255)),
                ('manufacturing_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('price', models.FloatField()),
                ('stock', models.IntegerField(default=20)),
                ('availability', models.CharField(choices=[('IN_STOCK', 'Instock'), ('OUT_OF_STOCK', 'Outofstock')], default='IN_STOCK', max_length=20)),
                ('avg_rating', models.FloatField(blank=True, default=0)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('REMOVED', 'Removed')], default='PUBLISHED', max_length=20)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('image', models.ManyToManyField(through='core.MediaRoomConnector', to='core.mediaroom')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_order_item_slug, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('review_status', models.CharField(choices=[('REVIEWED', 'Reviewed'), ('NOT_REVIEWED', 'Notreviewed')], default='NOT_REVIEWED', max_length=20)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='core.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='core.product')),
            ],
        ),
        migrations.AddField(
            model_name='mediaroomconnector',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_cart_item_slug, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.cart')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_product_category_slug, unique=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(through='core.ProductCategory', to='core.category'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField(blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='uid', unique=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ManyToManyField(through='core.MediaRoomConnector', to='core.mediaroom')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.product')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='core.review')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='review',
            field=models.ManyToManyField(related_name='review', through='core.ProductReview', to='core.review'),
        ),
        migrations.AddField(
            model_name='mediaroomconnector',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.review'),
        ),
        migrations.CreateModel(
            name='UserOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=core.utils.generate_user_organization_slug, unique=True)),
                ('role', models.CharField(blank=True, choices=[('OWNER', 'Owner'), ('ADMIN', 'Admin'), ('MANAGER', 'Manager'), ('STAFF', 'Staff')])),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('REMOVED', 'Removed')], default='ACTIVE')),
                ('salary', models.FloatField()),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
