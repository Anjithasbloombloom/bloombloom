from django.urls import path
from . import views

urlpatterns =[
    path('index/',views.index,name='index'),
    path('create/', views.create_course, name='create_course'),
    path('select/<int:id>/',views.select_featured.as_view(),name='select_featured'),
    path('page/',views.page,name='page'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('add_new_course/<int:id>', views.AddNewCourse.as_view(), name='add_new_course'),
    path('detail/',views.detail,name='detail'),
    path('latest/',views.latest_lauches,name='latest_lauches'),
    path('indexes/',views.indexes,name='indexes'),
    # path('my_view/',views.my_view,name="my_view"),
    # path('index/',views.index,name='index'),

    

]



