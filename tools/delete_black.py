"""
用于删除遥感数据集中黑色像素过多，有意义信息较少的图像
"""

import os
from PIL import Image


def is_mostly_black(image_path, threshold=0.3):
    """
    检查图像是否大部分为黑色。
    :param image_path: 图像文件的路径。
    :param threshold: 黑色像素的阈值比例，默认值为0.3。
    :return: 如果黑色像素比例超过阈值，返回True；否则返回False。
    """
    with Image.open(image_path) as img:
        # 如果图像不是灰度模式，将其转换为灰度模式
        img = img.convert("L")
        pixels = img.getdata()

        # 在灰度模式下，黑色像素的值为0
        black_pixels = sum(1 for pixel in pixels if pixel == 0)
        total_pixels = len(pixels)

        # 计算黑色像素的比例
        black_percentage = black_pixels / total_pixels

        return black_percentage > threshold


def delete_black_images(folder_path, threshold=0.3):
    """
    删除指定文件夹中黑色像素超过一定比例的灰度图像。
    :param folder_path: 文件夹路径。
    :param threshold: 黑色像素的阈值比例，默认值为0.3。
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.tif'):
            file_path = os.path.join(folder_path, filename)
            if is_mostly_black(file_path, threshold):
                print(f"Deleting {file_path} (more than {threshold * 100}% black pixels)")
                os.remove(file_path)


def get_image_names(folder_path):
    """
    获取给定文件夹中所有图像的名称（不包括扩展名）。
    :param folder_path: 文件夹路径。
    :return: 图像名称的集合（不包括扩展名）。
    """
    return {os.path.splitext(filename)[0] for filename in os.listdir(folder_path)}


def delete_unmatched_images(source_folder, reference_folder):
    """
    删除源文件夹中名称不在参考文件夹中的图像。
    :param source_folder: 源文件夹路径，包含需要检查和删除的图像。
    :param reference_folder: 参考文件夹路径，包含参考的图像名称。
    """
    reference_names = get_image_names(reference_folder)

    for filename in os.listdir(source_folder):
        name, ext = os.path.splitext(filename)
        if name not in reference_names:
            file_path = os.path.join(source_folder, filename)
            print(f"Deleting {file_path} (name not found in reference folder)")
            os.remove(file_path)


def main(sar_path, optics_path, label_path, threshold=0.05):
    # 设置文件夹路径和阈值
    optics_folder_path = optics_path
    sar_folder_path = sar_path
    label_folder_path = label_path
    black_threshold = threshold
    # 先删除光学图像中黑色像素过多的图像
    delete_black_images(optics_folder_path, black_threshold)
    # 同时删除sar和标签中对应的图像
    delete_unmatched_images(sar_folder_path, optics_folder_path)
    # 删除SAR图像中黑色像素过多的图像
    delete_black_images(sar_folder_path, black_threshold)
    # 删除不匹配的图像
    delete_unmatched_images(optics_folder_path, sar_folder_path)
    delete_unmatched_images(label_folder_path, sar_folder_path)
