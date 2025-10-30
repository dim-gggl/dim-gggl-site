from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def optimize_image(image_field, max_width=1920, quality=85):
    """Compress and resize uploaded images for optimal delivery."""

    image = Image.open(image_field)

    if image.mode in {"RGBA", "LA", "P"}:
        image = image.convert("RGB")

    if image.width > max_width:
        ratio = max_width / float(image.width)
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height), Image.LANCZOS)

    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)

    file_name = image_field.name.rsplit(".", 1)[0] + ".jpg"
    return InMemoryUploadedFile(
        buffer,
        field_name="ImageField",
        name=file_name,
        content_type="image/jpeg",
        size=buffer.getbuffer().nbytes,
        charset=None,
    )

def get_client_ip(request):
    """
    Get the client's IP address from the request.
    Handles proxies correctly.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Take the first IP if there are multiple
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip