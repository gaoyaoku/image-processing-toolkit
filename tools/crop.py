from PIL import Image

Image.MAX_IMAGE_PIXELS = 500000000


def crop_image(input_file, output_dir, tile_size=(1024, 1024)):
    # 打开原始图像
    img = Image.open(input_file)

    # 获取图像尺寸
    img_width, img_height = img.size
    tile_width, tile_height = tile_size

    # 计算横向和纵向的切片数量
    num_tiles_x = img_width // tile_width
    num_tiles_y = img_height // tile_height

    for x in range(num_tiles_x):
        for y in range(num_tiles_y):
            # 定义裁剪区域
            left = x * tile_width
            upper = y * tile_height
            right = left + tile_width
            lower = upper + tile_height

            # 裁剪图像
            box = (left, upper, right, lower)
            cropped_img = img.crop(box)

            # 保存裁剪后的图像
            cropped_img.save(f"{output_dir}/tile_{x}_{y}.tif")


if __name__ == '__main__':
    # 示例调用
    input_file = '/Users/gaoyaoku/Documents/Datasets/path/optics/gf1_1.tif'
    output_dir = '../data/sar1024'
    crop_image(input_file, output_dir)
