from django.http import Http404
from rest_framework import generics
from rest_framework import permissions as drf_permissions

from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    AddCartItemSerializer,
    AddOrderItemSerializer,
    AddOrderSerializer,
    CartDetailsSerializer,
    CartItemSerializer,
    DeliveredOrderSerializer,
    GetOrderSerializer,
    ReviewMediaRoomSerializer,
    MyReviewDetailsSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ReviewSerializer,
)


from core.models import (
    Cart,
    CartItem,
    MediaRoom,
    MediaRoomConnector,
    Order,
    OrderItem,
    Product,
    ProductReview,
    Review,
    UserOrganization,
)
from core.choices import OrderCreateChoices, OrderStatusChoices

from core import permissions as custom_permissions

# class ListMeCartView(generics.ListAPIView):

#     serializer_class = CartSerializer
#     permission_classes = [drf_permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Cart.objects.filter(user=user).select_related('user')


class RetrieveMeCartView(generics.ListAPIView):
    serializer_class = CartDetailsSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Cart.objects.filter(user=user)
            .prefetch_related("items")
            .select_related("user")
        )


class ListCreateCartItemsView(generics.ListCreateAPIView):
    # serializer_class = CartItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["product__name"]
    ordering_fields = ["quantity", "sub_total"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        cart = Cart.objects.get(user=self.request.user)
        context = super().get_serializer_context()
        context["cart"] = cart
        return context

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        return CartItem.objects.filter(cart=cart)


# class AddCartItemView(generics.CreateAPIView):
#     serializer_class = AddCartItemSerializer
#     permission_classes = [drf_permissions.IsAuthenticated]

#     def get_serializer_context(self):
#         cart = Cart.objects.get(user=self.request.user)

#         context = super().get_serializer_context()

#         context['cart'] = cart

#         return context

#     def perform_create(self, serializer):
#         serializer.save()


class RetrieveUpdateRemoveCartItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = "uid"

    # def get_serializer_class(self):
    #     if self.request.method == "GET":
    #         return CartItemSerializer
    #     return AddCartItemSerializer

    def get_object(self):
        return CartItem.objects.get(uid=self.kwargs["uid"])


class ListMeOrderView(generics.ListAPIView):
    serializer_class = GetOrderSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status", "review_status"]
    ordering_fields = ["added_on", "delivery_date", "grand_total"]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items")
            .select_related("user")
            .order_by("pk")
        )


class ListMeDeliveredOrdersView(generics.ListAPIView):
    serializer_class = DeliveredOrderSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["review_status"]
    ordering_fields = ["added_on", "delivery_date"]

    def get_queryset(self):
        return (
            Order.objects.IS_DELIVERED().filter(
                user=self.request.user,
                # review_status__in=["PARTIALLY_REVIEWED", "NOT_REVIEWED"],
            )
            .select_related("user")
            .order_by("pk")
        )


class RetrieveMeDeliveredOrderView(generics.RetrieveAPIView):
    serializer_class = DeliveredOrderSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = "uid"

    def get_object(self):
        try:
            order = Order.objects.IS_DELIVERED().get(
                uid=self.kwargs["order_uid"], review_status__in=["PARTIALLY_REVIEWED", "NOT_REVIEWED"]
            )
            
        except Order.DoesNotExist:
            raise Http404("Order does not exist")
        return order
        # return Order.objects.get(
        #     uid=self.kwargs["order_uid"], status=OrderStatusChoices.DELIVERED, review_status__in=["PARTIALLY_REVIEWED", "NOT_REVIEWED"]
        # )


class AddOrderView(generics.CreateAPIView):
    serializer_class = AddOrderSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddOrderItemView(generics.CreateAPIView):
    serializer_class = AddOrderItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    # def get_serializer_context(self):
    #     order = Order.objects.get(user=self.request.user, status=OrderCreateChoices.NEW)
    #     context = super().get_serializer_context()
    #     context['order'] = order
    #     context['user'] = self.request.user
    #     return context


class RetrieveRemoveOrderItemView(generics.RetrieveDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = "item_uid"

    def get_object(self):
        order = Order.objects.get(user=self.request.user, status=OrderCreateChoices.NEW)
        return OrderItem.objects.get(
            uid=self.kwargs["item_uid"],
            order=order,
            delivery_status=OrderCreateChoices.NEW,
        )


class OrderDetailsView(generics.RetrieveAPIView):
    serializer_class = GetOrderSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = "uid"

    def get_queryset(self):
        return (
            Order.objects.filter(uid=self.kwargs["uid"], user=self.request.user)
            .prefetch_related("items")
            .select_related("user")
        )


class GetAllOrders(generics.ListAPIView):
    # queryset = Order.objects.filter().select_related('user').order_by('pk')
    serializer_class = OrderSerializer
    permission_classes = [custom_permissions.IsOrganizationManager]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["user__username"]
    filterset_fields = ["status"]
    ordering_fields = ["delivery_date"]

    def get_queryset(self):
        user_orgs = UserOrganization.objects.IS_ACTIVE().filter(user=self.request.user).values_list(
            "organization", flat=True
        )
        products = Product.objects.filter(organization__in=user_orgs).values_list(
            "id", flat=True
        )
        order_items = OrderItem.objects.filter(product__in=products).values_list(
            "order", flat=True
        )

        return (
            Order.objects.filter(id__in=order_items)
            .select_related("user")
            .order_by("pk")
        )


class RetrieveUpdateOrderView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [custom_permissions.IsOrganizationManager]
    lookup_field = "uid"

    def get_queryset(self):
        return Order.objects.filter(uid=self.kwargs["uid"]).select_related("user")


# class RetrieveUpdateOrderView(generics.RetrieveUpdateAPIView):
#     serializer_class = OrderSerializer


class AddReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = "uid"

    def get_serializer_context(self):
        order = Order.objects.get(uid=self.kwargs["order_uid"])
        context = super().get_serializer_context()
        context["order"] = order

        return context

    def perform_create(self, serializer):
        user = self.request.user
        order = Order.objects.get(uid=self.kwargs["order_uid"])

        serializer.save(user=user, order=order)


class ListCreateReviewImageView(generics.ListCreateAPIView):
    serializer_class = ReviewMediaRoomSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    lookup_field = 'uid'
    
    def get_queryset(self):
        review = Review.objects.get(uid=self.kwargs['uid'])
        
        try:
            medias = MediaRoomConnector.objects.filter(review=review)
        except MediaRoomConnector.DoesNotExist:
            raise Http404("Images for this review do not exist")
        
        return MediaRoom.objects.filter(id__in=medias)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['uid'] = self.kwargs['uid']
        return context


class MyReviewDetailsView(generics.ListAPIView):
    serializer_class = MyReviewDetailsSerializer
    permission_classes = [drf_permissions.IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ["product__name", "comment"]
    ordering_fields = ["added_on", "rating"]

    def get_queryset(self):
        user_reviews = Review.objects.filter(user=self.request.user)
        return (
            ProductReview.objects.filter(review__in=user_reviews)
            .prefetch_related("review", "product")
            .order_by("pk")
        )

# class RetrieveMyReviewView(generics.RetrieveAPIView):
#     serializer_class = MyReviewDetailsSerializer
#     permission_classes = [drf_permissions.IsAuthenticated]
#     lookup_field = 'uid'
    
#     def get_object(self):
#         return 

