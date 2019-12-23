from rest_framework import serializers
from .models import Goods, GoodsCategory


# 使用Serializer实现商品列表页
# class GoodsSerializer(serializers.Serializer):
#    name = serializers.CharField(required=True, max_length=100)
#    click_num = serializers.IntegerField(default=0)
#    good_front_image = serializers.ImageField()

# 使用ModelSerializer实现商品列表页
class GoodscategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    category = GoodscategorySerializer()
    class Meta:
        model = Goods
        fields = '__all__'
