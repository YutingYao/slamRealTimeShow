from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from pointCloud.models import PointCloudChunk, ScanProject


# TODO:扫描数据 start
class ScanProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScanProject
        fields = "__all__"


class ScanProjectRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScanProject
        fields = ['id', 'corner_map', 'global_cloud_all', 'global_map', 'transformations',
                  'tile_item', 'is_active']
        # fields = "__all__"


class ScanProjectUpdateSerializer(serializers.HyperlinkedModelSerializer):
    # cloud_id = models.IntegerField(default=0, verbose_name=u"帧点云编号")
    # cloud_name = models.CharField(max_length=25, null=True, blank=True, verbose_name=u"帧点云名称")
    # cloud_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"帧点云url")
    # cloud_project = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"帧点云所属用户")
    # project_id = models.IntegerField(default=0, verbose_name=u"项目id")

    class Meta:
        model = ScanProject
        fields = "__all__"
        fields = ['id', 'corner_map', 'global_cloud_all', 'global_map', 'transformations',
                  'tile_item', 'is_active']

    # def update(self, instance, validated_data):
    #     '''
    #     重写 update  验证 用户是否为正常请求用户 或 管理员用户
    #     :param instance:
    #     :param validated_data:
    #     :return:
    #     '''
    #
    #     instance = super().update(instance, validated_data)
    #
    #     # TODO: 如果是否删除请求, 更新 user.scene_number
    #
    #     return instance
    #
    # def create(self, validated_data):
    #     # user = self.context["request"].user
    #
    #     # if user.scene_number >= user.upload_limit:
    #     #     # return JsonResponse(data={'detail': '创建项目数量已用完'}, status=200)
    #     #     raise serializers.ValidationError({'detail': '创建项目数量已用完'})
    #
    #     # validated_data["user"] = user
    #
    #     instance = super().create(validated_data)
    #     return instance

    # TODO: 对关联的 stations 做过滤
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['stations'] = [station for station in ret['stations'] if station["is_active"]]
    #     return ret


class ScanProjectListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScanProject
        # depth = 1
        # fields = "__all__"
        fields = ['id', 'corner_map', 'global_cloud_all', 'global_map', 'transformations',
                  'tile_item', 'is_active']


# TODO:扫描项目end

class PointCloudChunkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PointCloudChunk
        fields = "__all__"


class PointCloudChunkRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PointCloudChunk
        # fields = "__all__"
        # depth = 1

        fields = ['id', 'cloud_id', 'cloud_name', 'cloud_url', 'cloud_project', 'project_id']

        # fields = "__all__"

    # TODO: 对关联的 stations 做过滤
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # ret['stations'] = [station for station in ret['stations'] if station["is_active"]]
        return ret


class PointCloudChunkUpdateSerializer(serializers.HyperlinkedModelSerializer):
    # cloud_id = models.IntegerField(default=0, verbose_name=u"帧点云编号")
    # cloud_name = models.CharField(max_length=25, null=True, blank=True, verbose_name=u"帧点云名称")
    # cloud_url = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"帧点云url")
    # cloud_project = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"帧点云所属用户")
    # project_id = models.IntegerField(default=0, verbose_name=u"项目id")

    class Meta:
        model = PointCloudChunk
        # fields = "__all__"
        # depth = 1
        fields = ['id', 'cloud_id', 'cloud_name', 'cloud_url', 'cloud_project', 'project_id']

        # fields = "__all__"

    # def update(self, instance, validated_data):
    #     '''
    #     重写 update  验证 用户是否为正常请求用户 或 管理员用户
    #     :param instance:
    #     :param validated_data:
    #     :return:
    #     '''
    #
    #     instance = super().update(instance, validated_data)
    #
    #     # TODO: 如果是否删除请求, 更新 user.scene_number
    #
    #     return instance
    #
    # def create(self, validated_data):
    #     # user = self.context["request"].user
    #
    #     # if user.scene_number >= user.upload_limit:
    #     #     # return JsonResponse(data={'detail': '创建项目数量已用完'}, status=200)
    #     #     raise serializers.ValidationError({'detail': '创建项目数量已用完'})
    #
    #     # validated_data["user"] = user
    #
    #     instance = super().create(validated_data)
    #     return instance

    # TODO: 对关联的 stations 做过滤
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['stations'] = [station for station in ret['stations'] if station["is_active"]]
    #     return ret


class PointCloudChunkListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PointCloudChunk
        # depth = 1
        # fields = ['url', 'id', 'name', 'user', 'tags', 'category', 'cover_image', 'cover_image_thumb', 'project_time',
        #           'project_author',
        #           'scan_station_number', 'address',
        #           'is_active','type_show', 'show_way', 'scene_show', 'scene_permission', 'download_permission',
        #           'longitude', 'latitude', 'all_original_file', 'all_results_file', 'desc', 'results_described',
        #           'scan_station_number', 'project_start_time', 'project_end_time', "add_time", ]
        fields = ['id', 'cloud_id', 'cloud_name', 'cloud_url', 'cloud_project', 'project_id']
