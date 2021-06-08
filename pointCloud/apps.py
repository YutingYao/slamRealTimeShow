from django.apps import AppConfig
# from pointCloud.models import PointCloudChunk
from slamShow.settings import MEDIA_ROOT
from django.core.cache import cache

class PointcloudConfig(AppConfig):
    name = 'pointCloud'

    def initData(self):
        initList = {'CIRCLE_DATA': [], 'TRACT_DATA': [], 'point_cloud': [], 'stop': 'False'}
        cache.set_many(initList)
        # from pointCloud.models import PointCloudChunk
        # point_cloud = PointCloudChunk.objects.all().delete()
        # track_path = MEDIA_ROOT + "/track/trackPoint.txt"
        # circle_path = MEDIA_ROOT + "/track/circlePoint.txt"
        #
        # with open(track_path, 'r+', encoding='utf-8') as f:
        #     f.truncate()
        # with open(circle_path, 'r+', encoding='utf-8') as f:
        #     f.truncate()
        print('执行初始化操作')
