from django.db import models


class ShotsCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ShotsSubCategory(models.Model):
    category = models.ForeignKey(ShotsCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class Shots(models.Model):
    sub_category = models.ForeignKey(ShotsSubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to=f'Videos/Shots/')

    def __str__(self):
        return "%s" % (self.title)


class Diff_Dig_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class Diff_Dig_SubCategory(models.Model):
    category = models.ForeignKey(Diff_Dig_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class Diff_Dig(models.Model):
    sub_category = models.ForeignKey(Diff_Dig_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/Dif_Dig/')

    def __str__(self):
        return "%s" % (self.title)


class Recent_Updates_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class Recent_Updates_SubCategory(models.Model):
    category = models.ForeignKey(Recent_Updates_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class recent_updates(models.Model):
    sub_category = models.ForeignKey(Recent_Updates_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/recent_updates/')

    def __str__(self):
        return "%s" % (self.title)


class Values_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class Values_SubCategory(models.Model):
    category = models.ForeignKey(Values_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class Values(models.Model):
    sub_category = models.ForeignKey(Values_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/Values/')

    def __str__(self):
        return "%s" % (self.title)


class ICardsPDF_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ICardsPDF_SubCategory(models.Model):
    category = models.ForeignKey(ICardsPDF_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ICardsPDF(models.Model):
    sub_category = models.ForeignKey(ICardsPDF_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/Icards/')

    def __str__(self):
        return "%s" % (self.title)


class ICardsAudio_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ICardsAudio_SubCategory(models.Model):
    category = models.ForeignKey(ICardsAudio_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ICardsAudio(models.Model):
    sub_category = models.ForeignKey(ICardsAudio_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    audio = models.FileField(upload_to=f'Audios/Icards/')

    def __str__(self):
        return "%s" % (self.title)


class ICardsVideo_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ICardsVideo_SubCategory(models.Model):
    category = models.ForeignKey(ICardsVideo_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ICardsVideo(models.Model):
    sub_category = models.ForeignKey(ICardsVideo_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to=f'Videos/Icards/')

    def __str__(self):
        return "%s" % (self.title)


class ImageBank_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ImageBank_SubCategory(models.Model):
    category = models.ForeignKey(ImageBank_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class ImageBank(models.Model):
    sub_category = models.ForeignKey(ImageBank_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/ImageBank/')

    def __str__(self):
        return "%s" % (self.title)


class WallPoster_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class WallPoster_SubCategory(models.Model):
    category = models.ForeignKey(WallPoster_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class WallPosters(models.Model):
    sub_category = models.ForeignKey(WallPoster_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/Wall_Posters/')

    def __str__(self):
        return "%s" % (self.title)


class DailyBoostBanner(models.Model):
    title = models.CharField(max_length=200)
    banner = models.ImageField(upload_to=f'banner/images')

    def __str__(self):
        return "%s" % (self.title)

class QuestionOfTheDay(models.Model):
    Question = models.CharField(max_length=200)
    Answer1 = models.CharField(max_length=200)
    Answer2 = models.CharField(max_length=200)
    Answer3 = models.CharField(max_length=200)
    Answer4 = models.CharField(max_length=200)
    CorrectAnswer = models.CharField(max_length=200)
    Explanation = models.CharField(max_length=200)
    Image = models.ImageField(upload_to=f'Question/images')

    def __str__(self):
        return "%s" % (self.Question)

class DailyBoosterQuiz(models.Model):
    banner = models.ForeignKey(DailyBoostBanner, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=200)
    answer1 = models.CharField(max_length=200)
    answer2 = models.CharField(max_length=200)
    answer3 = models.CharField(max_length=200)
    answer4 = models.CharField(max_length=200)
    correctanswer = models.CharField(max_length=200)
    explanation = models.CharField(max_length=200)
    timer = models.TimeField()
    image = models.ImageField(upload_to=f'Daily/images')

    def __str__(self):
        return "%s" % (self.question)

class QuestionBank_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)

class QuestionBank_SubCategory(models.Model):
    category = models.ForeignKey(QuestionBank_Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)

class QuestionBank(models.Model):
    category = models.ForeignKey(QuestionBank_SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    examtype = models.CharField(max_length=200)
    numberofmcqs = models.CharField(max_length=200)
    question = models.CharField(max_length=200)
    answer1 = models.CharField(max_length=200)
    answer2 = models.CharField(max_length=200)
    answer3 = models.CharField(max_length=200)
    answer4 = models.CharField(max_length=200)
    correctanswer = models.CharField(max_length=200)
    explanation = models.CharField(max_length=200)
    image = models.ImageField(upload_to=f'Bank/images')

    def __str__(self):
        return "%s" % (self.title)