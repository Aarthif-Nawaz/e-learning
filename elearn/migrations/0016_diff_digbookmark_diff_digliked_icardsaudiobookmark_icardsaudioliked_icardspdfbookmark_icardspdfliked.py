# Generated by Django 3.2.5 on 2021-07-17 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0015_rename_registration_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='WallPostersLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('WallPosters', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.wallposters')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='WallPostersbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('WallPosters', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.wallposters')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ValuesLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('Values', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.values')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ValuesbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('Values', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.values')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ShotsLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('shots', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.shots')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ShotsbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('shots', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.shots')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='Recent_UpdatesLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('Recent_Updates', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.recent_updates')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='Recent_UpdatesbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('Recent_Updates', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.recent_updates')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionDiscussionbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('QuestionDiscussion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.questiondiscussion')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='PrimeClassVideobookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('PrimeClassVideo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.primeclassvideo')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='PrimeClassNotesbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('PrimeClassNotes', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.primeclassnotes')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='PrimeClassAudiobookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('PrimeClassAudio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.primeclassaudio')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='LiveClassbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('liveClass', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.liveclass')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ImageBankLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('ImageBank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.imagebank')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ImageBankbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('ImageBank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.imagebank')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ICardsVideoLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('ICardsVideo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.icardsvideo')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ICardsVideobookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('ICardsVideo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.icardsvideo')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ICardsPDFLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('ICardsPDF', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.icardspdf')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ICardsPDFbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('ICardsPDF', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.icardspdf')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ICardsAudioLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('ICardsAudio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.icardsaudio')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='ICardsAudiobookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('ICardsAudio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.icardsaudio')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='Diff_DigLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_status', models.BooleanField(default=False)),
                ('Diff_Digg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.diff_dig')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='Diff_DigbookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark_status', models.BooleanField(default=False)),
                ('Diff_Digg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.diff_dig')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elearn.user')),
            ],
        ),
    ]
