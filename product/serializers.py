from rest_framework import serializers

from core.models import (
    Category,
    MediaRoom,
    MediaRoomConnector,
    Organization,
    Product,
    ProductCategory,
    Review,
    UserOrganization,
)

from core.choices import ProductStockChoices, StatusChoices


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "description")


class MediaRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaRoom
        fields = ("id", "uid", "file")
        read_only_fields = ("id", "uid")

    def create(self, validated_data):
        media = MediaRoom.objects.create(**validated_data)

        product = Product.objects.get(uid=self.context["prod_uid"])

        MediaRoomConnector.objects.create(mediaroom=media, product=product)

        return media


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.IS_ACTIVE(),
        # write_only = True,
        slug_field="slug",
        many=True,
    )
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.IS_ACTIVE(),
        slug_field="slug",
    )
    image = MediaRoomSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "uid",
            "name",
            "organization",
            "category",
            "description",
            "price",
            "manufacturing_date",
            "expiry_date",
            "image",
            "stock",
            "availability",
            "avg_rating",
            "brand",
            "status",
        )
        read_only_fields = ("avg_rating",)

    def validate_organization(self, data):
        orgs = UserOrganization.objects.IS_ACTIVE().filter(
            user=self.context["request"].user
        ).values_list("organization", flat=True)

        curr_user_organizations = Organization.objects.filter(id__in=orgs)

        # org = Organization.objects.get(slug = data)

        if data not in curr_user_organizations:
            raise serializers.ValidationError(
                "You must have to be internal member of the organization to add product."
            )

        return data

    def create(self, validated_data):
        categories = validated_data.pop("category", [])
        product = Product.objects.create(**validated_data)

        for cat_name in categories:
            category = Category.objects.IS_ACTIVE().get(slug=cat_name)
            ProductCategory.objects.create(product=product, category=category)
        return product

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        stock = validated_data.get("stock", None)
        # print(validated_data)
        if stock is not None:
            if instance.stock > 0:
                instance.availability = ProductStockChoices.IN_STOCK
        instance.save()

        return instance


# class ProductOrganizationSerializer(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(
#         queryset = Category.objects.filter(),
#         slug_field='slug',
#         many=True
#     )
#     name = serializers.CharField(source="product.name")
#     description = serializers.CharField(source="product.description")
#     brand = serializers.CharField(source="product.brand")
#     organization = serializers.SlugRelatedField(
#         queryset=Organization.objects.filter(status=StatusChoices.ACTIVE),
#         slug_field="slug"
#     )
#     class Meta:
#         model = ProductOrganization
#         fields = ('name', 'organization','category', 'description', 'price', 'manufacturing_date', 'expired_date', 'image',
#                   'availability', 'avg_rating', 'brand', 'status')
#         read_only_fields = ('avg_rating',)


#     def create(self, validated_data):
#         categories = validated_data.pop('category', [])
#         name = validated_data.pop('name')
#         description = validated_data.pop('description')
#         brand = validated_data.pop('brand')
#         product = Product.objects.get_or_create(name=name, brand=brand)
#         product.description = description
#         product.save()

#         product_organization = ProductOrganization.objects.create(**validated_data)

#         for cat_name in categories:
#             category= Category.objects.get(slug=cat_name)
#             ProductCategory.objects.create(product_org = product_organization, category = category)
#         return product


class ProductReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(source="review.rating")
    comment = serializers.CharField(source="review.comment")
    image = serializers.ImageField(source="review.image")

    class Meta:
        model = Review
        fields = ("uid", "rating", "comment", "image", "added_on")


class PublicProductSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source="organization.name")
    category = serializers.SlugRelatedField(
        queryset=Category.objects.IS_ACTIVE(), slug_field="slug", many=True
    )
    reviews = ProductReviewSerializer(many=True)
    image = MediaRoomSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "uid",
            "name",
            "organization",
            "category",
            "description",
            "price",
            "manufacturing_date",
            "expiry_date",
            "image",
            "stock",
            "availability",
            "avg_rating",
            "brand",
            "reviews",
        )
