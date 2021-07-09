# 1、 apps.py 添加初始化功能
if os.path.exists(CONFIG_FILE.TILE_PATH):
    shutil.rmtree(CONFIG_FILE.TILE_PATH)  # 删除目录，包括目录下的所有文件
os.mkdir(CONFIG_FILE.TILE_PATH)

# 2、 瓦片切割位置更改
pts_out_src = CONFIG_FILE.TILE_PATH + only_file_name + "conver"  # TODO: 修改单独文件夹存放瓦片数据

# 3、添加点云修改
if current_point_cloud['id'] < 2:
    if os.path.exists(CONFIG_FILE.TILE_PATH):
        project_dir = os.listdir(CONFIG_FILE.TILE_PATH)
        if len(project_dir) > 2:
            shutil.rmtree(CONFIG_FILE.TILE_PATH)  # 删除目录，包括目录下的所有文件
            os.mkdir(CONFIG_FILE.TILE_PATH)


# nginx 文件配置
# 3.1、/GOSLAMtemp/ 由 '/GOSLAM/Downloads/GOSLAM/' 改为
# 	 '/GOSLAM/Downloads/TILE'

