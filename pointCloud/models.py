from django.db import models


# 定义配置模型类HeroInfo
class ConfigInfo(models.Model):
    is_record = models.BooleanField(default=False, verbose_name='是否录制')

    class Meta:
        db_table = 'tb_config'
        verbose_name = '扫描配置'
        verbose_name_plural = verbose_name
