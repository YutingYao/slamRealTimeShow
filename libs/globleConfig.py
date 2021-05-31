from slamShow.settings import BASE_DIR, MEDIA_ROOT

SOURCE_POINT_CLOUD_PATH = 'D:/slamPointCloudShow/GOSLAMtemp/'  # TODO: why ? - ubuntu- /GOSLAM/Downloads/GOSLAMtemp/
TRACT_PATH = 'D:/slamPointCloudShow/GOSLAMtemp/trackPoint.txt'  # TODO: track point file path
TRACT_DATA = None
PLATFORM_INFO = {
    'system': 'Windows',
    'version': 10  # 10 ;linux 16 20 ...
}
CURRENT_PROJECT = {
    'project_name': '',  # 项目名称
    'project_id': 0,  # -1 表示没有保存瓦片文件夹和没有扫描项目
    'point_cloud_id': 0,
    'pre_project_id': None,
    'status': 'notStart',  # 扫描状态 notStart 没有扫描数据文件夹 pending 代表已经存在 扫描数据文件夹， stop 代表扫描完成
    'tile_path': '',  # 瓦片存放路径
    'tile_name': 'conver20210525151322',
    'point_cloud_path': SOURCE_POINT_CLOUD_PATH,  # 原始点云路径
    'track_path': '',  # 轨迹路径
}
POTREE_PATH = BASE_DIR + '/potree/windowsE57PotreeConverter/PotreeConverter.exe '
SET_SCAN_PARAMETER = {

}
# 1、创建扫描文件夹，没有扫描，下次开机时，初始化为没有扫描文件夹
# 2、后台确定扫描是调用start_scan接口，不调用就是没有开始扫描
activeProject = ''

scanStatus = 'notStart'  # scan status noStart pending end
