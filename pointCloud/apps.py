from django.apps import AppConfig
from slamShow.settings import MEDIA_ROOT
from django.core.cache import cache


class PointcloudConfig(AppConfig):
    name = 'pointCloud'

    def initData(self):
        initList = {'CIRCLE_DATA': [], 'TRACT_DATA': [], 'point_cloud': [], 'stop': 'False'}
        cache.set_many(initList)
        # if os.path.exists(CONFIG_FILE.TILE_PATH):
        #     shutil.rmtree(CONFIG_FILE.TILE_PATH)  # 删除目录，包括目录下的所有文件
        # os.mkdir(CONFIG_FILE.TILE_PATH)
