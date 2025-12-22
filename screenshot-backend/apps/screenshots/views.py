from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
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
            return Response({'error': 'Please specify brand'}, status=400)

        brand_dir = settings.SCREENSHOTS_ROOT / brand
        models = []

        if brand_dir.exists():
            for item in sorted(brand_dir.iterdir()):
                # 排除隐藏目录和 data 目录
                if item.is_dir() and not item.name.startswith('.') and item.name != 'data':
                    models.append(item.name)

        return Response({'models': models})


class VersionListView(APIView):
    """获取版本列表（三级目录）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        model = request.query_params.get('model', '')

        if not brand or not model:
            return Response({'error': 'Please specify brand and model'}, status=400)

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
            return Response({'error': 'Please specify brand and model'}, status=400)
        if not keyword:
            return Response({'error': 'Please enter search keyword'}, status=400)

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


class HtmlListView(APIView):
    """获取品牌目录下的 JSON 数据文件列表"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        if not brand:
            return Response({'error': 'Please specify brand'}, status=400)

        data_dir = settings.SCREENSHOTS_ROOT / brand / 'data'
        files = []

        if data_dir.exists():
            for item in sorted(data_dir.glob('*.json')):
                if item.is_file():
                    name = item.stem.replace('_', ' ')
                    files.append({
                        'name': name,
                        'filename': item.name,
                    })

        return Response({'files': files})


class HtmlContentView(APIView):
    """获取 HTML 文件内容（JSON 数据 + 模板）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        filename = request.query_params.get('filename', '')

        if not brand or not filename:
            return Response({'error': 'Please specify brand and filename'}, status=400)

        # 安全检查，防止路径遍历
        if '..' in filename or '/' in filename or '\\' in filename:
            return Response({'error': 'Invalid filename'}, status=400)

        brand_dir = settings.SCREENSHOTS_ROOT / brand
        json_path = brand_dir / 'data' / filename
        template_path = brand_dir / 'template.html'

        if not json_path.exists():
            return Response({'error': 'Data file not found'}, status=404)
        if not template_path.exists():
            return Response({'error': 'Template not found'}, status=404)

        try:
            json_content = json_path.read_text(encoding='utf-8')
            template_content = template_path.read_text(encoding='utf-8')

            # 在模板的 jsonData script 标签中注入数据
            content = template_content.replace(
                '<script id="jsonData" type="application/json"></script>',
                f'<script id="jsonData" type="application/json">{json_content}</script>'
            )

            return Response({'content': content})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
