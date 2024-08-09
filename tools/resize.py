import os
from PIL import Image
from PIL.Image import Resampling


def resize(input_folder: str, output_folder: str, image_type: str, height: int = 512, width: int = 512):
    """
    调整输入文件夹中所有图像的大小，并保存到输出文件夹。

    :param input_folder: 输入文件夹路径，包含需要调整大小的图像。
    :param output_folder: 输出文件夹路径，用于保存调整大小后的图像。
    :param image_type: 要调整的图像类型。
    :param height: 调整后的图像大小，默认为512。
    :param width: 调整后的图像大小，默认为512。
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith("." + image_type):
            # 使用Pillow读取图像
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                # 调整图像大小
                resized_img = img.resize((width, height), resample=Resampling.BICUBIC)
                # 构造输出文件路径
                output_path = os.path.join(output_folder, filename)
                # 保存调整大小后的图像，确保使用16位深度保存
                resized_img.save(output_path)
