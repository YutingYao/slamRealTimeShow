import time
import traceback
import multiprocessing

from PIL import Image
import os
import math

from django.utils.autoreload import logger

from ShareCloudServer.settings import global_process_pool

import logging

logger = logging.getLogger(__name__)
logger = logging.getLogger('django')


# logger.error("错误")
# logger.info("警告")
class Map():
    """
    Simple Map object
    tiles can be generated by passing Map to MapGenerator
    =====================================
    1 : Get original map dimension
    - dimensions

    2 : Check if original map dimension is
    Wider than long or the reverse (ratioPriority)
    - ratioPriority

    3 : Get Smallest map dimension into a tiles
    by reduce the bigger side (ratioPriority)
    to get both side inside the tile size
    - smallestDimensions
    - _calculateDimensions

    4 : Calcul number zoom from smallest map to biggest
    with zoomFactor without exceed limit of original map
    get the list of all dimensions Map calculated
    - zMapDimensions
    """

    def __init__(self, src, nb_zoom=None, tileSize=None, sizeFactor=None):
        print("src", src)
        self.image = Image.open(src)
        self.path = src
        self.ext = self.image.filename.split('.')[-1]
        self.sizeFactor = sizeFactor if sizeFactor else 2
        self.tileSize = tileSize if tileSize else 256
        self.hookGen = None
        self.progress = 0

    @property
    def ratio(self):
        if (self.image.width > self.image.height):
            return self.image.width / self.image.height
        return self.image.height / self.image.width

    @property
    def ratioPriority(self):
        if (self.image.width > self.image.height):
            return 0
        return 1

    @property
    def nb_zoom(self):
        # dim, c = self.tileSize, 0
        # while dim * self.sizeFactor < self.image.width:
        #     dim = dim * self.sizeFactor
        #     c += 1
        # return c + 1
        c_zoom = 0
        if self.ratioPriority == 0:
            c_zoom = round(math.log(self.image.width / self.tileSize, 2))
        elif self.ratioPriority == 1:
            c_zoom = round(math.log(self.image.height / self.tileSize, 2))

        return c_zoom + 1

    @property
    def dimensions(self):
        return (math.ceil(self.image.width), math.ceil(self.image.height))

    @property
    def smallestDimensions(self):
        return self._calculateDimensions(self.tileSize)

    # TODO: 计算不准确需要重写
    @property
    def numberTilesTotal(self):
        """瓦片总数"""
        nbTiles = 0
        for zMap in self.zMapDimensions:
            nbTiles += self.calculMapTilesNumber(zMap)

        return nbTiles

    @property
    def zMapDimensions(self):
        smallestDimensions = self.smallestDimensions[self.ratioPriority]
        zDimensions = [self.smallestDimensions]
        for i in range(1, self.nb_zoom):
            zDimensions.append(self._calculateDimensions(smallestDimensions * pow(self.sizeFactor, i)))
        # zDimensions.append(self.dimensions)
        return zDimensions

    def calculNumberTiles(self, dimensions, x_or_y):
        x_or_y = (x_or_y == 'y')
        return math.ceil(dimensions[x_or_y] / self.tileSize)

    def calculMapTilesNumber(self, dimensions):
        nbTiles0 = math.ceil(dimensions[0] / self.tileSize)
        nbTiles1 = math.ceil(dimensions[1] / self.tileSize)
        return nbTiles0 * nbTiles1

    def _calculateDimensions(self, newDimension):
        dimensions = [0, 0]
        dimensions[self.ratioPriority] = math.ceil(newDimension)
        dimensions[1 - self.ratioPriority] = math.ceil(self._calculDimFromProp(newDimension))
        return tuple(dimensions)

    def _calculDimFromProp(self, dimension):
        return dimension / self.ratio


