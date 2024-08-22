import os
import platform
from tabulate import tabulate

from tools import resize
from tools import delete_black
from tools import contrast_up
from tools import luminance_up
from tools import road_center
from tools import randomly_select
from tools.multi2label import main as multi2label
from tools.single2lable import main as single2label


def f0():
    exit()


def f1():
    print("\n[图像处理工具箱] -> [调整图像大小]\n")
    header = ["参数", "默认值", "示例"]
    data = [
        ["输入文件夹路径", "无", "C:\\path\\to\\folder"],
        ["输出文件夹路径", "无", "C:\\path\\to\\folder"],
        ["图像类型", "tif", "tif|jpg|png"],
        ["调整后的图像高度", "512", "512"],
        ["调整后的图像宽度", "512", "512"]
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))
    input_folder = input("输入文件夹路径: ")
    output_folder = input("输出文件夹路径: ")
    image_type = input("图像类型: ")
    height = input("调整后的图像高度: ")
    width = input("调整后的图像宽度: ")
    image_type = image_type if image_type != "" else "tif"
    height = int(height) if height != "" else 512
    width = int(width) if width != "" else 512
    print("运行中...")
    resize.resize(input_folder, output_folder, image_type, height, width)
    print("完成！")


def f2():
    print("\n[图像处理工具箱] -> [SAR+光学+矢量数据制作标签]\n")
    header = ["参数", "默认值", "示例"]
    data = [
        ["矢量数据路径", "无", "C:\\path\\to\\file.shp"],
        ["SAR影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["光学影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["输出文件夹路径", "无", "C:\\path\\to\\folder"],
        ["数据集图像大小", "512", "512"],
        ["数据集图像步幅比率", "0.5", "0.5"],
        ["是否统一输入数据坐标系", "False", "False"],
        ["是否将16位遥感图像压缩至8位", "False", "False"]
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))
    shapefile_path = input("矢量数据路径: ")
    sar_path = input("SAR影像文件夹路径: ")
    optics_path = input("光学影像文件夹路径: ")
    output_path = input("输出文件夹路径: ")
    block_size = input("数据集图像大小: ")
    stride = input("数据集图像步幅比率: ")
    UCS = input("是否统一输入数据坐标系: ")
    tif2RGB = input("是否将16位遥感图像压缩至8位: ")
    block_size = int(block_size) if block_size != "" else 512
    stride = float(stride) if stride != "" else 0.5
    UCS = bool(UCS) if UCS != "" else False
    tif2RGB = bool(tif2RGB) if tif2RGB != "" else False
    print("运行中...")
    multi2label.main(shapefile_path, sar_path, optics_path, output_path, block_size, stride, UCS, tif2RGB)
    print("完成！")


def f3():
    print("\n[图像处理工具箱] -> SAR/光学+矢量数据制作标签\n")
    header = ["参数", "默认值", "示例"]
    data = [
        ["矢量数据路径", "无", "C:\\path\\to\\file.shp"],
        ["SAR/光学影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["输出文件夹路径", "无", "C:\\path\\to\\folder"],
        ["数据集图像大小", "768", "768"],
        ["数据集图像步幅比率", "0.5", "0.5"],
        ["是否将16位遥感图像压缩至8位", "False", "False"]
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))
    shapefile_path = input("矢量数据路径: ")
    image_path = input("SAR/光学影像文件夹路径: ")
    output_path = input("输出文件夹路径: ")
    block_size = input("数据集图像大小: ")
    stride = input("数据集图像步幅比率: ")
    tif2RGB = input("是否将16位遥感图像压缩至8位: ")

    block_size = int(block_size) if block_size != "" else 768
    stride = float(stride) if stride != "" else 0.5
    tif2RGB = bool(tif2RGB) if tif2RGB != "" else False

    print("运行中...")
    single2label.main(shapefile_path, image_path, output_path, block_size, stride, tif2RGB)
    print("完成！")


