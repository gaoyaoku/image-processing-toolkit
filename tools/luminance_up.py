import os
from PIL import Image, ImageEnhance


def increase_brightness(image_path, output_path, brightness_factor):
    """
    增加图像的亮度。
    :param image_path: 输入图像的路径。
    :param output_path: 增加亮度后的图像保存路径。
    :param brightness_factor: 亮度增加的倍数（1.0表示不变，2.0表示亮度加倍）。
    """
    # 打开图像
    image = Image.open(image_path)
    # 创建亮度增强对象
    enhancer = ImageEnhance.Brightness(image)
    # 增加亮度
    image_enhanced = enhancer.enhance(brightness_factor)
    # 保存增强后的图像
    image_enhanced.save(output_path)


def process_folder(input_folder, output_folder, brightness_factor):
    """
    处理文件夹中的所有图像，增加其亮度并保存到指定的输出文件夹。

    :param input_folder: 输入文件夹路径，包含需要处理的图像。
    :param output_folder: 输出文件夹路径，用于保存处理后的图像。
    :param brightness_factor: 亮度增加的倍数。
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            increase_brightness(input_path, output_path, brightness_factor)
            print(f"Processed {filename}")


if __name__ == "__main__":
    # 输入文件夹路径
    input_folder = r"P:\project_sar_road\data\road6_26\train\images_optics"
    # 输出文件夹路径
    output_folder = r"P:\project_sar_road\data\road7_2\train\images_optics"
    # 亮度增加的倍数（1.0表示不变，2.0表示亮度加倍）
    brightness_factor = 1.8
    # 处理文件夹中的所有tif图像
    process_folder(input_folder, output_folder, brightness_factor)
