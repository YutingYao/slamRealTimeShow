from django.db import models
from django.utils import timezone


# Create your models here.
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateField(verbose_name='发布日期')
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_books'  # 指明数据库表名
        verbose_name = '图书'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.btitle



# project info
class Project(models.Model):
    """
    save each project info
    """
    id = models.AutoField(verbose_name=u"项目编号", primary_key=True)
    project_name = models.CharField(default='项目', max_length=32, null=True, blank=True, verbose_name=u"项目名称2")
    tile_name = models.CharField(default='tile', max_length=32, null=True, blank=True, verbose_name=u"点云瓦片名称")
    active = models.BooleanField(default=True, verbose_name="是否激活", help_text="是否激活",)
    status = models.CharField(default='notStart', max_length=32, verbose_name="扫描状态")
    add_time = models.DateTimeField(default=timezone.now, verbose_name=u"添加时间")
    # point_cloud_list = models.ForeignKey(PointCloudChunk, related_name='point_cloud', on_delete=models.SET_NULL, null=True, blank=True,
    #                              verbose_name=u"帧点云")

    class Meta:
        verbose_name = "扫描项目"
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.name


# get point cloud by project info
# class get_project_data(models.Model):
#     """
#     save each project info
#     """
#     id = models.AutoField(verbose_name=u"项目编号", primary_key=True)
#     name = models.CharField(default='项目', max_length=32, null=True, blank=True, verbose_name=u"项目名称2")
#     active = models.BooleanField(default=True, verbose_name="是否激活", help_text="是否激活",)
#     add_time = models.DateTimeField(default=timezone.now, verbose_name=u"添加时间")
#     # point_cloud_list = models.ForeignKey(PointCloudChunk, related_name='point_cloud', on_delete=models.SET_NULL, null=True, blank=True,
#     #                              verbose_name=u"帧点云")
#
#     class Meta:
#         verbose_name = "扫描项目"
#         verbose_name_plural = verbose_name
#
#         def __str__(self):
#             return self.name


# 帧点云数据
class PointCloudChunk(models.Model):
    """
    存储每一帧点云数据
    """
    # table_name = models.CharField(max_length=35, null=True, blank=True, verbose_name=u"帧点云数据表名")
    # models.IntegerField(default=0, verbose_name=u"获取OSS下载连接的次数统计")
    cloud_id = models.IntegerField(default=0, verbose_name=u"帧点云编号")
    cloud_name = models.CharField(max_length=25, null=True, blank=True, verbose_name=u"帧点云名称")
    cloud_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"帧点云url")
    cloud_project = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"帧点云所属用户")
    # project_id = models.ForeignKey('Project', related_name="project_id", on_delete=models.SET_NULL, null=True,
    #                                  blank=True,
    #                                  verbose_name=u"所属项目")
    project_id = models.IntegerField(default=0, verbose_name=u"项目id")

    class Meta:
        verbose_name = u"帧点云"
        verbose_name_plural = verbose_name

    # 重载__str__方法使后台不再直接显示object
    def __str__(self):
        return self.cloud_name





# 点云轨迹数据
class Track(models.Model):
    """
    存储每一帧点云数据
    """
    # table_name = models.CharField(max_length=35, null=True, blank=True, verbose_name=u"帧点云数据表名")
    cloud_name = models.CharField(max_length=25, null=True, blank=True, verbose_name=u"轨迹属于点云")
    cloud_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"轨迹数据")
    cloud_project = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"轨迹属于项目")

    class Meta:
        verbose_name = u"点云轨迹"
        verbose_name_plural = verbose_name

    # 重载__str__方法使后台不再直接显示object
    def __str__(self):
        return self.cloud_name


# 点云轨迹回环点索引
class CirclePoint(models.Model):
    """
    存储每一帧点云数据
    """
    # table_name = models.CharField(max_length=35, null=True, blank=True, verbose_name=u"帧点云数据表名")
    circle_point_id = models.AutoField(verbose_name=u"回环点id", primary_key=True)
    # circle_point_start = models.IntegerField(default=0, verbose_name=u"开始回环点")
    # circle_point_end = models.IntegerField(default=0, verbose_name=u"结束回环点")
    circle_point_start = models.IntegerField(default=0, null=True, blank=True, verbose_name=u"开始回环点")
    circle_point_end = models.IntegerField(default=0, null=True, blank=True, verbose_name=u"结束回环点")

    # cloud_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"轨迹数据")
    # cloud_project = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"轨迹属于项目")

    class Meta:
        db_table = 'tb_circle_point'
        verbose_name = u"回环点"
        verbose_name_plural = verbose_name

    # 重载__str__方法使后台不再直接显示object
    def __str__(self):
        return self.circle_point_id
