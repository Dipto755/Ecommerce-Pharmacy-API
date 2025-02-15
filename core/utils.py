def generate_user_slug(instance):
    return instance.username

def generate_organization_slug(instance):
    return instance.name

def generate_user_organization_slug(instance):
    return f"{instance.user.username}-{instance.organization.name}-{instance.role}".lower()

def generate_category_slug(instance):
    return f"{instance.name}".lower()

def generate_product_slug(instance):
    return f"{instance.brand}-{instance.name}".lower()

# def generate_product_organization_slug(instance):
#     return f"{instance.organization.name}-{instance.product.brand}-{instance.product.name}"

def generate_product_category_slug(instance):
    return f"{instance.product.name}-{instance.category.name}".lower()

def generate_cart_slug(instance):
    return f"{instance.user.username}-cart".lower()

def generate_cart_item_slug(instance):
    return f"{instance.cart.slug}-item-{instance.product.name}".lower()

def generate_order_slug(instance):
    return f"{instance.added_on}-{instance.status}".lower()

def generate_order_item_slug(instance):
    return f"{instance.product}".lower()

# def generate_

