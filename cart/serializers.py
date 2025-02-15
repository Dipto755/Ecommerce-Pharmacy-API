from rest_framework import serializers

from core.models import (
    Cart,
    CartItem,
    Category,
    MediaRoom,
    MediaRoomConnector,
    Product,
    Order,
    OrderItem,
    Review,
    ProductReview,
    UserOrganization,
)

from product.serializers import PublicProductSerializer

from core.choices import (
    OrderStatusChoices,
    ProductStockChoices,
    ReviewStatusChoices,
    ReviewStatusForOrderChoices,
    StatusChoices,
)

class ReviewMediaRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaRoom
        fields = ("id", "uid", "file")
        read_only_fields = ("id", "uid")
        
    def create(self, validated_data):
        media = MediaRoom.objects.create(**validated_data)

        review = Review.objects.get(uid=self.context['uid'])
        
        MediaRoomConnector.objects.create(mediaroom=media, review=review)
        
        return media

class CartItemSerializer(serializers.ModelSerializer):
    product = PublicProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItem
        fields = ("id", "uid", "product", "quantity", "sub_total")

    def total(self, cartitem: CartItem) -> float:
        return cartitem.product.price * cartitem.quantity


class CartSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Cart
        fields = ("uid", "username")


class CartDetailsSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    items = CartItemSerializer(many=True)
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = ("uid", "username", "items", "grand_total")

    def main_total(self, cart: Cart) -> float:
        items = cart.items.all()
        total = sum(item.product.price * item.quantity for item in items)
        return total


class AddCartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.IS_IN_STOCK(),
        slug_field="slug",
        many=False,
        help_text="brand1-prod1",
    )
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ("product", "quantity")

    def validate_quantity(self, data):
        prod_slug = self.initial_data.get("product")
        prod = Product.objects.get(slug=prod_slug)
        if data == 0:
            raise serializers.ValidationError("Quantity cannot be zero")

        if prod.stock < data:
            raise serializers.ValidationError("Not enough stock!")
        return data

    def create(self, validated_data):
        prod = validated_data.pop("product", None)
        quantity = validated_data.pop("quantity", 0)
        cart = self.context["cart"]
        # prod.stock = prod.stock - quantity
        # if prod.stock == 0:
        #     prod.availability = ProductStockChoices.OUTOFSTOCK
        # prod.save()
        return CartItem.objects.create(
            cart=cart, product=prod, quantity=quantity, **validated_data
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product = PublicProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = OrderItem
        fields = ("id", "uid", "product", "quantity", "sub_total", "delivery_status")

    def total(self, orderitem: OrderItem) -> float:
        return orderitem.product.price * orderitem.quantity


class AddOrderSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Order
        fields = ("uid", "username", "status")
        read_only_fields = ("status",)


class OrderSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    delivery_date = serializers.DateField()
    status = serializers.ChoiceField(choices=OrderStatusChoices)

    class Meta:
        model = Order
        fields = ("uid", "username", "delivery_date", "status")

    def update(self, instance, validated_data):
        if instance.status == OrderStatusChoices.DELIVERED:
            raise serializers.ValidationError("Order cannot be updated after delivery.")

        user_orgs = UserOrganization.objects.IS_ACTIVE().filter(
            user=self.context["request"].user
        ).values_list("organization", flat=True)
        order_items = OrderItem.objects.filter(
            order=instance, product__organization__in=user_orgs
        )
        if not order_items.exists():
            raise serializers.ValidationError("Items not found")
        for item in order_items:
            item.delivery_status = validated_data.get("status")
        OrderItem.objects.bulk_update(order_items, ["delivery_status"])

        if (
            validated_data.get("status") == OrderStatusChoices.PROCESSING
            or validated_data.get("status") == OrderStatusChoices.SHIPPED
        ):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        else:
            # all_order_items = OrderItem.objects.filter(order=instance)
            if (
                OrderItem.objects.filter(order=instance).count()
                == OrderItem.objects.IS_DELIVERED().filter(
                    order=instance
                ).count()
            ):
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
            else:
                status = validated_data.pop("status")
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
        instance.save()
        return instance


class GetOrderSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    items = OrderItemSerializer(many=True)
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Order
        fields = (
            "uid",
            "username",
            "added_on",
            "delivery_date",
            "status",
            "items",
            "grand_total",
            "review_status",
        )

    def main_total(self, order: Order) -> float:
        items = order.items.all()
        total = sum(item.product.price * item.quantity for item in items)
        return total


class DeliveredOrderItemSerializer(serializers.ModelSerializer):
    product = PublicProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = ("product",)


class DeliveredOrderSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    items = DeliveredOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "uid",
            "username",
            "added_on",
            "delivery_date",
            "review_status",
            "items",
        )


