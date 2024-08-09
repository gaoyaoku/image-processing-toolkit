from shapely.geometry import Polygon
from osgeo import gdal
from osgeo import ogr


def get_image_transform(img):
    transform = (img.GetGeoTransform())
    rX = transform[1]  # 分辨率  （像元高度）
    rY = transform[5]
    lX = transform[0]  # 左上角点
    lY = transform[3]
    width = img.RasterXSize  # 列数
    height = img.RasterYSize  # 行数
    bX = lX + rX * width  # 右下角点
    bY = lY + rY * height
    return rX, rY, lX, lY, width, height, bX, bY


def merge_duplicate_lines(input_file, output_file):  # 合并相同项目
    lines_dict = {}
    # 读取输入文件并将行存储到字典中
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()  # 去除行末尾的换行符和空白字符
            if line in lines_dict:
                lines_dict[line] += 1
            else:
                lines_dict[line] = 1
    # 将合并后的内容写入输出文件
    with open(output_file, 'w') as f:
        for line, count in lines_dict.items():
            f.write(f"{line}\n")


def getAttribute(dataSource):
    layer = dataSource.GetLayer(0)
    output_txt_file = "./tmp/Attribute.txt"
    with open(output_txt_file, "w") as txt_file:
        # 写入属性列名
        layerDefinition = layer.GetLayerDefn()
        field_names = [layerDefinition.GetFieldDefn(i).GetName() for i in range(layerDefinition.GetFieldCount())]
        txt_file.write(",".join(field_names) + "\n")
        # 逐行写入属性值
        for feature in layer:
            attribute_values = [str(feature.GetField(field_name)) for field_name in field_names]
            txt_file.write(",".join(attribute_values) + "\n")
    # 7. 关闭数据源
    dataSource = None
    merge_duplicate_lines("./tmp/Attribute.txt", "./tmp/Attribute.txt")


def grouped_image(image_path):
    # 用于存储图像坐标的列表
    img_points = []
    # 打开每个图像并提取其坐标
    for i, image_path in enumerate(image_path):
        img = gdal.Open(image_path)
        rX, rY, lX, lY, width, height, bX, bY = get_image_transform(img)
        coordinates = Polygon([(lX, lY), (bX, lY), (bX, bY), (lX, bY)])
        img_points.append((i, coordinates, image_path[i]))  # 存储图像编号和坐标

    # 创建一个空列表来存储分组结果
    groups = []
    for i, polygon1, image_path1 in img_points:
        # 创建一个标志来指示是否与任何一个已分组的图像坐标相交
        intersects = False
        for group in groups:
            for j, polygon2, image_path2 in group:
                if polygon1.intersects(polygon2):
                    group.append((i, polygon1, image_path1))
                    intersects = True
                    break
        # 如果没有与任何已分组的图像坐标相交，创建一个新的分组
        if not intersects:
            groups.append([(i, polygon1, image_path1)])

    grouped_image_paths = [[image_path for _, _, image_path in group] for group in groups]
    return grouped_image_paths
