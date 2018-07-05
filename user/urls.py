from django.conf.urls import url,include
from . import views
from rest_framework.routers import DefaultRouter,SimpleRouter

# 视图集路由SimpleRouter写法
route = SimpleRouter()
route.register(r'book', views.BookSetView, base_name= 'books')

urlpatterns = [

    # url(r'^index/$', views.index),
    # url(r'^books/', views.BooksView.as_view()),
    # url(r'book/(?P<id>\d+)/',views.BookView.as_view()).
    url(r'^Books/', views.BookAPIView.as_view()),
    url(r'^Books/(?P<pk>\d+)/$', views.BookInfoView.as_view()),
    url(r'^Book/', views.BooksViews.as_view()),
    url(r'^Booklist/',views.BooksList.as_view()),

    # url(r'^Bookset/$', views.BookSetView.as_view({'get':'list'})),
    # url(r'^Bookset/latest/$', views.BookSetView.as_view({'get':'latest'})),
    # url(r'^Bookset/(?P<pk>\d+)/$', views.BookSetView.as_view({'get':'retrieve'})),
    # url(r'^Bookset/read/(?P<pk>\d+)/$', views.BookSetView.as_view({'put':'read'})),

    url(r'', include(route.urls)),
]

# route = DefaultRouter()
# route.register(r'Books',views.BooksViews)
# urlpatterns += route.urls
