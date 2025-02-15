from rest_framework import serializers

from core.models import Cart, CartItem, Category, Product, Order, OrderItem, Review, ProductReview

from product.serializers import PublicProductSerializer

from core.choices import (
    OrderStatusChoices, 
    ReviewStatusChoices,
    ReviewStatusForOrderChoices,
    ProductStockChoices)


class CartItemSerializer(serializers.ModelSerializer):
    product = PublicProductSerializer(many= False)
    sub_total = serializers.SerializerMethodField(method_name='total')
    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'sub_total')
        
    def total(self, cartitem:CartItem):
        return cartitem.product.price * cartitem.quantity
        


class CartSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    class Meta:
        model = Cart
        fields = ('uid', 'username')
        
class CartDetailsSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    items = CartItemSerializer(many = True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')
    class Meta:
        model = Cart
        fields = ('uid', 'username', 'items', 'grand_total')
        
    def main_total(self, cart:Cart):
        items = cart.items.all()
        total = sum(item.product.price * item.quantity for item in items )
        return total
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.filter(availability = ProductStockChoices.InStock),
        slug_field='slug',
        many=False,
        help_text = "brand1-prod1"
    )
    quantity = serializers.IntegerField()
    
    class Meta:
        model = CartItem
        fields = ('product', 'quantity')
        
    def create(self, validated_data):
        prod = validated_data.pop('product', None)
        quantity = validated_data.pop('quantity', 0)
        cart = self.context['cart']
        
        return CartItem.objects.create(cart = cart, product = prod, quantity = quantity, **validated_data)
    
        

class OrderItemSerializer(serializers.ModelSerializer):
    product = PublicProductSerializer(many= False)
    sub_total = serializers.SerializerMethodField(method_name='total')
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'sub_total')
        
    def total(self, orderitem:OrderItem):
        return orderitem.product.price * orderitem.quantity
        

class AddOrderSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    class Meta:
        model = Order
        fields = ('uid', 'username', 'status')
        read_only_fields = ('status',)
        
class OrderSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    delivery_date = serializers.DateField()
    status = serializers.ChoiceField(choices=OrderStatusChoices.CHOICES)
    
    class Meta:
        model = Order
        fields = ('uid', 'username', 'delivery_date', 'status')
        
    def update(self, instance, validated_data):
        if instance.status == OrderStatusChoices.Delivered:
            raise serializers.ValidationError("Order cannot be updated after delivery.")
        return validated_data
        

class GetOrderSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    items = OrderItemSerializer(many=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')
    class Meta:
        model = Order
        fields = ('uid', 'username', 'added_on', 'delivery_date', 'status', 'items', 'grand_total', 'review_status')
        
    def main_total(self, order:Order):
        items = order.items.all()
        total = sum(item.product.price * item.quantity for item in items )
        return total
        
        
class GetOrderForReviewSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    class Meta:
        model = Order
        fields = ('uid', 'username', 'added_on', 'delivery_date', 'review_status')

class AddOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')
        read_only_fields = ('product', 'quantity')
        
    
    def create(self, validated_data):
        cart = Cart.objects.get(user = self.context['request'].user)
        order_items=[]
        for item in cart.items.all():
            order_items.append(OrderItem(order=self.context['order'], product=item.product, quantity=item.quantity))
        
        cart.items.all().delete()
        OrderItem.objects.bulk_create(order_items)
        return OrderItem.objects.filter(order = self.context['order'])
        

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.CharField(write_only=True)
    order_uid = serializers.CharField(source = 'order.uid', read_only = True)
    rating = serializers.ChoiceField(choices=[(i ,i) for i in range(1,6)])
    
    class Meta:
        model = Review
        fields = ('uid', 'order_uid', 'product', 'rating', 'comment', 'image', 'added_on')
        read_only_fields = ('uid', 'order_uid', 'added_on')
        
    def validate_product(self, data):
        product = Product.objects.get(slug = data)
        if product is None:
            raise serializers.ValidationError("Product does not exist")
        if not OrderItem.objects.filter(product=product, order = self.context['order'], review_status=ReviewStatusChoices.NotReviewed).exists():
            raise serializers.ValidationError("Product is not available for review")
        
        return product
        
    def create(self, validated_data):
        product = validated_data.pop('product')
        user = self.context['request'].user
        order = self.context['order']
        
        review = Review.objects.create(**validated_data)
        order_item = OrderItem.objects.get(product=product, order=order)
        order_item.review_status = ReviewStatusChoices.Reviewed
        order_item.save()
        order_items = OrderItem.objects.filter(order = order)
        order_items_count = order_items.count()
        cnt = 0
        for o_item in order_items:
            if o_item.review_status == ReviewStatusChoices.Reviewed:
                cnt+=1
                
        if cnt == order_items_count:
            order.review_status = ReviewStatusForOrderChoices.Reviewed
            order.save()
        elif cnt > 0:
            order.review_status = ReviewStatusForOrderChoices.PartiallyReviewed
            order.save()
        product_review = ProductReview.objects.create(product=product, review=review)
        return review
        
class ProductReviewSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True)
    class Meta:
        model = ProductReview
        fields = ['review']

class ReviewDetailsSerializer(serializers.ModelSerializer):
    order_uid = serializers.CharField(source = 'order.uid', read_only = True)   
    class Meta:
        model = Review
        fields = ('uid', 'order_uid', 'added_on')
        read_only_fields = ('uid', 'order_uid', 'added_on')
        

class MyReviewedProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset = Category.objects.filter(),
        slug_field='slug', 
        many=True
    )
    class Meta:
        model = Product
        fields = ('uid', 'name', 'category', 'description', 'price', 'manufacturing_date', 'expired_date', 'image', 
                  'availability', 'avg_rating', 'brand')

class MyReviewDetailsSerializer(serializers.ModelSerializer):
    product = MyReviewedProductSerializer()
    rating = serializers.IntegerField(source='review.rating')
    comment = serializers.CharField(source='review.comment')
    image = serializers.ImageField(source='review.image')
    added_on = serializers.DateTimeField(source='review.added_on')
    class Meta:
        model = ProductReview
        fields = ['product', 'rating', 'comment', 'image', 'added_on']
