# Generated by Django 3.2.5 on 2021-07-18 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0021_dailyboosterbookmark_discussion_groupdiscussionadmin_groupdiscussionuser_leaderboard_test_category_t'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyboosterbookmark',
            name='DailyBoosterMain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.dailyboosterquiz'),
        ),
    ]
