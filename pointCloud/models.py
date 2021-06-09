from django.db import models
from django.utils import timezone


# 帧点云数据
class PointCloudChunk(models.Model):
    """
    存储每一帧点云数据
    """
    # table_name = models.CharField(max_length=35, null=True, blank=True, verbose_name=u"帧点云数据表名")
    # models.IntegerField(default=0, verbose_name=u"获取OSS下载连接的次数统计")
    # id = models.AutoField(verbose_name=u"帧点云id")
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
    circle_point_start = models.IntegerField(default=0, null=True, blank=True, verbose_name=u"开始回环点")
    circle_point_end = models.IntegerField(default=0, null=True, blank=True, verbose_name=u"结束回环点")

    class Meta:
        db_table = 'tb_circle_point'
        verbose_name = u"回环点"
        verbose_name_plural = verbose_name

    # 重载__str__方法使后台不再直接显示object
    def __str__(self):
        return self.circle_point_id
