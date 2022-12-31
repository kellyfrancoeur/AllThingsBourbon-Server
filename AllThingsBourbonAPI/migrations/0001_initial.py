# Generated by Django 4.1.3 on 2022-12-31 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bourbon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('proof', models.IntegerField(blank=True, null=True)),
                ('aroma', models.CharField(max_length=500)),
                ('taste', models.CharField(max_length=500)),
                ('finish', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('made_in', models.CharField(max_length=75)),
                ('link_to_buy', models.CharField(max_length=150)),
                ('bourbon_img', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='BourbonDescriptor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BourbonStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BourbonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BourbonUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cocktail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ingredients', models.CharField(max_length=500)),
                ('how_to_make', models.CharField(max_length=1000)),
                ('cocktail_img', models.CharField(max_length=500)),
                ('staff_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_cocktail', to='AllThingsBourbonAPI.bourbonstaff')),
            ],
        ),
        migrations.CreateModel(
            name='CocktailType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Descriptor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Distillery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('location', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=1000)),
                ('link_to_site', models.CharField(max_length=500)),
                ('distillery_img', models.CharField(max_length=500)),
                ('staff_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_distillery', to='AllThingsBourbonAPI.bourbonstaff')),
            ],
        ),
        migrations.CreateModel(
            name='DistilleryVisited',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=500)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('distillery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enthusiasts', to='AllThingsBourbonAPI.distillery')),
                ('distillery_enthusiast', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='distillery_visited', to='AllThingsBourbonAPI.bourbonuser')),
            ],
        ),
        migrations.CreateModel(
            name='CocktailTried',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=500)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('cocktail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enthusiasts', to='AllThingsBourbonAPI.cocktail')),
                ('cocktail_enthusiast', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cocktails_tried', to='AllThingsBourbonAPI.bourbonuser')),
            ],
        ),
        migrations.AddField(
            model_name='cocktail',
            name='type_of_cocktail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cocktails', to='AllThingsBourbonAPI.cocktailtype'),
        ),
        migrations.CreateModel(
            name='BourbonTried',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=500)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('bourbon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enthusiasts', to='AllThingsBourbonAPI.bourbon')),
                ('bourbon_enthusiast', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bourbons_tried', to='AllThingsBourbonAPI.bourbonuser')),
                ('descriptors', models.ManyToManyField(through='AllThingsBourbonAPI.BourbonDescriptor', to='AllThingsBourbonAPI.descriptor')),
            ],
        ),
        migrations.AddField(
            model_name='bourbondescriptor',
            name='bourbon_tried',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AllThingsBourbonAPI.bourbontried'),
        ),
        migrations.AddField(
            model_name='bourbondescriptor',
            name='descriptor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AllThingsBourbonAPI.descriptor'),
        ),
        migrations.AddField(
            model_name='bourbon',
            name='staff_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_bourbon', to='AllThingsBourbonAPI.bourbonstaff'),
        ),
        migrations.AddField(
            model_name='bourbon',
            name='type_of_bourbon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bourbons', to='AllThingsBourbonAPI.bourbontype'),
        ),
    ]
