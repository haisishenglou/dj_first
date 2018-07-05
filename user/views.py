from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import BookInfo
from django.views import View
import json
from rest_framework.viewsets import ModelViewSet,ViewSet,GenericViewSet
from .serializers import BookSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin ,CreateModelMixin
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,BasePermission


# Create your views here.


#  Django函数写法，返回模板
def index(request):
    books = BookInfo.objects.all()
    return render(request, 'index.html', {'books': books})


#  类视图写法
class BooksView(View):
    #  获取所有的书籍信息
    def get(self, requset):
        books = BookInfo.objects.all()
        book_list = []

        for book in books:
            book_list.append({
                "id": book.id,
                "btitle": book.btitle,
                "bpub_date": book.bpub_date,
                "bread": book.bread,
                "bcomment": book.bcomment,
                "is_name": book.is_delete,
                "image": book.image.url if book.image else ''

            })

        return JsonResponse(book_list, safe=False)

    #  新增书籍
    def post(self, requst):
        body_data = requst.body
        body_data = body_data.decode()
        str_data = json.loads(body_data)
        book = BookInfo.objects.create(
            btitle=str_data['btitle'],
            bpub_date=str_data['bpub_date']
        )
        return JsonResponse({
            "id": book.id,
            "btitle": book.btitle,
            "bpub_date": book.bpub_date,
            "bread": book.bread,
            "bcomment": book.bcomment,
            "is_name": book.is_delete,
            "image": book.image.url if book.image else ''

        })


# 操作单独一本书
class BookView(View):
    # 查询 id对应书籍
    def get(self, request, id):
        try:
            book = BookInfo.objects.get(id=id)
        except Exception as e:
            return HttpResponse('id输入有误')

        return JsonResponse({
            "id": book.id,
            "btitle": book.btitle,
            "bpub_date": book.bpub_date,
            "bread": book.bread,
            "bcomment": book.bcomment,
            "is_name": book.is_delete,
            "image": book.image.url if book.image else ''

        })

    # 修改id对应书籍
    def put(self, request, id):
        try:
            book = BookInfo.objects.get(id=id)
        except Exception as e:
            return HttpResponse("id输入有误")

        body_data = request.body
        body_data = body_data.decode()
        str_data = json.loads(body_data)
        book.btitle = str_data.get("btitle")
        book.bpub_date = str_data.get("bpub_date")
        book.save()
        return JsonResponse({
            "id": book.id,
            "btitle": book.btitle,
            "bpub_date": book.bpub_date,
            "bread": book.bread,
            "bcomment": book.bcomment,
            "is_name": book.is_delete,
            "image": book.image.url if book.image else ''

        })

    # 删除id对应书籍
    def delete(self, request, id):
        try:
            book = BookInfo.objects.get(id=id)
        except Exception as e:
            return HttpResponse("id输入有误")

        book.delete()

        return HttpResponse("删除成功")


# APIView写法
class BookAPIView(APIView):
    #  查询所有书籍
    def get(self, request):
        books = BookInfo.objects.all()
        ser = BookSerializer(books, many=True)
        return Response(ser.data)

    #  新增书籍
    def post(self, request):
        data = request.data
        ser = BookSerializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


# GenericAPI写法
class BookInfoView(GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookSerializer

    # 查询指定书籍
    def get(self, request, pk):
        book = self.get_object()
        ser = self.get_serializer(book)
        return Response(ser.data)


# 扩展类写法
class BooksViews(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookSerializer

    # 查询所有书籍
    def get(self, request, *args, **kwargs):
        return self.list(request)

    #  新建书籍
    def post(self, request, *args, **kwargs):
        return self.create(request)


# 子类写法,主要是继承对应的子类
# ListAPIView 继承后，展示所有书籍
# CreateAPIView 继承后，新建书籍
class BooksList(ListAPIView, CreateAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookSerializer


# 视图集写法，继承ViewSet
# class BookSetView(ViewSet):
#
#     def list(self,request):
#         books = BookInfo.objects.all()
#         ser = BookSerializer(books, many= True)
#         return Response(ser.data)
#
#     def retrieve(self,request, pk):
#         book = BookInfo.objects.get(id= pk)
#         ser = BookSerializer(book)
#         return Response(ser.data)


#  自定义权限
class MyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return False

# 分页
class StandardPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 2

#  视图集，继承子类写法
class BookSetView(ListModelMixin, RetrieveModelMixin,GenericViewSet):
    queryset =  BookInfo.objects.all()
    serializer_class = BookSerializer

    # 认证设置
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    # 权限设置
    # permission_classes = (IsAuthenticated,MyPermission)

    #  排序
    ordering_fields = ('id', 'bread', 'bpub_date')

    #  分页
    pagination_class = StandardPageNumberPagination

    #  自定义action
    @action(methods=['get'], detail= False)
    def latest(self,request):
        book = BookInfo.objects.latest("id")
        ser = self.get_serializer(book)
        return Response(ser.data)

    @action(methods=['put'], detail= True)
    def read(self,request, pk ):
        book = self.get_object()
        data = request.data
        ser = self.get_serializer(book,data=data)
        ser.is_valid(raise_exception = True)
        ser.save()
        return Response(ser.data)


# 视图集写法
# class BooksViews(ModelViewSet):
#     queryset = BookInfo.objects.all()
#     serializer_class = BookSerializer
