from django.conf.urls import url, include
from rest_framework import routers
from restApp.viewsets import *

from rest_framework.routers import DefaultRouter

# initiate router and register all endpoints
router = routers.DefaultRouter()

router.register(r'brands', BrandViewSet)
router.register(r'brands_list', BrandListViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product', ProductDetailsViewSet)
router.register(r'productSearch', ProductViewSearchSet)
router.register(r'brandDetails', BrandDetailsViewSet)

router.register(r'commentsbrand',   CommentBrandViewSet)
router.register(r'commentsproduct', CommentProductViewSet)
router.register(r'createcomment', CreateCommentViewSet)

#top15 urls
router.register(r'postrank', postRankViewSet)
router.register(r'topbrands', topBrandsViewSet)
router.register(r'topproducts', topProductsViewSet)
router.register(r'topusers', topUsersViewSet)

# Wire up our API with our urls
urlpatterns = [
    url(r'^', include(router.urls)),
]
