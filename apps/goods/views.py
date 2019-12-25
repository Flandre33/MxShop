from django.shortcuts import render
from rest_framework.views import APIView
from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from .models import Goods, GoodsCategory, Banner
from rest_framework.response import Response
from rest_framework import generics, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from .filters import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle


# Create your views here.
# class GoodsListView(APIView):
#     """
#     商品列表
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()
#         # 自动补全图片的路径
#         goods_serialzer = GoodsSerializer(goods, many=True)
#         return Response(goods_serialzer.data)

class GoodsPagination(PageNumberPagination):
    """
    商品列表自定义分页
    """
    # 默认每页显示的个数
    page_size = 10
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100

# class GoodsListView(generics.ListAPIView):
#     """
#     商品列表页
#     """
#     pagination_class = GoodsPagination # 分页
#     queryset = Goods.objects.all().order_by('id')
#     serializer_class = GoodsSerializer

class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    商品列表页
    """
    # 分页
    pagination_class = GoodsPagination
    # 这里必须要定义一个默认的排序,否则会报错
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    filter_backends = [DjangoFilterBackend]

    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter

    # 搜索,=name表示精确搜索，也可以使用各种正则表达式
    search_fields = ('=name', 'goods_brief')

    # 排序
    ordering_fields = ('sold_num', 'shop_price')

    throttle_classes = (UserRateThrottle, AnonRateThrottle)

    # 商品点击数 + 1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''
    # 分页
    pagination_class = GoodsPagination
    queryset = GoodsCategory.objects.filter(category_type=1).order_by('id')
    serializer_class = CategorySerializer

class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer

class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    # 获取is_tab=True(导航栏)里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer


