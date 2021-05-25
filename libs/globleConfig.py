CURRENT_PROJECT = {
    'name': '',
    'project_id': -1,
    'pre_project_id': None,
    'status': 'notStart',
    'tile_path': '',
    'point_cloud_path': '',
    'track_path': '',

}
# 1、创建扫描文件夹，没有扫描，下次开机时，初始化为没有扫描文件夹
# 2、后台确定扫描是调用start_scan接口，不调用就是没有开始扫描
activeProject = ''

scanStatus = 'notStart'  # scan status noStart pending end
