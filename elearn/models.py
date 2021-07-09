from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.name)


class Shots(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to=f'Videos/Shots/')

    def __str__(self):
        return "%s" % (self.title)

class Diff_Dig(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/Dif_Dig/')

    def __str__(self):
        return "%s" % (self.title)

class recent_updates(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/recent_updates/')

    def __str__(self):
        return "%s" % (self.title)

class Values(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/Values/')

    def __str__(self):
        return "%s" % (self.title)

class ICardsPDF(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/Icards/')

    def __str__(self):
        return "%s" % (self.title)

class ICardsVideo(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'Videos/Icards/')

    def __str__(self):
        return "%s" % (self.title)

class ImageBank(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/ImageBank/')

    def __str__(self):
        return "%s" % (self.title)

class WallPosters(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to=f'PDF/Wall_Posters/')

    def __str__(self):
        return "%s" % (self.title)