from django.db import models


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
class CirclePoint2(models.Model):
    """
    存储每一帧点云数据
    """
    # table_name = models.CharField(max_length=35, null=True, blank=True, verbose_name=u"帧点云数据表名")
    circle_point_id = models.IntegerField(default=0, verbose_name=u"回环点id")
    # circle_point_start = models.IntegerField(default=0, verbose_name=u"开始回环点")
    # circle_point_end = models.IntegerField(default=0, verbose_name=u"结束回环点")
    circle_point_start = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"开始回环点")
    circle_point_end = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"结束回环点")

    # cloud_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"轨迹数据")
    # cloud_project = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"轨迹属于项目")

    class Meta:
        db_table = 'tb_circle_point2'
        verbose_name = u"回环点"
        verbose_name_plural = verbose_name

    # 重载__str__方法使后台不再直接显示object
    def __str__(self):
        return self.circle_point_id
