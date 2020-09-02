from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_snippet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='slug',
            field=models.SlugField(default='', max_length=75, verbose_name='slug'),
            preserve_default=True,
        ),
    ]
