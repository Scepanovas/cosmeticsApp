from rest_framework import serializers
from modelsViews.models import *
from django.core.files.base import ContentFile
import base64
import six
import uuid
import imghdr

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
            	header, data = data.split(';base64,')
            try:
            	decoded_file = base64.b64decode(data)
            except TypeError:
            	self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)
    def get_file_extension(self, file_name, decoded_file):
    	extension = imghdr.what(file_name, decoded_file)
    	extension = "jpg" if extension == "jpeg" else extension
    	return extension

class ProductSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True,
        allow_empty_file=True,
    )
    class Meta:
        model = ProductsModel
        fields = ('pk',
                  'brand',
                  'name',
                  'tagLine',
                  'image',
                  'ingredients',
                  'created_date',
                  'thumbnail')
        read_only_fields = ('thumbnail',)
    def create(self, validated_data):
            product = ProductsModel(
                brand=validated_data['brand'],
                name=validated_data['name'],
                tagLine=validated_data['tagLine'],
                image=validated_data['image'],
            )
            product.save()
            return product

class WarningSerializer(serializers.ModelSerializer):

    class Meta:
        model = warningsModel
        fields = ('pk',
                  'referenceNumber',
                  'description')

class FunctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ingredientFunctionsModel
        fields = ('pk',
                  'name',
                  'description')

class SuggestedReasonsConfigSerializer(serializers.ModelSerializer):
    suggestedFunction = FunctionSerializer(many=True, read_only=True)
    class Meta:
        model = SuggestedReasonsConfig
        fields = ('pk',
                  'suggestedFunction',
                  'text')

class SkinTypeSerializer(serializers.ModelSerializer):
    suggested    = SuggestedReasonsConfigSerializer(many=True, read_only=True)
    notSuggested = SuggestedReasonsConfigSerializer(many=True, read_only=True)
    class Meta:
        model = SkinTypeModel
        fields = ('pk',
                  'name',
                  'suggested',
                  'notSuggested')

class BrandDetailsSerializer(serializers.ModelSerializer):
    skinType = SkinTypeSerializer(read_only=True)
    products_list = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = ('pk',
                  'username',
                  'email',
                  'country',
                  'tagLine',
                  'brandName',
                  'isBrand',
                  'isTested',
                  'skinType',
                  'image',
                  'webPage',
                  'thumbnail',
                  'created_date',
                  'password',
                  'products_list')

class BrandSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True,
        allow_empty_file=True,
    )
    #skinType = SkinTypeSerializer()
    products_list = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = ('pk',
                  'username',
                  'email',
                  'country',
                  'tagLine',
                  'brandName',
                  'isBrand',
                  'isTested',
                  'skinType',
                  'image',
                  'webPage',
                  'thumbnail',
                  'created_date',
                  'password',
                  'products_list')
        read_only_fields = ('thumbnail',)
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
            #user = Brand.objects.create_user(**validated_data)
            user = Brand(
                email=validated_data['email'],
                username=validated_data['username'],
                isBrand=validated_data['isBrand'],
                brandName=validated_data['brandName'],
                tagLine=validated_data['tagLine'],
                image=validated_data['image'],
                webPage=validated_data['webPage'],
                country=validated_data['country']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

class IngredientsSerializer(serializers.ModelSerializer):

    functions = serializers.StringRelatedField(many=True)

    class Meta:
        model = ingredientsModel
        fields = ('pk',
                  'referenceNumber',
                  'riskLevel',
                  'name',
                  'casNumber',
                  'ecNumber',
                  'cannotBeUsedUnderAge',
                  'functions',
                  'warnings')

class IngredientsDetailSerializer(serializers.ModelSerializer):
    functions = FunctionSerializer(many=True, read_only=True)
    warnings  = WarningSerializer (many=True, read_only=True)

    class Meta:
        model = ingredientsModel
        fields = ('pk',
                  'referenceNumber',
                  'riskLevel',
                  'name',
                  'casNumber',
                  'ecNumber',
                  'cannotBeUsedUnderAge',
                  'functions',
                  'warnings')

class CommentSerializer(serializers.ModelSerializer):
    author             = BrandSerializer   (read_only=True)
    commentedOnProduct = ProductSerializer (read_only=True)
    commentedOnBrand   = BrandSerializer   (read_only=True)

    class Meta:
        model = CommentsModel
        fields = ('pk',
                  'author',
                  'tagLine',
                  'youtube',
                  'created_date',
                  'commentedOnBrand',
                  'commentedOnProduct')

class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentsModel
        fields = ('pk',
                  'author',
                  'tagLine',
                  'youtube',
                  'created_date',
                  'commentedOnBrand',
                  'commentedOnProduct')

class ProductDetailsSerializer(serializers.ModelSerializer):
    ingredients = IngredientsDetailSerializer(many=True, read_only=True)
    brand       = BrandSerializer            (read_only=True)

    class Meta:
        model = ProductsModel
        fields = ('pk',
                  'brand',
                  'name',
                  'tagLine',
                  'image',
                  'ingredients',
                  'created_date',
                  'thumbnail')
        read_only_fields = ('thumbnail',)

class RankingSerializer(serializers.ModelSerializer):

    result         = serializers.DecimalField(max_digits=None, decimal_places=1)
    voted          = serializers.IntegerField()
    newestTs       = serializers.DateTimeField()
    ratedOnBrand   = BrandSerializer  (read_only=True)
    ratedOnProduct = ProductSerializer(read_only=True)
    ratedOnBrand__username       = serializers.CharField()
    ratedOnBrand__brandName      = serializers.CharField()
    ratedOnBrand__thumbnail      = serializers.URLField()
    ratedOnProduct__name         = serializers.CharField()
    ratedOnProduct__thumbnail    = serializers.URLField()
    ratedOnProduct_id            = serializers.IntegerField()
    ratedOnBrand_id              = serializers.IntegerField()

    class Meta:
        model = RankingModel
        fields = ('ratedOnProduct_id',
                  'ratedOnProduct__name',
                  'ratedOnProduct__thumbnail',
                  'ratedOnBrand_id',
                  'ratedOnBrand__username',
                  'ratedOnBrand__brandName',
                  'ratedOnBrand__thumbnail',
                  'ratedOnBrand',
                  'ratedOnProduct',
                  'result',
                  'newestTs',
                  'voted',
                  'type')

class PostRankSerializer(serializers.ModelSerializer):

    class Meta:
        model = RankingModel
        fields = ('pk',
                  'ratedOnBrand',
                  'ratedOnProduct',
                  'ratedById',
                  'type',
                  'rating')

"""
class UploadedImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedImage
        fields = ('pk', 'image', 'thumbnail', 'title', 'description', )
        read_only_fields = ('thumbnail',)

class CommentProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('pk', 'author_name',
                  'author', 'title', 'tagLine', 'youtube',
                  'created_date', 'commentedOnProduct')
       #image_url = serializers.SerializerMethodField('get_image_url')
       #def get_image_url(self, obj):
       #    return obj.image.url
class IngredientTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientTest
        fields = ('pk', 'refNo', 'inciName', 'innName', 'eurName', 'casNo',
                  'enlincsNo', 'chem', 'restriction', 'function', 'updated')

"""
"""#sample
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('pk', 'name', 'tagLine',
        'image', 'thumbnail', 'created_date')
        read_only_fields = ('thumbnail',)
"""
