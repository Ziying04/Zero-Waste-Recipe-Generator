from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationFoodPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('quantity', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Fruits', 'Fruits'), ('Vegetables', 'Vegetables'), ('Dairy', 'Dairy'), ('Grains & Bread', 'Grains & Bread'), ('Protein', 'Protein & Meat'), ('Prepared Meals', 'Prepared Meals'), ('Canned Goods', 'Canned Goods'), ('Other', 'Other')], max_length=50)),
                ('image', models.ImageField(upload_to='donation_food_posts/')),
                ('expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation_food_posts', to='auth.user')),
            ],
        ),
    ]
