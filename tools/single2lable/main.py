import os
from . import ShpToTrain
from . import TifTrans
from .utensil import specifics, pretreatment


# class paths:
#     def __init__(self) -> None:
#         self.ShapefilePath = "../data/road6_12/road.shp"
#         self.ImagePath = ['../data/road6_12/road.tif']
#
#         self.OutputLabelPath = "../output/road6_12/label"
#         self.OutputImagePath = "../output/road6_12/image"
#
#         self.stride = 0.5
#         self.tif2RGB = False
#         self.OutputImageRGBPath = "../output/road5_30/imageRGB"
#         self.block_size = 768


def read_first_line_to_list(input_file):
    with open(input_file, 'r') as f:
        first_line = f.readline().strip()  # 读取第一行并去除换行符和空白字符
        p = first_line.split(",")  # 拆分第一行内容为列表

    return p

def list_all_files(directory):
    file_paths = []

    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)

    return file_paths

def make_directories(base_path, folder_names):
    folder_paths = {}

    for folder in folder_names:
        # 创建完整的文件夹路径
        folder_path = os.path.join(base_path, folder)

        # 如果文件夹不存在，则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 将文件夹名和路径添加到字典中
        folder_paths[folder] = folder_path

    return folder_paths


def main(shapefile_path: str,
         image_path: str,
         output_path: str,

         block_size: int = 768,
         tif2RGB: bool = False,
         stride: float = 0.5):

    ###########################################Begin
    # 对于1.shp，list中的路径为sar3不行
    image_path = list_all_files(image_path)

    folders_paths = make_directories(output_path, ["image", "label", "rgb"])
    output_label_path = folders_paths["label"]
    output_image_path = folders_paths["image"]
    output_rgb_path = folders_paths["rgb"]
    ###########################################End
    shapefile, image, image_path = pretreatment.data_input(image_path, shapefile_path)
    specifics.getAttribute(shapefile)

    ###########################################Begin
    # 读取矢量数据的txt属性表
    # input_file = "./tmp/Attribute.txt"
    # 获取当前模块的目录
    current_directory = os.path.dirname(__file__)
    # 构造绝对路径
    input_file = os.path.join(current_directory, 'tmp', 'Attribute.txt')
    ###########################################End

    p = read_first_line_to_list(input_file)

    for i in range(len(image)):
        data = ShpToTrain.DataSet(image[i], image_path[i], shapefile,
                                  block_size, output_image_path,
                                  output_label_path, stride, field=p[0])
        data.getData()

    if tif2RGB:
        img_path = output_image_path
        files = os.listdir(img_path)
        num_png = len(files)
        for a in range(0, num_png):
            print(f"image转换为RGB  {a + 1}/{num_png}")
            TifTrans.compress(f"{output_image_path}/{a}.tiff",
                              f"{output_rgb_path}/{a}.tiff")