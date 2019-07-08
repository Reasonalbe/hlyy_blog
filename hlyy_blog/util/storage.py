from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


class WatermarkStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        # 保存文件时的处理
        if 'image' in content.content_type:
            # 加水印
            image = self.wartermark_with_text(content, 'HLYY Blog', 'red')
            # 将加完水印的Image对象转换为文件对象
            content = self.conver_image_to_file(image, name)
        return super().save(name, content, max_length=max_length)

    def conver_image_to_file(self, image, name):
        """将Image对象转为文件对象已便于存储"""
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)

    def wartermark_with_text(self, file_obj, text, color, fontfamily=None):
        """将水印加在图片的右下角"""
        image = Image.open(file_obj).conver('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        text_width, text_height = draw.textsize(text, font)
        # 水印在图片右下角
        x = width - text_width - margin
        y = height - text_height - margin
        draw.text((x, y), text, color, font)
        return image


