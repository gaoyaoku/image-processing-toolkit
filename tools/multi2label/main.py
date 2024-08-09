import os
from . import ShpToTrain
from . import TifTrans
from .utensil import specifics, pretreatment
from osgeo import gdal, ogr, osr


# class paths:
#     def __init__(self,
#                  ShapefilePath: str,
#                  SarPath: list[str],
#                  OpticsPath: list[str],
#
#                  OutputLabelPath: str,
#                  OutputSarPath: str,
#                  OutputOpticsPath: str,
#
#                  OutputImageRGBPath: str,
#                  block_size: int = 512,
#                  stride: int = 0.5,
#
#                  UCS: bool = False,
#                  tif2RGB: bool = False
#                  ):
#         """
#         参数输入
#         ShapefilePath : 矢量数据路径
#         SarPath : sar影像路径
#         OpticsPath : 光学影像路径
#         OutputLabelPath : 输出标签路径
#         OutputSarPath : 输出sar原图路径
#         OutputOpticsPath : 输出光学原图路径
#         block_size : 数据集图像大小
#         stride : 数据集图像步幅比率
#         UCS : 是否统一输入数据坐标系
#         tif2RGB : 是否将16位遥感图像压缩至8位
#         OutputImageRGBPath : 8位输出光学原图路径
#         """
#         self.ShapefilePath = ShapefilePath
#         self.SarPath = SarPath
#         self.OpticsPath = OpticsPath
#         self.OutputLabelPath = OutputLabelPath
#         self.OutputSarPath = OutputSarPath
#         self.OutputOpticsPath = OutputOpticsPath
#         self.block_size = block_size
#         self.stride = stride
#         self.UCS = UCS
#         self.tif2RGB = tif2RGB
#         self.OutputImageRGBPath = OutputImageRGBPath
#
#         # self.ShapefilePath = r"G:\data\shp\4\4.shp"
#         # self.SarPath = [r"P:\project_shp2label\data\road7_11\8位\sar1.tif",
#         #                 r"G:\data\8_6\sar2.tif",
#         #                 r"G:\data\8_6\sar3.tif",
#         #                 r"G:\data\8_6\sar4.tif"]
#         # self.OpticsPath = [r"G:\data\8_6\gf1_1.tif",
#         #                    r"G:\data\8_6\gf1_2.tif",
#         #                    r"G:\data\8_6\gf1_3.tif",
#         #                    r"G:\data\8_6\gf1_4.tif",
#         #                    r"G:\data\7_18\8\GF6_PMS_E116.tif"]
#         #
#         # self.OutputLabelPath = r"P:\project_shp2label\output\road8_2-4_1\label"
#         # self.OutputSarPath = r"P:\project_shp2label\output\road8_2-4_1\image_sar"
#         # self.OutputOpticsPath = r"P:\project_shp2label\output\road8_2-4_1\image_optics"
#         #
#         # self.block_size = 512
#         # self.stride = 0.5
#         #
#         # self.UCS = False
#         # self.tif2RGB = False
#         # self.OutputImageRGBPath = r"P:\project_shp2label\output\road8_2-4_1\imageRGB"
#

def read_first_line_to_list(input_file):
    """
    读取矢量属性表的字段值
    :param txt格式的矢量属性表
    :return 属性表的第一个字段值
    """
    with open(input_file, 'r') as f:
        first_line = f.readline().strip()  # 读取第一行并去除换行符和空白字符
        p = first_line.split(",")  # 拆分第一行内容为列表

    return p


def main(shapefile_path: str,
         sar_path: list[str],
         optics_path: list[str],

         output_label_path: str,
         output_sar_path: str,
         output_optics_path: str,

         output_rgb_path: str,
         block_size: int = 512,
         stride: int = 0.5,

         UCS: bool = False,
         tif2RGB: bool = False):
    """
    ShapefilePath : 矢量数据路径
    SarPath : sar影像路径
    OpticsPath : 光学影像路径
    OutputLabelPath : 输出标签路径
    OutputSarPath : 输出sar原图路径
    OutputOpticsPath : 输出光学原图路径
    block_size : 数据集图像大小
    stride : 数据集图像步幅比率
    UCS : 是否统一输入数据坐标系
    tif2RGB : 是否将16位遥感图像压缩至8位
    OutputImageRGBPath : 8位输出光学原图路径
    """
    # 数据预处理
    if UCS:
        sar_path, optics_path = pretreatment.coordinate_conversion(sar_path, optics_path)
        shapefile = pretreatment.coordinate_conversion_Vector(shapefile_path, sar_path)
    else:
        sar_path = sar_path
        optics_path = optics_path
        shapefile = ogr.Open(shapefile_path)
    sar, sar_points = pretreatment.img_input(sar_path, "sar")
    optics, optics_points = pretreatment.img_input(optics_path, "optics")

    specifics.getAttribute(shapefile)
    # 读取矢量数据的txt属性表
    # input_file = "./tmp/Attribute.txt"
    # 获取当前模块的目录
    current_directory = os.path.dirname(__file__)
    # 构造 data/config.json 文件的绝对路径
    input_file = os.path.join(current_directory, 'tmp', 'Attribute.txt')

    p = read_first_line_to_list(input_file)

    for i in range(len(sar)):
        for j in range(len(optics)):
            data = ShpToTrain.DataSet(sar[i], sar_points[i], shapefile,
                                      block_size, output_sar_path,
                                      output_label_path, optics[j], output_optics_path,
                                      stride, field=p[0])
            data.getData()

    if tif2RGB:
        img_path = output_optics_path
        files = os.listdir(img_path)
        num_png = len(files)
        for a in range(0, num_png):
            print(f"image转换为RGB  {a+1}/{num_png}")
            TifTrans.compress(f"{output_optics_path}/{a}.tiff",
                              f"{output_rgb_path}/{a}.tiff")
