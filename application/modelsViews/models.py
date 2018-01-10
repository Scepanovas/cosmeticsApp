import os
import uuid

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from PIL import Image
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


def scramble_uploaded_filename(instance, filename):

    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)


def create_thumbnail(input_image, thumbnail_size=(256, 256)):

    if not input_image or input_image == "":
        return

    image = Image.open(input_image)
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
    filename = scramble_uploaded_filename(None, os.path.basename(input_image.name))
    arrdata = filename.split(".")
    extension = arrdata.pop()
    basename = "".join(arrdata)
    new_filename = basename + "_thumb." + extension
    image.save(os.path.join(settings.MEDIA_ROOT, new_filename))

    return new_filename

#INGREDIENTS

class warningsModel(models.Model):
    referenceNumber  = models.IntegerField(unique=True)
    description      = models.CharField(max_length=300)

    def __str__(self):
        return str(self.referenceNumber)

class ingredientFunctionsModel(models.Model):
    name            = models.CharField(max_length=50,unique=True)
    description     = models.TextField()

    def __str__(self):
        return self.description

class ingredientsModel(models.Model):
    referenceNumber  = models.IntegerField(db_index=True, unique=True)
    riskLevel        = models.IntegerField(validators=[MaxValueValidator(3),
                                                      MinValueValidator(1)])
    name             = models.TextField(db_index=True, unique=True)
    casNumber        = models.CharField(null=True, blank=True,
                                       db_index=True, max_length=20)
    ecNumber         = models.CharField(null=True, blank=True,
                                       db_index=True, max_length=20)
    description      = models.TextField(null=True, blank=True)
    restriction      = models.CharField(null=True, blank=True, max_length=50)
    cannotBeUsedUnderAge = models.IntegerField(default=0)
    functions        = models.ManyToManyField(ingredientFunctionsModel,
                                             related_name ='function',
                                             blank=True)
    warnings         = models.ManyToManyField(warningsModel,
                                             related_name ='warning',
                                             blank=True)
    updateDate      = models.CharField(null=True, blank=True, max_length=10)

    def __str__(self):
        return str(self.referenceNumber) + ' ' + self.name + ' Score:' + str(self.riskLevel)

#Skin test and recommendations
class SuggestedReasonsConfig(models.Model):
    function = models.ForeignKey(ingredientFunctionsModel,
                                 on_delete=models.CASCADE,
                                 related_name ='suggestedFunction')
    text     = models.CharField(max_length=400)

    def __str__(self):
        return str(self.pk) + ' - ' + self.text

class SkinTypeModel(models.Model):
    name         = models.CharField(max_length=128)
    suggested    = models.ManyToManyField(SuggestedReasonsConfig,
                                          related_name ='suggested',
                                          null=True, blank=True)
    notSuggested = models.ManyToManyField(SuggestedReasonsConfig,
                                          related_name ='notSuggested',
                                          null=True, blank=True)
    def __str__(self):
        return str(self.pk) + ' ' + str(self.name)

class Brand(AbstractUser):
    username     = models.CharField(max_length=128, unique=True)
    email        = models.CharField(max_length=128, unique=True, db_index=True)
    country      = models.CharField(max_length=64, blank=True)
    tagLine      = models.CharField(max_length=4000, blank=True)
    isBrand      = models.NullBooleanField(null=True)
    isTested     = models.BooleanField(default=False)
    skinType     = models.ForeignKey(SkinTypeModel, related_name ='skinType',
                                     default=0)
    brandName    = models.CharField(max_length=256, blank=True)
    image        = models.ImageField("Uploaded image",
                                     upload_to=scramble_uploaded_filename,
                                     default='../uploaded_media/index.png')
    webPage      = models.CharField(max_length=128, blank=True, db_index=True)
    thumbnail    = models.ImageField("Thumbnail of uploaded image", blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS  = ['email']

    def __str__(self):
        return self.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.thumbnail = create_thumbnail(self.image)
        super(Brand, self).save(force_update=force_update)

#Products

class ProductsModel(models.Model):

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,
                              related_name="products_list")
    name = models.CharField(max_length=128, db_index=True)
    tagLine = models.CharField(max_length=4000)
    image = models.ImageField("Uploaded image",
                              upload_to=scramble_uploaded_filename, blank=True)
    ingredients = models.ManyToManyField(ingredientsModel,
                                         related_name ='ingredients')
    thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.thumbnail = create_thumbnail(self.image)
        super(ProductsModel, self).save(force_update=force_update)

class CommentsModel(models.Model):

    author             = models.ForeignKey(Brand, on_delete=models.CASCADE,
                                           related_name = 'author')
    commentedOnBrand   = models.ForeignKey(Brand, related_name = 'commentedOnBrand',
                                           on_delete=models.CASCADE, null=True)
    commentedOnProduct = models.ForeignKey(ProductsModel,
                                           related_name = 'commentedOnProduct',
                                           on_delete=models.CASCADE, null=True)
    tagLine            = models.CharField(max_length=4000)
    youtube            = models.CharField(max_length=400, blank=True)
    created_date       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    #def author_thumbnail(self):
    #    return self.author.thumbnail

