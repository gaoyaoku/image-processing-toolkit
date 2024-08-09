import os
from skimage import morphology
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def process_image(image_path, output_folder):
    """
    处理单个图像，提取中心线并保存结果。
    :param image_path: 输入图像的路径。
    :param output_folder: 输出文件夹路径，用于保存处理后的图像。
    """
    # 从PNG图像加载
    image = Image.open(image_path)
    image = np.array(image)  # 将图像转换为NumPy数组

    # 替换255为1
    image[image == 255] = 1

    # 实施骨架算法
    skeleton = morphology.skeletonize(image)

    # 获取文件名
    file_name = os.path.basename(image_path)

    # 保存结果图像
    skeleton_image = Image.fromarray((skeleton * 255).astype(np.uint8))
    output_path = os.path.join(output_folder, file_name)
    skeleton_image.save(output_path)

    print(f"Processed and saved: {output_path}")


def process_images_in_folder(input_folder, output_folder):
    """
    处理文件夹中的所有图像，提取中心线并保存结果。
    :param input_folder: 输入文件夹路径，包含需要处理的图像。
    :param output_folder: 输出文件夹路径，用于保存处理后的图像。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(input_folder, filename)
            process_image(image_path, output_folder)


if __name__ == "__main__":
    # 设置输入文件夹和输出文件夹路径
    input_folder = r"P:\project_shp2label\output\road8_2-3\label"
    output_folder = r"P:\project_shp2label\output\center"

    # 处理文件夹中的所有图像
    process_images_in_folder(input_folder, output_folder)