class MapGenerator():
    """
    Generator object
    Use map object to generate all tiles
    organised in path /z/x/y.imageExtention
    =====================================
    """

    def __init__(self, map, genFolder='genZXY'):
        self.map = map
        self.genFolder = os.path.dirname(os.path.abspath(map.path))  # TODO: 瓦片存储的路径
        # self.genFolder = 'E:/服务器web3d/ShareCloudServer/libs'

    # it's a generator for returning
    # stream of generation progress
    def generateMapTiles(self):
        progress = 0
        self.makeFolderGen(self.genFolder)

        return (self.genTilesTreeZ(self._genZ),
                self.genTilesTreeZX(self._genZ, self._genX),
                self.genTilesTreeZXY(self._genZ, self._genX, self._genY))

        # for tile in self.genTilesTreeZX(self._genZ, self._genX):
        #     # pass
        #     tile[0](tile)
        #     # progress += 1
        #     yield progress
        # for tile in self.genTilesTreeZXY(self._genZ, self._genX, self._genY):
        #     tile[0](tile)
        #     progress += 1
        #     # pass
        #     yield progress

    def genTilesTreeZ(self, actionZ=None):
        for z, zMap in enumerate(self.map.zMapDimensions):
            yield [actionZ, z, self.genFolder, self.map]  # TODO: 生成层并得到层的缩略图 map

    def genTilesTreeZX(self, actionZ=None, actionX=None):
        for z, zMap in enumerate(self.map.zMapDimensions):

            # yield [actionZ, z, self.genFolder, self.map]  # TODO: 生成层并得到层的缩略图 map
            for x in range(0, self.map.calculNumberTiles(self.map.zMapDimensions[z], 'x')):
                yield [actionX, z, x, self.genFolder]  # TODO: 生成每个层级下的子文件夹  x 表示列数
                # for y in range(0, self.map.calculNumberTiles(self.map.zMapDimensions[z], 'y')):

    def genTilesTreeZXY(self, actionZ=None, actionX=None, actionY=None):
        for z, zMap in enumerate(self.map.zMapDimensions):
            posX, posY = 0, 0
            # yield [actionZ, z]  # TODO: 生成层并得到层的缩略图 map
            for x in range(0, self.map.calculNumberTiles(self.map.zMapDimensions[z], 'x')):
                posY = 0
                # yield [actionX, z, x]  # TODO: 生成每个层级下的子文件夹  x 表示列数
                for y in range(0, self.map.calculNumberTiles(self.map.zMapDimensions[z], 'y')):
                    yield [actionY, z, x, y, posX, posY, self.map.tileSize, self.genFolder, self.map.ratioPriority,
                           self.map.ext]  # TODO: 生成瓦片图  y 表示行数
                    posY += self.map.tileSize
                posX += self.map.tileSize

    @staticmethod
    def makeFolderGen(genFolder, path=''):
        folder = os.path.join(genFolder, path)
        if not os.path.isdir(folder):
            os.mkdir(folder)

    @staticmethod
    def _genZ(tile):
        """ genFolder,map
        When we arrive to new zoom, we create new z folder
        and save in z folder , the resized image of map
        """
        map = tile[3]
        MapGenerator.makeFolderGen(tile[2], str(tile[1]))  # 创建文件夹

        prior = map.ratioPriority
        dim1 = map.zMapDimensions[tile[1]][prior]
        dim2 = map.zMapDimensions[tile[1]][prior - 1]
        MapGenerator.makeFolderGen(tile[2], str(tile[1]))  # 创建文件夹
        croped = map.image.resize((dim1, dim2), Image.ANTIALIAS)
        croped.save(os.path.join(tile[2], str(tile[1]), 'map' + "." + map.ext))

    @staticmethod
    def _genX(tile):
        """
        When we arrive to new x column, we create new z/x/ folder
        创建 层下面的的 列文件夹
        """
        genFolder = tile[3]
        MapGenerator.makeFolderGen(genFolder, os.path.join(str(tile[1]), str(tile[2])))

    @staticmethod
    def _genY(tile):
        """
        For each Y row, we create a tile croped
        from current map of current zoom
        创建切割得到瓦片图  z, x, y,posX, posY,tileSize,genFolder,ratioPriority(prior = self.map.ratioPriority)、
        """
        t = tile
        # print('pathMap', t )

        pathMap = os.path.join(t[7], str(t[1]), "map." + t[9])
        # print('pathMap',pathMap)
        path_zxy = os.path.join(str(t[1]), str(t[2]), str(t[3]))
        pathImage = os.path.join(t[7], path_zxy + "." + t[9])
        cropZone = (t[4], t[5], t[6] + t[4], t[6] + t[5])  # 得到区域盒子

        prior = t[8]
        # dim1 = self.map.zMapDimensions[tile[1]][prior]
        # dim2 = self.map.zMapDimensions[tile[1]][prior - 1]
        MapGenerator.makeFolderGen(t[7],str(tile[1]))  # 创建文件夹
        # tileMap = self.map.image.resize((dim1, dim2), Image.ANTIALIAS)
        tileMap = Image.open(pathMap)
        tileCroped = tileMap.crop(cropZone)
        # print(pathImage)
        # TODO:判断文件夹是否存在不存在创建
        tileCroped.save(pathImage)
        tileMap.close()


