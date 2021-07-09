from django.apps import AppConfig
# from pointCloud.models import PointCloudChunk
import shutil
from slamShow.settings import MEDIA_ROOT
from libs.globleConfig import CONFIG_FILE
# from libs.WebSocket import th
from django.core.cache import cache


class PointcloudConfig(AppConfig):
    name = 'pointCloud'

    def initData(self):
        initList = {'CIRCLE_DATA': [], 'TRACT_DATA': [], 'point_cloud': [], 'stop': 'False'}
        cache.set_many(initList)
        if os.path.exists(CONFIG_FILE.TILE_PATH):
            shutil.rmtree(CONFIG_FILE.TILE_PATH)  # 删除目录，包括目录下的所有文件
        os.mkdir(CONFIG_FILE.TILE_PATH)
        # th()
        # Thread(target=th).start()
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
