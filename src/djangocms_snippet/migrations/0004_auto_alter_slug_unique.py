from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0003_auto_data_fill_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='slug',
            field=models.SlugField(default='', unique=True, max_length=75, verbose_name='slug'),
            preserve_default=True,
        ),
    ]
