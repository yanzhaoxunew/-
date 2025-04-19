from rest_framework import serializers
from .models import OrderDetail, UserList


class MealBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['id', 'date', 'name', 'breakfast', 'lunch', 'dinner']

    def validate_name(self,value):
        '''
        验证姓名
        :param value:
        :return:
        '''
        if not UserList.objects.filter(name=value,is_active=True).exists():
            raise serializers.ValidationError("该用户不在允许报餐的名单中")
        return value

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserList
        fields = ['id','name','is_active']