import os
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductImage

def convert_to_webp(image_path):
    if not image_path.lower().endswith(".webp"):
        img = Image.open(image_path).convert("RGB")
        webp_path = os.path.splitext(image_path)[0] + ".webp"
        img.save(webp_path, "webp", quality=80)
        os.remove(image_path)  # Optional: remove original
        return webp_path
    return image_path

@receiver(post_save, sender=Product)
def convert_product_image(sender, instance, **kwargs):
    if instance.image and not instance.image.name.lower().endswith(".webp"):
        image_path = instance.image.path
        new_path = convert_to_webp(image_path)
        if new_path != image_path:
            instance.image.name = instance.image.name.rsplit(".", 1)[0] + ".webp"
            instance.save(update_fields=["image"])

@receiver(post_save, sender=ProductImage)
def convert_preview_image(sender, instance, **kwargs):
    if instance.image and not instance.image.name.lower().endswith(".webp"):
        image_path = instance.image.path
        new_path = convert_to_webp(image_path)
        if new_path != image_path:
            instance.image.name = instance.image.name.rsplit(".", 1)[0] + ".webp"
            instance.save(update_fields=["image"])
