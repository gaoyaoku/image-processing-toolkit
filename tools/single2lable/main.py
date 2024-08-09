import os
import ShpToTrain
import TifTrans
from utensil import specifics, pretreatment


class paths:
    def __init__(self) -> None:
        self.ShapefilePath = "../data/road6_12/road.shp"
        self.ImagePath = ['../data/road6_12/road.tif']

        self.OutputLabelPath = "../output/road6_12/label"
        self.OutputImagePath = "../output/road6_12/image"

        self.stride = 0.5
        self.tif2RGB = False
        self.OutputImageRGBPath = "../output/road5_30/imageRGB"
        self.block_size = 768


def read_first_line_to_list(input_file):
    with open(input_file, 'r') as f:
        first_line = f.readline().strip()  # 读取第一行并去除换行符和空白字符
        p = first_line.split(",")  # 拆分第一行内容为列表

    return p


if __name__ == "__main__":
    paths = paths()
    shapefile, image, image_path = pretreatment.data_input(paths.ImagePath, paths.ShapefilePath)
    specifics.getAttribute(shapefile)
    input_file = "./tmp/Attribute.txt"
    p = read_first_line_to_list(input_file)

    for i in range(len(image)):
        data = ShpToTrain.DataSet(image[i], image_path[i], shapefile,
                                  paths.block_size, paths.OutputImagePath,
                                  paths.OutputLabelPath, paths.stride, field=p[0])
        data.getData()

    if paths.tif2RGB:
        img_path = paths.OutputImagePath
        files = os.listdir(img_path)
        num_png = len(files)
        for a in range(0, num_png):
            print(f"image转换为RGB  {a + 1}/{num_png}")
            TifTrans.compress(f"{paths.OutputImagePath}/{a}.tiff",
                              f"{paths.OutputImageRGBPath}/{a}.tiff")