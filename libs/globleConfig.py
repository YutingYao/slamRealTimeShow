from slamShow.settings import BASE_DIR, MEDIA_ROOT


class ConfigFile:
    __instance = None
    __flag = False
    SOURCE_POINT_CLOUD_PATH = '/GOSLAM/Downloads/GOSLAMtemp/'  # TODO: why ? - ubuntu- /GOSLAM/Downloads/GOSLAMtemp/
    TRACT_PATH = '/GOSLAM/Downloads/GOSLAMtemp/trackPoint.txt'  # TODO: track point file path
    TRACT_DATA = [{'id': 0, 'x': 0.0, 'y': -0.0, 'z': 0.0, 'er': 0.1589, 'ep': -0.2975, 'ey': 1.3474}]
    FILE_FORMAT = '_.pcd'
    PLATFORM_INFO = {
        'system': 'Linux',  # Windows
        'version': 10  # 10 ;linux 16 20 ...
    }
    CURRENT_PROJECT = {
        'project_name': '',  # 项目名称
        'point_cloud_id': 0,
        'project_id': 39,  # -1 表示没有保存瓦片文件夹和没有扫描项目
        'pre_project_id': None,
        'status': 'notStart',  # 扫描状态 notStart 没有扫描数据文件夹 pending 代表已经存在 扫描数据文件夹， stop 代表扫描完成
        'tile_path': '',  # 瓦片存放路径
        'tile_name': 'conver20210527105516',
        'point_cloud_path': SOURCE_POINT_CLOUD_PATH,  # 原始点云路径
        'track_path': '',  # 轨迹路径
    }
    SCAN_SET = {
        'outdoor': '1',  # 室外模式
        'indoor': '2',  # 室内模式
        'loopback_true': '3',  # 开启回环
        'loopback_false': '4',  # 关闭回环
        'optimize_true': '5',  # 室外模式
        'optimize_false': '6',  # 开启二次优化
        'noSample_true': '7',  # 保存不采样数据
        'noSample_false': '8',  # 不保存不采样数据
        'sample_true': '9',  # 保存采样数据
        'sample_false': '10'  # 不保存采样数据
    }
    # PotreeUbuntu20Potree
    POTREE_PATH = BASE_DIR + '/libs/PotreeUbuntu20Potree/PotreeConverter '
    SET_SCAN_PARAMETER = {

    }
    # 1、创建扫描文件夹，没有扫描，下次开机时，初始化为没有扫描文件夹
    # 2、后台确定扫描是调用start_scan接口，不调用就是没有开始扫描
    activeProject = ''

    scanStatus = 'notStart'  # scan status noStart pending end

    def __new__(cls, *args, **kwargs):
        print('new 执行了')

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not ConfigFile.__flag:
            print('init 执行了')
            ConfigFile.__flag = True


CONFIG_FILE = ConfigFile()
