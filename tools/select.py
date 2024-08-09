"""
随机抽取指定数量的测试数据，并删除源路径中被抽取的数据
"""
import os
import random
import shutil


def find_common_image_basenames(folder1, folder2, folder3):
    """
    查找三个文件夹中共有的文件名（不包括后缀）。
    :param folder1: 第一个文件夹路径。
    :param folder2: 第二个文件夹路径。
    :param folder3: 第三个文件夹路径。
    :return: 共有文件名的列表。
    """
    basenames1 = {os.path.splitext(f)[0] for f in os.listdir(folder1)}
    basenames2 = {os.path.splitext(f)[0] for f in os.listdir(folder2)}
    basenames3 = {os.path.splitext(f)[0] for f in os.listdir(folder3)}

    # 找到三个文件夹中共有的文件名
    common_basenames = basenames1 & basenames2 & basenames3
    return list(common_basenames)


def randomly_select_and_copy_images(source_folders, destination_folders, num_images=500):
    """
    从源文件夹中随机选择共有的图像文件，并复制到目标文件夹。
    :param source_folders: 源文件夹列表，需要包含三个文件夹路径。
    :param destination_folders: 目标文件夹列表，需要包含三个文件夹路径。
    :param num_images: 要随机选择的图像数量，默认值为500。
    """
    if len(source_folders) != 3 or len(destination_folders) != 3:
        print("需要提供三个源文件夹和三个目标文件夹。")
        return

    common_basenames = find_common_image_basenames(*source_folders)

    if len(common_basenames) < num_images:
        print(f"警告：共有图像文件少于 {num_images} 个，将使用所有共有图像文件。")
        num_images = len(common_basenames)

    selected_basenames = random.sample(common_basenames, num_images)

    for i in range(3):
        os.makedirs(destination_folders[i], exist_ok=True)
        for basename in selected_basenames:
            # 查找并复制匹配的文件
            for f in os.listdir(source_folders[i]):
                if os.path.splitext(f)[0] == basename:
                    shutil.copy(os.path.join(source_folders[i], f), os.path.join(destination_folders[i], f))
                    os.remove(os.path.join(source_folders[i], f))
                    break  # 只需要复制和删除一个匹配的文件

    print(f"已成功抽取 {num_images} 张图像到目标文件夹，并从源文件夹中删除。")


if __name__ == "__main__":
    # 示例用法
    source_folders = [
        r"P:\project_sar_road\data\road7_8\train\image_optics",  # 第一个源文件夹路径
        r"P:\project_sar_road\data\road7_8\train\image_sar",  # 第二个源文件夹路径
        r"P:\project_sar_road\data\road7_8\train\label"  # 第三个源文件夹路径
    ]

    destination_folders = [
        r"P:\project_sar_road\data\road7_8\test\image_optics",  # 第一个目标文件夹路径
        r"P:\project_sar_road\data\road7_8\test\image_sar",  # 第二个目标文件夹路径
        r"P:\project_sar_road\data\road7_8\test\label" # 第三个目标文件夹路径
    ]
    randomly_select_and_copy_images(source_folders, destination_folders, num_images=500)

