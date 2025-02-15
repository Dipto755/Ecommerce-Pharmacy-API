from rest_framework import generics
from rest_framework import permissions as drf_permissions

from .serializers import (CartSerializer, CartDetailsSerializer, CartItemSerializer, AddCartItemSerializer,
                          AddOrderSerializer, GetOrderSerializer, AddOrderItemSerializer, OrderSerializer,
                          ReviewSerializer, MyReviewDetailsSerializer, GetOrderForReviewSerializer)

from core.models import Cart, CartItem, Order, OrderItem, ProductReview, Review
from core.choices import OrderCreateChoices, OrderStatusChoices

from core import permissions as custom_permissions

class ListMeCartView(generics.ListAPIView):

    serializer_class = CartSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user).select_related('user')
    
class RetrieveMeCartView(generics.ListAPIView):

    serializer_class = CartDetailsSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user).prefetch_related('items').select_related('user')
    
class ListMeCartItemsView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        cart = Cart.objects.get(user = user)
        return CartItem.objects.filter(cart=cart)

class AddCartItemView(generics.CreateAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        cart = Cart.objects.get(user=self.request.user)
        
        context = super().get_serializer_context()
        
        context['cart'] = cart
        
        return context
        
    def perform_create(self, serializer):
        serializer.save()
    

class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = 'product__slug'
    
    def get_object(self):
        return CartItem.objects.get(product__slug = self.kwargs['product__slug'])
    
    
class ListMeOrderView(generics.ListAPIView):
    serializer_class = GetOrderSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items').select_related('user')
    
class ListMeOrdersForReviewView(generics.ListAPIView):
    serializer_class = GetOrderForReviewSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status=OrderStatusChoices.Delivered, review_status__in=['partially_reviewed', 'not_reviewed']).select_related('user').order_by('pk')

class AddOrderView(generics.CreateAPIView):
    serializer_class = AddOrderSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    

class AddOrderItemView(generics.CreateAPIView):
    serializer_class = AddOrderItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        order = Order.objects.get(user=self.request.user, status=OrderCreateChoices.New)
        context = super().get_serializer_context()
        context['order'] = order
        context['user'] = self.request.user
        return context
    

class RemoveOrderItemView(generics.DestroyAPIView):
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = 'product__slug'
    
    def get_object(self):
        order = Order.objects.get(user = self.request.user, status = OrderCreateChoices.New)
        return OrderItem.objects.get(order = order, product__slug=self.kwargs['product__slug'])
    
    
class OrderDetailsView(generics.RetrieveAPIView):
    serializer_class = GetOrderSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = 'uid'
    
    def get_queryset(self):
        return Order.objects.filter(uid = self.kwargs['uid'], user=self.request.user).prefetch_related('items').select_related('user')

class GetAllOrders(generics.ListAPIView):
    queryset = Order.objects.filter().select_related('user').order_by('pk')
    serializer_class = OrderSerializer
    permission_classes = [custom_permissions.IsOrganizationManager]
    

class UpdateOrderView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [custom_permissions.IsOrganizationManager]
    lookup_field = 'uid'
    
    def get_queryset(self):
        return Order.objects.filter(uid = self.kwargs['uid']).select_related('user')
    
class AddReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = 'uid'
    
    def get_serializer_context(self):
        order = Order.objects.get(uid=self.kwargs['uid'])
        context = super().get_serializer_context()
        context['order'] = order
        
        return context
        
    
    def perform_create(self, serializer):
        user = self.request.user
        order = Order.objects.get(uid=self.kwargs['uid'])
        
        serializer.save(user=user, order=order)
        
        
class MyReviewDetailsView(generics.ListAPIView):
    serializer_class = MyReviewDetailsSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_reviews = Review.objects.filter(user=self.request.user)
        return ProductReview.objects.filter(review__in = user_reviews).prefetch_related('review', 'product').order_by('pk')

