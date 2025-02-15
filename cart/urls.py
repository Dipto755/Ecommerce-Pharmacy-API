from django.urls import path
from . import views

urlpatterns = [
    path('me/cart', views.ListMeCartView.as_view(), name='me_cart'),
    path('me/cart/details', views.RetrieveMeCartView.as_view(), name='me_cart_details'),
    path('me/cart/cartitems', views.ListMeCartItemsView.as_view(), name='me_cartitems'),
    path('me/cart/add-items/', views.AddCartItemView.as_view(), name='add_cartitems'),
    path('me/cart/remove-item/<str:product__slug>', views.RemoveCartItemView.as_view(), name='remove_cartitem'),
    path('me/orders', views.ListMeOrderView.as_view(), name='my_orders'),
    path('me/orders/orders-for-review', views.ListMeOrdersForReviewView.as_view(), name='my_orders_for_review'),
    path('me/order-details/<str:uid>', views.OrderDetailsView.as_view(), name='my_order_details'),
    path('me/order/add-order', views.AddOrderView.as_view(), name='add_order'),
    path('me/order/my-order/add-items', views.AddOrderItemView.as_view(), name='add_order_items'),
    path('me/order/my-order/remove-item/<str:product__slug>', views.RemoveOrderItemView.as_view(), name='remove_order_item'),
    path('we/order/all-order', views.GetAllOrders.as_view(), name='all_orders'),
    path('we/order/update-order/<str:uid>', views.UpdateOrderView.as_view(), name='update_order'),
    path('me/review/<str:uid>/add-review', views.AddReviewView.as_view(), name='add_review'),
    path('me/reviews', views.MyReviewDetailsView.as_view(), name='my_reviews'),
    
]