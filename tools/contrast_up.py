import os
from PIL import Image, ImageEnhance


def enhance_contrast(original_folder, enhanced_folder, contrast_factor = 2):
    """
    增强文件夹中所有TIF图像的对比度并保存到另一个文件夹。
    :param original_folder: 原始图像文件夹路径。
    :param enhanced_folder: 增强后图像文件夹路径。
    :param contrast_factor: 对比度增强因子，默认值为2。
    """
    # 如果增强后文件夹不存在，则创建它
    if not os.path.exists(enhanced_folder):
        os.makedirs(enhanced_folder)

    # 遍历原始文件夹中的所有文件
    for filename in os.listdir(original_folder):
        if filename.endswith('.tif'):
            # 打开图像
            img_path = os.path.join(original_folder, filename)
            img = Image.open(img_path)

            # 增强对比度
            enhancer = ImageEnhance.Contrast(img)
            enhanced_img = enhancer.enhance(contrast_factor)

            # 保存增强后的图像到增强文件夹
            enhanced_img.save(os.path.join(enhanced_folder, filename))

    print("所有 TIF 文件的对比度增强已完成，并保存在新的文件夹中。")


if __name__ == "__main__":
    # 示例用法
    original_folder = r"P:\project_sar_road\data\road7_5\image_sar"
    enhanced_folder = r"P:\project_sar_road\data\road7_8\image_sar"
    contrast_factor = 2  # 可调整对比度增强因子

    enhance_contrast(original_folder, enhanced_folder, contrast_factor)