def f4():
    print("\n[图像处理工具箱] -> [删除遥感数据集中黑色像素过多的图像]\n")
    header = ["参数", "默认值", "示例"]
    data = [
        ["SAR影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["光学影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["标签文件夹路径", "无", "C:\\path\\to\\folder"],
        ["阈值", "0.05", "0.05"]
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))
    sar_path = input("SAR影像文件夹路径: ")
    optics_path = input("光学影像文件夹路径: ")
    label_path = input("标签文件夹路径: ")
    threshold = input("阈值: ")

    threshold = int(threshold) if threshold != "" else 0.05

    print("运行中...")
    delete_black.main(sar_path, optics_path, label_path, threshold)
    print("完成！")


def f5():
    print("\n[图像处理工具箱] -> [增强图像对比度]\n")
    header = ["参数", "默认值", "示例"]
    data = [
        ["原始图像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["增强后图像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["对比度增强因子", "2", "2"]
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))
    original_path = input("原始图像文件夹路径: ")
    enhanced_path = input("增强后图像文件夹路径: ")
    contrast_factor = input("对比度增强因子: ")

    contrast_factor = int(contrast_factor) if contrast_factor != "" else 0.05

    print("运行中...")
    contrast_up.main(original_path, enhanced_path, contrast_factor)
    print("完成！")


def f6():
    print("\n[图像处理工具箱] -> [增强图像亮度]\n")
    header = ["参数", "默认值", "示例"]
    data = [
        ["原始图像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["增强后图像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["亮度增加倍数", "2", "2"]
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))
    original_path = input("原始图像文件夹路径: ")
    enhanced_path = input("增强后图像文件夹路径: ")
    brightness_factor = input("亮度增加倍数: ")

    brightness_factor = int(brightness_factor) if brightness_factor != "" else 2

    print("运行中...")
    luminance_up.main(original_path, enhanced_path, brightness_factor)
    print("完成！")


def f7():
    print("\n[图像处理工具箱] -> [提取道路骨架]\n")
    header = ["参数", "默认值", "示例"]
    data = [
        ["输入文件夹路径", "无", "C:\\path\\to\\folder"],
        ["输出文件夹路径", "无", "C:\\path\\to\\folder"],
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))
    input_path = input("输入文件夹路径: ")
    output_path = input("输出文件夹路径: ")

    print("运行中...")
    road_center.main(input_path, output_path)
    print("完成！")


def f8():
    print("\n[图像处理工具箱] -> [随机抽取测试集]\n")
    header = ["参数", "默认值", "示例"]
    data = [
        ["SAR影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["光学影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["标签文件夹路径", "无", "C:\\path\\to\\folder"],
        ["目标SAR影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["目标光学影像文件夹路径", "无", "C:\\path\\to\\folder"],
        ["目标标签文件夹路径", "无", "C:\\path\\to\\folder"],
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))
    sar_path = input("SAR影像文件夹路径: ")
    optics_path = input("光学影像文件夹路径: ")
    label_path = input("标签文件夹路径: ")
    destination_sar_path = input("目标SAR影像文件夹路径: ")
    destination_optics_path = input("目标光学影像文件夹路径: ")
    destination_label_path = input("目标标签文件夹路径: ")

    print("运行中...")
    randomly_select.main(sar_path, optics_path, label_path, destination_sar_path, destination_optics_path, destination_label_path)
    print("完成！")


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def main():
    print("\n[图像处理工具箱]\n")
    header = ["序号", "名称"]
    data = [
        [0, "退出"],
        [1, "调整图像大小"],
        [2, "SAR+光学+矢量数据制作标签"],
        [3, "SAR/光学+矢量数据制作标签"],
        [4, "删除遥感数据集中黑色像素过多的图像"],
        [5, "增强图像对比度"],
        [6, "增加图像亮度"],
        [7, "提取道路骨架"],
        [8, "随机抽取测试集"],
    ]
    print(tabulate(data, headers=header, tablefmt="rst"))

    choice = int(input("请输入操作序号："))
    if choice == 0:
        f0()
    elif choice == 1:
        f1()
    elif choice == 2:
        f2()
    elif choice == 3:
        f3()
    elif choice == 4:
        f4()
    elif choice == 5:
        f5()
    elif choice == 6:
        f6()
    elif choice == 7:
        f7()
    elif choice == 8:
        f8()


    # clear_screen()

if __name__ == '__main__':
    while True:
        main()
