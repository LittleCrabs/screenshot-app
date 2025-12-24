from pathlib import Path
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ModeListView(APIView):
    """获取模式列表（一级目录）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        screenshots_dir = settings.SCREENSHOTS_ROOT
        modes = []

        if screenshots_dir.exists():
            for item in sorted(screenshots_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    modes.append(item.name)

        return Response({'modes': modes})


class BrandListView(APIView):
    """获取品牌列表（二级目录）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mode = request.query_params.get('mode', '')
        if not mode:
            return Response({'error': 'Please specify mode'}, status=400)

        mode_dir = settings.SCREENSHOTS_ROOT / mode
        brands = []

        if mode_dir.exists():
            for item in sorted(mode_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.') and item.name != 'data':
                    brands.append(item.name)

        return Response({'brands': brands})


class ModelListView(APIView):
    """获取型号列表（三级目录，仅 Error Code 模式）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mode = request.query_params.get('mode', '')
        brand = request.query_params.get('brand', '')

        if not mode or not brand:
            return Response({'error': 'Please specify mode and brand'}, status=400)

        brand_dir = settings.SCREENSHOTS_ROOT / mode / brand
        models = []

        if brand_dir.exists():
            for item in sorted(brand_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.') and item.name != 'data':
                    models.append(item.name)

        return Response({'models': models})


class ImageSearchView(APIView):
    """搜索图片（Error Code 模式）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mode = request.query_params.get('mode', 'Error Code')
        brand = request.query_params.get('brand', '')
        model = request.query_params.get('model', '')
        keyword = request.query_params.get('keyword', '')

        if not brand or not model:
            return Response({'error': 'Please specify brand and model'}, status=400)
        if not keyword:
            return Response({'error': 'Please enter search keyword'}, status=400)

        target_dir = settings.SCREENSHOTS_ROOT / mode / brand / model

        images = []
        if target_dir.exists():
            images = self._search_images(target_dir, keyword)

        return Response({'images': images})

    def _search_images(self, directory, keyword):
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


class ComponentListView(APIView):
    """获取 Component IO Check 的 JSON 文件列表"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        if not brand:
            return Response({'error': 'Please specify brand'}, status=400)

        data_dir = settings.SCREENSHOTS_ROOT / 'Component IO Check' / brand
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


class ComponentContentView(APIView):
    """获取 Component IO Check 的 JSON 数据"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        filename = request.query_params.get('filename', '')

        if not brand or not filename:
            return Response({'error': 'Please specify brand and filename'}, status=400)

        if '..' in filename or '/' in filename or '\\' in filename:
            return Response({'error': 'Invalid filename'}, status=400)

        json_path = settings.SCREENSHOTS_ROOT / 'Component IO Check' / brand / filename

        if not json_path.exists():
            return Response({'error': 'Data file not found'}, status=404)

        try:
            import json
            json_content = json_path.read_text(encoding='utf-8')
            data = json.loads(json_content)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class VideoListView(APIView):
    """获取 Video Tutorial 的视频列表"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand = request.query_params.get('brand', '')
        keyword = request.query_params.get('keyword', '').strip().lower()

        if not brand:
            return Response({'error': 'Please specify brand'}, status=400)

        video_dir = settings.SCREENSHOTS_ROOT / 'Video Tutorial' / brand
        videos = []
        video_extensions = {'.mp4', '.webm', '.mov', '.avi', '.mkv'}

        if video_dir.exists():
            for item in sorted(video_dir.glob('*')):
                if item.is_file() and item.suffix.lower() in video_extensions:
                    # 如果有关键词，过滤文件名
                    if keyword and keyword not in item.stem.lower():
                        continue
                    rel_path = item.relative_to(settings.SCREENSHOTS_ROOT)
                    videos.append({
                        'name': item.stem,
                        'filename': item.name,
                        'path': f'/screenshots/{rel_path.as_posix()}',
                    })

        return Response({'videos': videos})