class RankingModel(models.Model):
    ratedOnBrand   = models.ForeignKey(Brand, related_name = 'ratedOnBrand',
                                       on_delete=models.CASCADE, null=True)
    ratedOnProduct = models.ForeignKey(ProductsModel,
                                       related_name = 'ratedOnProduct',
                                       on_delete=models.CASCADE, null=True)
    ratedById      = models.ForeignKey(Brand, related_name = 'ratedBy',
                                       on_delete=models.CASCADE)
    type           = models.CharField(max_length=1)
    rating         = models.IntegerField(validators=[MaxValueValidator(5),
                                                     MinValueValidator(1)])
    created_date = models.DateTimeField(auto_now_add=True)

#SUBSTANCES

class banedSubstancesModel(models.Model):
    referenceNumber = models.CharField(max_length=5, db_index=True, unique=True)
    chemicalName    = models.TextField(null=True, blank=True)
    casNumber       = models.TextField(null=True, blank=True)
    ecNumber        = models.TextField(null=True, blank=True)
    regulation      = models.TextField(null=True, blank=True)
    regulatedBy     = models.TextField(null=True, blank=True)
    otherDirective  = models.TextField(null=True, blank=True)
    sccsOpinion     = models.TextField(null=True, blank=True)
    iupacName       = models.TextField(null=True, blank=True)
    ingredients     = models.TextField(null=True, blank=True)
    cmr             = models.TextField(null=True, blank=True)
    updateDate      = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.referenceNumber

class restrictedSubstancesModel(models.Model):
    referenceNumber = models.CharField(max_length=5, db_index=True, unique=True)
    chemicalName    = models.TextField(null=True, blank=True)
    glossary        = models.TextField(null=True, blank=True)
    casNumber       = models.TextField(null=True, blank=True)
    ecNumber        = models.TextField(null=True, blank=True)
    productType     = models.TextField(null=True, blank=True)
    maxConcetration = models.TextField(null=True, blank=True)
    other           = models.TextField(null=True, blank=True)
    wordingWarnings = models.TextField(null=True, blank=True)
    regulation      = models.TextField(null=True, blank=True)
    regulatedBy     = models.TextField(null=True, blank=True)
    otherDirective  = models.TextField(null=True, blank=True)
    sccsOpinion     = models.TextField(null=True, blank=True)
    iupacName       = models.TextField(null=True, blank=True)
    ingredients     = models.TextField(null=True, blank=True)
    cmr             = models.TextField(null=True, blank=True)
    updateDate      = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.referenceNumber

class colorantsModel(models.Model):
    referenceNumber = models.CharField(max_length=5, db_index=True, unique=True)
    chemicalName    = models.TextField(null=True, blank=True)
    colourIndex     = models.TextField(null=True, blank=True)
    casNumber       = models.TextField(null=True, blank=True)
    ecNumber        = models.TextField(null=True, blank=True)
    colour          = models.TextField(null=True, blank=True)
    productType     = models.TextField(null=True, blank=True)
    maxConcetration = models.TextField(null=True, blank=True)
    other           = models.TextField(null=True, blank=True)
    wordingWarnings = models.TextField(null=True, blank=True)
    regulation      = models.TextField(null=True, blank=True)
    regulatedBy     = models.TextField(null=True, blank=True)
    otherDirective  = models.TextField(null=True, blank=True)
    sccsOpinion     = models.TextField(null=True, blank=True)
    iupacName       = models.TextField(null=True, blank=True)
    ingredients     = models.TextField(null=True, blank=True)
    cmr             = models.TextField(null=True, blank=True)
    updateDate      = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.referenceNumber

class preservativesModel(models.Model):
    referenceNumber = models.CharField(max_length=5, db_index=True, unique=True)
    chemicalName    = models.TextField(null=True, blank=True)
    glossary        = models.TextField(null=True, blank=True)
    casNumber       = models.TextField(null=True, blank=True)
    ecNumber        = models.TextField(null=True, blank=True)
    productType     = models.TextField(null=True, blank=True)
    maxConcetration = models.TextField(null=True, blank=True)
    other           = models.TextField(null=True, blank=True)
    wordingWarnings = models.TextField(null=True, blank=True)
    regulation      = models.TextField(null=True, blank=True)
    regulatedBy     = models.TextField(null=True, blank=True)
    otherDirective  = models.TextField(null=True, blank=True)
    sccsOpinion     = models.TextField(null=True, blank=True)
    iupacName       = models.TextField(null=True, blank=True)
    ingredients     = models.TextField(null=True, blank=True)
    cmr             = models.TextField(null=True, blank=True)
    updateDate      = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.referenceNumber

class uvFiltersModel(models.Model):
    referenceNumber = models.CharField(max_length=5, db_index=True, unique=True)
    chemicalName    = models.TextField(null=True, blank=True)
    glossary        = models.TextField(null=True, blank=True)
    casNumber       = models.TextField(null=True, blank=True)
    ecNumber        = models.TextField(null=True, blank=True)
    productType     = models.TextField(null=True, blank=True)
    maxConcetration = models.TextField(null=True, blank=True)
    other           = models.TextField(null=True, blank=True)
    wordingWarnings = models.TextField(null=True, blank=True)
    regulation      = models.TextField(null=True, blank=True)
    regulatedBy     = models.TextField(null=True, blank=True)
    otherDirective  = models.TextField(null=True, blank=True)
    sccsOpinion     = models.TextField(null=True, blank=True)
    iupacName       = models.TextField(null=True, blank=True)
    ingredients     = models.TextField(null=True, blank=True)
    cmr             = models.TextField(null=True, blank=True)
    updateDate      = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.referenceNumber
