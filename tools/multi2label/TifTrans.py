"""
将16位遥感图像压缩至8位，并保持色彩一致
"""

from osgeo import gdal
import os
import glob
import numpy as np
import pandas as pd


def read_tiff(input_file):
    """
    读取影像
    :param input_file:输入影像
    :return:波段数据，仿射变换参数，投影信息、行数、列数、波段数
    """
    dataset = gdal.Open(input_file)

    rows = dataset.RasterYSize
    cols = dataset.RasterXSize

    geo = dataset.GetGeoTransform()
    proj = dataset.GetProjection()

    couts = dataset.RasterCount

    array_data = np.zeros((couts, rows, cols))

    for i in range(couts):
        band = dataset.GetRasterBand(i + 1)  # 读取每个波段的突破
        array_data[i, :, :] = band.ReadAsArray()  # 融合每个波段到图片

    return array_data, geo, proj, rows, cols, 3


def compress(origin_16, output_8):
    array_data, geo, proj, rows, cols, couts = read_tiff(origin_16)
    compress_data = np.zeros((couts, rows, cols))
    for i in range(couts):
        band_max = np.max(array_data[i, :, :])
        band_min = np.min(array_data[i, :, :])
        cutmin, cutmax = cumulativehistogram(array_data[i, :, :], rows, cols, band_min, band_max)
        compress_scale = (cutmax - cutmin) / 255
        temp = np.array(array_data[i, :, :])
        temp[temp > cutmax] = cutmax
        temp[temp < cutmin] = cutmin
        compress_data[i, :, :] = (temp - cutmin) / compress_scale
    write_tiff(output_8, compress_data, rows, cols, couts, geo, proj)


def write_tiff(output_file, array_data, rows, cols, counts, geo, proj):
    Driver = gdal.GetDriverByName("Gtiff")
    dataset = Driver.Create(output_file, cols, rows, counts, gdal.GDT_Byte)

    dataset.SetGeoTransform(geo)
    dataset.SetProjection(proj)

    for i in range(counts):
        band = dataset.GetRasterBand(i + 1)
        band.WriteArray(array_data[i, :, :])  # 波段写入顺序调整可以改变图像颜色，思路i改为2-i


def cumulativehistogram(array_data, rows, cols, band_min, band_max):
    gray_level = int(band_max - band_min + 1)
    gray_array = np.ones(gray_level)
    counts = 0
    b = array_data - band_min
    c = np.array(b).reshape(1, -1)
    d = pd.DataFrame(c[0])[0].value_counts()
    for i in range(len(d.index)):
        gray_array[int(d.index[i])] = int(d.values[i])
    counts = rows * cols
    count_percent2 = counts * 0.02
    count_percent98 = counts * 0.98
    cutmax = 0
    cutmin = 0
    for i in range(1, gray_level):
        gray_array[i] += gray_array[i - 1]
        if (gray_array[i] >= count_percent2 and gray_array[i - 1] <= count_percent2):
            cutmin = i + band_min
        if (gray_array[i] >= count_percent98 and gray_array[i - 1] <= count_percent98):
            cutmax = i + band_min
    return cutmin, cutmax
