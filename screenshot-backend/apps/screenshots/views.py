from pathlib import Path
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class BrandListView(APIView):
    """获取品牌列表（一级目录）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        screenshots_dir = settings.SCREENSHOTS_ROOT
        brands = []

        if screenshots_dir.exists():
            for item in sorted(screenshots_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    brands.append(item.name)

        return Response({'brands': brands})


class ModelListView(APIView):
    """获取型号列表（二级目录）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        if not brand:
            return Response({'error': '请指定品牌'}, status=400)

        brand_dir = settings.SCREENSHOTS_ROOT / brand
        models = []

        if brand_dir.exists():
            for item in sorted(brand_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    models.append(item.name)

        return Response({'models': models})


class VersionListView(APIView):
    """获取版本列表（三级目录）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        model = request.query_params.get('model', '')

        if not brand or not model:
            return Response({'error': '请指定品牌和型号'}, status=400)

        model_dir = settings.SCREENSHOTS_ROOT / brand / model
        versions = []

        if model_dir.exists():
            for item in sorted(model_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    versions.append(item.name)

        return Response({'versions': versions})


class ImageSearchView(APIView):
    """搜索图片"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        model = request.query_params.get('model', '')
        version = request.query_params.get('version', '')
        keyword = request.query_params.get('keyword', '')

        if not brand or not model:
            return Response({'error': '请指定品牌和型号'}, status=400)
        if not keyword:
            return Response({'error': '请输入搜索关键词'}, status=400)

        # 构建目录路径
        if version:
            target_dir = settings.SCREENSHOTS_ROOT / brand / model / version
        else:
            target_dir = settings.SCREENSHOTS_ROOT / brand / model

        images = []
        if target_dir.exists():
            images = self._search_images(target_dir, keyword, brand)

        return Response({'images': images})

    def _search_images(self, directory, keyword, brand):
        """递归搜索匹配关键词的图片"""
        images = []
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

        for item in directory.rglob('*'):
            if item.is_file() and item.suffix.lower() in image_extensions:
                if keyword.lower() in item.stem.lower():
                    rel_path = item.relative_to(settings.SCREENSHOTS_ROOT)
                    images.append({
                        'name': item.stem,
                        'filename': item.name,
                        'path': f'/screenshots/{rel_path.as_posix()}',
                    })

        return sorted(images, key=lambda x: x['name'])
