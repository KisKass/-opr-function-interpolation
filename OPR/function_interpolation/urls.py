from django.urls import path

from . import views  # it means - 'from all import views'

urlpatterns = [
    path('', views.index, name='index'),
    path('excel', views.excel, name='excel'),
    # path('new_points', views.new_points, name='new_points'),

]

# whenever 'localhost:8000' will be called, function named 'index' will be called that is present in 'views.py' file
# This will happen for all other routes as well