def generate_map_tiles_thread(src):
    """
    传入绝对路径在,在绝对路径
    :param src:
    :return:
    """

    # global_process_pool.lock.acquire()  # TODO: 获取锁
    try:
        mapTile = Map(
            src,
            # "C:/Users/Administrator/Downloads/地图.png",
            tileSize=256,
            sizeFactor=2)
        start = time.time()
        generator = MapGenerator(mapTile)  # , genFolder=os.path.dirname(os.path.abspath("E:/模型/长信宫灯/DENGZHAO2.png"))
        # generator.generateMapTiles()

        tile01, tile02, tile03 = generator.generateMapTiles()

        pool01 = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        for tile in tile01:
            pool01.apply_async(tile[0], (tile,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
            # tile[0](tile)
        print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
        pool01.close()
        pool01.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
        end = time.time()

        print(end - start)

        pool02 = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        for tile in tile02:
            pool02.apply_async(tile[0], (tile,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
            # tile[0](tile)
        print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
        pool02.close()
        pool02.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
        end = time.time()

        print(end - start)

        pool03 = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        for tile in tile03:
            pool03.apply_async(tile[0], (tile,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
            # tile[0](tile)
        print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
        pool03.close()
        pool03.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
        # for progress in generator.generateMapTiles():
        #     print(progress, mapTile.numberTilesTotal)
        # pass
        end = time.time()

        print(end - start)

        # global_process_pool.lock.release()
    except Exception as e:
        trace_log = traceback.format_exc()
        logger.error(repr(e), '异步任务执行失败:\n %s' % trace_log)
        # global_process_pool.lock.release()  # TODO: 释放锁


if __name__ == '__main__':
    generate_map_tiles_thread( r"C:\Users\Administrator\Pictures\恐龙.jpg")
    print('aa')
    # mapTile = Map(
    #     # "E:/模型/长信宫灯/DENGZHAO2.png",
    #     r"C:\Users\Administrator\Pictures\恐龙.jpg",
    #     tileSize=256,
    #     sizeFactor=2)
    # start = time.time()
    # generator = MapGenerator(mapTile)  # , genFolder=os.path.dirname(os.path.abspath("E:/模型/长信宫灯/DENGZHAO2.png"))
    # # generator.generateMapTiles()
    #
    # tile01, tile02, tile03 = generator.generateMapTiles()
    #
    # pool01 = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    #
    # for tile in tile01:
    #     pool01.apply_async(tile[0], (tile,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    #     # tile[0](tile)
    # print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    # pool01.close()
    # pool01.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    # end = time.time()
    #
    # print(end - start)
    #
    # pool02 = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    #
    # for tile in tile02:
    #     pool02.apply_async(tile[0], (tile,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    #     # tile[0](tile)
    # print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    # pool02.close()
    # pool02.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    # end = time.time()
    #
    # print(end - start)
    #
    # pool03 = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    # for tile in tile03:
    #     pool03.apply_async(tile[0], (tile,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    #     # tile[0](tile)
    # print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    # pool03.close()
    # pool03.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    # # for progress in generator.generateMapTiles():
    # #     print(progress, mapTile.numberTilesTotal)
    # # pass
    # end = time.time()
    #
    # print(end - start)