from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from appdemo.models import *
from appdemo.serializers import MealBookingSerializer
from .serializers import UserListSerializer


# Create your views here.
class CreateBookingView(generics.CreateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = MealBookingSerializer

    def create(self, request, *args, **kwargs):
        # 验证
        name = request.data.get('name')
        if not UserList.objects.filter(name=name, is_active=True).exists():
            return Response({"error": "该用户不在允许报餐的名单中"}, status=status.HTTP_403_FORBIDDEN)
        # 检查是否存在相同日期和姓名的记录
        existing_booking = OrderDetail.objects.filter(
            date=request.data.get('date'),
            name=request.data.get('name')
        ).first()

        if existing_booking:
            serializer = self.get_serializer(existing_booking, data=request.data, partial=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PersonalBookingView(generics.ListAPIView):
    serializer_class = MealBookingSerializer

    def get_queryset(self):
        date_param = self.request.query_params.get('date', None)
        name_param = self.request.query_params.get('name', None)
        if date_param and name_param:
            return OrderDetail.objects.filter(date=date_param, name=name_param)
        return OrderDetail.objects.none()


class DailyReportView(generics.ListAPIView):
    serializer_class = MealBookingSerializer

    def get_queryset(self):
        date_param = self.request.query_params.get('date', None)
        print(date_param)
        if date_param:
            return OrderDetail.objects.filter(date=date_param)
        return OrderDetail.objects.none()


class CancelBookingView(generics.DestroyAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = MealBookingSerializer

    def delete(self, request, *args, **kwargs):
        date_param = self.request.query_params.get('date', None)
        name_param = self.request.query_params.get('name', None)
        if not date_param or not name_param:
            return Response(
                {"detail": "需要提供date和name参数"},
                status=status.HTTP_400_BAD_REQUEST
            )
        bookings = OrderDetail.objects.filter(date=date_param, name=name_param)
        if bookings.exists():
            bookings.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"detail": "未找到匹配的预订记录"},
            status=status.HTTP_404_NOT_FOUND
        )

    def post(self, request, *args, **kwargs):
        date_param = request.data.get('date')
        name_param = request.data.get('name')

        if not date_param or not name_param:
            return Response(
                {"detail": "需要提供date和name参数"},
                status=status.HTTP_400_BAD_REQUEST
            )
        bookings = OrderDetail.objects.filter(date=date_param, name=name_param)
        if bookings.exists():
            bookings.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"detail": "未找到匹配的预订记录"},
            status=status.HTTP_404_NOT_FOUND
        )


class UserListView(generics.ListCreateAPIView):
    queryset = UserList.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserList.objects.all()
    serializer_class = UserListSerializer
