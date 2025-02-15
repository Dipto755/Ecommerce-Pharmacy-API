from rest_framework import serializers

from core.models import Product, Category, ProductCategory, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset = Category.objects.filter(),
        # write_only = True,
        slug_field='slug', 
        many=True
    )
    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'price', 'manufacturing_date', 'expired_date', 'image', 
                  'availability', 'avg_rating', 'brand', 'status')
        read_only_fields = ('avg_rating',)
        
        
    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        product = Product.objects.create(**validated_data)
        
        for cat_name in categories:
            category= Category.objects.get(slug=cat_name)
            ProductCategory.objects.create(product = product, category = category)
        return product


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(source = 'review.rating')
    comment = serializers.CharField(source = 'review.comment')
    image = serializers.ImageField(source = 'review.image')
    
    class Meta:
        model = Review
        fields = ('uid','rating', 'comment', 'image', 'added_on')


class PublicProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset = Category.objects.filter(),
        slug_field='slug', 
        many=True
    )
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Product
        fields = ('uid', 'name', 'category', 'description', 'price', 'manufacturing_date', 'expired_date', 'image', 
                  'availability', 'avg_rating', 'brand', 'reviews')

        

