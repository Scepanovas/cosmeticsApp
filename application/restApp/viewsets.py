from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, generics, status, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import (SearchFilter, OrderingFilter,)
from restApp.serializers import *
from modelsViews.models import *
from django.db.models import Max, Avg, Count
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class SkinTypeViewSet(viewsets.ModelViewSet):
    queryset = SkinTypeModel.objects.all()
    serializer_class = SkinTypeSerializer

class BrandListViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all().filter(isBrand=True).order_by('-created_date')
    serializer_class = BrandSerializer
    filter_backends  = (filters.SearchFilter,)
    search_fields    = ('email', 'brandName', 'webPage')
    pagination_class = StandardResultsSetPagination

class BrandDetailsViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailsSerializer

class BrandViewSet(viewsets.ModelViewSet, UpdateModelMixin):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends  = (filters.SearchFilter,)
    search_fields    = ('=username', '=email', '=brandName')
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ProductDetailsViewSet(viewsets.ModelViewSet):
    queryset = ProductsModel.objects.all()
    serializer_class = ProductDetailsSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductsModel.objects.all()
    serializer_class = ProductSerializer
    filter_backends  = (filters.SearchFilter,)
    search_fields    = ('=name',)
    pagination_class = StandardResultsSetPagination
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ProductViewSearchSet(viewsets.ModelViewSet):
    queryset = ProductsModel.objects.all().order_by('-created_date')
    serializer_class = ProductSerializer
    filter_backends  = (filters.SearchFilter,)
    search_fields    = ('name',)
    pagination_class = StandardResultsSetPagination
    lookup_field = 'pk'

class IngredientsViewSet(viewsets.ModelViewSet):
    queryset         = ingredientsModel.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends  = (filters.SearchFilter,)
    search_fields    = ('referenceNumber', 'name', 'casNumber', 'ecNumber')
    pagination_class = StandardResultsSetPagination

#Ratings and TOP 15 ------------------------------------------------------------
class postRankViewSet(viewsets.ModelViewSet):
    serializer_class = PostRankSerializer
    queryset = RankingModel.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('ratedOnBrand', 'ratedOnProduct', 'ratedById')

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class topBrandsViewSet(viewsets.ModelViewSet):
    serializer_class = RankingSerializer
    queryset = (RankingModel.objects
        .values('ratedOnProduct__name',
                'ratedOnProduct__thumbnail',
                'ratedOnProduct_id',
                'ratedOnBrand__username',
                'ratedOnBrand__brandName',
                'ratedOnBrand__thumbnail',
                'ratedOnBrand_id',
                'type')
        .filter(type='B')
        .annotate(voted    = Count('ratedOnBrand_id'),
                  result   = Avg('rating'),
                  newestTs = Max('created_date'))
        .order_by('-result','-newestTs')
        [:15]
        )
class topProductsViewSet(viewsets.ModelViewSet):
    serializer_class = RankingSerializer
    queryset = (RankingModel.objects
        .values('ratedOnProduct__name',
                'ratedOnProduct__thumbnail',
                'ratedOnProduct_id',
                'ratedOnBrand__username',
                'ratedOnBrand__brandName',
                'ratedOnBrand__thumbnail',
                'ratedOnBrand_id',
                'type')
        .filter(type='P')
        .annotate(voted    = Count('ratedOnProduct'),
                  result   = Avg('rating'),
                  newestTs = Max('created_date'))
        .order_by('-result','-newestTs')
        [:15]
        )
class topUsersViewSet(viewsets.ModelViewSet):
    serializer_class = RankingSerializer
    queryset = (RankingModel.objects
        .values('ratedOnProduct__name',
                'ratedOnProduct__thumbnail',
                'ratedOnProduct_id',
                'ratedOnBrand__username',
                'ratedOnBrand__brandName',
                'ratedOnBrand__thumbnail',
                'ratedOnBrand_id',
                'type')
        .filter(type='U')
        .annotate(voted    = Count('ratedOnBrand_id'),
                  result   = Avg('rating'),
                  newestTs = Max('created_date'))
        .order_by('-result','-newestTs')
        [:15]
        )
#end Ratings and TOP 15 --------------------------------------------------------

#Comments section --------------------------------------------------------------
class CommentBrandViewSet(viewsets.ModelViewSet):
    queryset = CommentsModel.objects.all().order_by('-created_date')
    serializer_class = CommentSerializer
    filter_backends  = (filters.SearchFilter,)
    search_fields    = ('=commentedOnBrand__id',)
    pagination_class = StandardResultsSetPagination

class CommentProductViewSet(viewsets.ModelViewSet):
    queryset = CommentsModel.objects.all().order_by('-created_date')
    serializer_class = CommentSerializer
    filter_backends  = (filters.SearchFilter,)
    search_fields    = ('=commentedOnProduct__id',)
    pagination_class = StandardResultsSetPagination

class CreateCommentViewSet(viewsets.ModelViewSet):
    queryset = CommentsModel.objects.all()
    serializer_class = CreateCommentSerializer