class AddOrderItemSerializer(serializers.ModelSerializer):
    order = AddOrderSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ("order", "product", "quantity")
        read_only_fields = ("order", "product", "quantity")

    def create(self, validated_data):
        cart = Cart.objects.get(user=self.context["request"].user)
        order = Order.objects.create(user=self.context["request"].user)
        order_items = []
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                raise serializers.ValidationError("Not enough stock for this product")
            order_items.append(
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )
            )

            item.product.stock = item.product.stock - item.quantity
            if item.product.stock == 0:
                item.product.availability = ProductStockChoices.OUT_OF_STOCK
            item.product.save()

        cart.items.all().delete()
        OrderItem.objects.bulk_create(order_items)
        # return OrderItem.objects.filter(order=self.context["order"])
        return validated_data


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.CharField(write_only=True)
    order_uid = serializers.CharField(source="order.uid", read_only=True)
    rating = serializers.ChoiceField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        model = Review
        fields = (
            "uid",
            "order_uid",
            "product",
            "rating",
            "comment",
            "image",
            "added_on",
        )
        read_only_fields = ("uid", "order_uid", "added_on")

    def validate_product(self, data):
        product = Product.objects.get(slug=data)
        if product is None:
            raise serializers.ValidationError("Product does not exist")
        if not OrderItem.objects.IS_REVIEWED().filter(
            product=product,
            order=self.context["order"],
        ).exists():
            raise serializers.ValidationError("Product is not available for review")

        return product

    def create(self, validated_data):
        product = validated_data.pop("product")
        user = self.context["request"].user
        order = self.context["order"]

        review = Review.objects.create(**validated_data)
        order_item = OrderItem.objects.get(product=product, order=order)
        order_item.review_status = ReviewStatusChoices.REVIEWED
        order_item.save()
        order_items = OrderItem.objects.filter(order=order)
        order_items_count = order_items.count()
        cnt = 0
        for o_item in order_items:
            if o_item.review_status == ReviewStatusChoices.REVIEWED:
                cnt += 1

        if cnt == order_items_count:
            order.review_status = ReviewStatusForOrderChoices.REVIEWED
            order.save()
        elif cnt > 0:
            order.review_status = ReviewStatusForOrderChoices.PARTIALLY_REVIEWED
            order.save()
        product_review = ProductReview.objects.create(product=product, review=review)
        return review


class ProductReviewSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True)

    class Meta:
        model = ProductReview
        fields = ["review"]


class ReviewDetailsSerializer(serializers.ModelSerializer):
    order_uid = serializers.CharField(source="order.uid", read_only=True)

    class Meta:
        model = Review
        fields = ("uid", "order_uid", "added_on")
        read_only_fields = ("uid", "order_uid", "added_on")


class MyReviewedProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.IS_ACTIVE(), slug_field="slug", many=True
    )
    image = ReviewMediaRoomSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "uid",
            "name",
            "category",
            "description",
            "price",
            "manufacturing_date",
            "expiry_date",
            "image",
            "availability",
            "avg_rating",
            "brand",
        )


class MyReviewDetailsSerializer(serializers.ModelSerializer):
    product = MyReviewedProductSerializer()
    rating = serializers.IntegerField(source="review.rating")
    comment = serializers.CharField(source="review.comment")
    image = serializers.ImageField(source="review.image")
    added_on = serializers.DateTimeField(source="review.added_on")
    uid = serializers.CharField(source='review.uid')

    class Meta:
        model = ProductReview
        fields = ["uid", "product", "rating", "comment", "image", "added_on"]
        

