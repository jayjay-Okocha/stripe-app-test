from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<int:item_id>', views.buy_item, name='buy'),
    path('item/<int:item_id>', views.get_item, name='get-item'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
]