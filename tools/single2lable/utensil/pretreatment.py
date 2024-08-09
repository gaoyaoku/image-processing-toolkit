from shapely.geometry import Polygon
from utensil import specifics
import fiona
import pyproj
from osgeo import gdal, ogr, osr
import os


def get_resolution(file_path):
    dataset = gdal.Open(file_path)
    if dataset is not None:
        geotransform = dataset.GetGeoTransform()
        x_resolution = geotransform[1]
        y_resolution = geotransform[5]
        return x_resolution, y_resolution
    return None


def sort_image_paths_by_resolution(image_paths):
    # 创建一个字典，将图像文件路径和其分辨率关联起来
    resolution_dict = {}
    for file_path in image_paths:
        resolution = get_resolution(file_path)
        if resolution is not None:
            resolution_dict[file_path] = resolution
    # 根据分辨率值从大到小排序图像文件路径
    sorted_image_paths = sorted(image_paths, key=lambda x: resolution_dict[x], reverse=True)
    return sorted_image_paths


def group_image(img_path):
    # 用于存储图像坐标的列表
    img_points = []
    img_point = []
    # 打开每个图像并提取其坐标
    for i, image_path in enumerate(img_path):
        img = gdal.Open(image_path)
        rX, rY, lX, lY, width, height, bX, bY = specifics.get_image_transform(img)
        points = [(lX, lY), (bX, lY), (bX, bY), (lX, bY)]

        coordinates = Polygon([(lX, lY), (bX, lY), (bX, bY), (lX, bY)])
        img_points.append((i, coordinates, img_path[i], points))  # 存储图像编号和坐标

    # 创建一个空列表来存储分组结果
    groups = []
    for i, polygon1, image_path1, points1 in img_points:
        # 创建一个标志来指示是否与任何一个已分组的图像坐标相交
        intersects = False
        for group in groups:
            for j, polygon2, image_path2, points2 in group:
                if polygon1.intersects(polygon2):
                    group.append((i, polygon1, image_path1, points1))
                    intersects = True
                    break
        # 如果没有与任何已分组的图像坐标相交，创建一个新的分组
        if not intersects:
            groups.append([(i, polygon1, image_path1, points1)])
    img_point = [[image_p for _, _, _, image_p in group] for group in groups]
    grouped_image_paths = [[image_path for _, _, image_path, _ in group] for group in groups]
    return grouped_image_paths, img_point


def data_input(ImagePath, ShapefilePath):
    shapefile = ogr.Open(ShapefilePath)
    if shapefile is None:
        print("无法打开Shapefile文件。")
        exit(1)
    espg_list = []
    for i in range(len(ImagePath)):
        dataset = gdal.Open(ImagePath[i])
        if dataset is not None:
            # 获取栅格数据的地理坐标系统
            spatial_ref = dataset.GetProjection()
            # 使用GDAL的SpatialReference类来解析EPSG代码
            srs = osr.SpatialReference()
            srs.ImportFromWkt(spatial_ref)
            # 获取EPSG代码
            epsg_code = srs.GetAuthorityCode(None)
            espg_list.append(epsg_code)
            if epsg_code is None:
                print("无法获取EPSG值。")
            # 关闭栅格数据集
            dataset = None
        else:
            print("无法打开栅格数据文件。")
            exit(1)
    img_path = [ImagePath[0]]
    for n in range(1, len(ImagePath)):
        if espg_list[0] != espg_list[n]:
            tiff_name = os.path.basename(ImagePath[n])
            input_ds = gdal.Open(ImagePath[n])
            source_srs = osr.SpatialReference()
            source_srs.ImportFromEPSG(espg_list[n])
            target_srs = osr.SpatialReference()
            target_srs.ImportFromEPSG(espg_list[0])
            # 创建坐标系转换器
            transform = osr.CoordinateTransformation(source_srs, target_srs)
            # 创建输出栅格数据
            output_file = f"./tmp/{tiff_name}"
            output_ds = gdal.Warp(output_file, input_ds, dstSRS=target_srs)
            # 关闭数据集
            input_ds = None
            output_ds = None
            img_path.append(output_file)
        else:
            img_path.append(ImagePath[n])
    # print(img_path)
    grouped_image_paths = group_image(img_path)[0]
    img_points = group_image(img_path)[1]
    # print(grouped_image_paths)
    options = gdal.BuildVRTOptions(
        separate=False,  # 如果希望每个输入数据集在VRT中保持独立数据集，请设置为True
        hideNodata=True,  # 隐藏输入数据集中的nodata值
        resolution='highest',
        srcNodata=0,  # 输入数据集中的nodata值
        VRTNodata=0  # VRT文件中的nodata值
    )
    vrt_list = []
    for i in range(len(grouped_image_paths)):
        sorted_paths = sort_image_paths_by_resolution(grouped_image_paths[i])
        vrt_ds = gdal.BuildVRT(f"./tmp/vrt_ds{i}.vrt", sorted_paths, options=options)
        vrt_list.append(vrt_ds)

    raster_crs = vrt_list[0].GetProjection()
    vector_data = fiona.open(ShapefilePath)
    vector_crs = vector_data.crs
    vector_proj = pyproj.CRS(vector_crs).to_proj4()
    raster_proj = pyproj.CRS(raster_crs).to_proj4()
    if vector_proj == raster_proj:
        return shapefile, vrt_list, img_points
    else:
        VectorTranslate(ShapefilePath, "./tmp", format="ESRI Shapefile", dstSrsESPG=espg_list[0])
        file_name = os.path.basename(ShapefilePath)
        file_name_without_extension = os.path.splitext(file_name)[0]
        shapefile_new = ogr.Open(f"./tmp/{file_name_without_extension}/{file_name}")
        return shapefile_new, vrt_list, img_points


def VectorTranslate(
        shapeFilePath,
        saveFolderPath,
        format="ESRI Shapefile",
        accessMode=None,
        dstSrsESPG=4326,
        selectFields=None,
        geometryType="POLYGON",
        dim="XY", ):
    """
    转换矢量文件，包括坐标系，名称，格式，字段，类型，纬度等。

    :param shapeFilePath: 要转换的矢量文件
    :param saveFolderPath: 生成矢量文件保存目录
    :param format: 矢量文件格式，强烈建议不要使用ESRI Shapefile格式。
    :param accessMode:None代表creation,'update','append','overwrite'
    :param dstSrsESPG: 目标坐标系EPSG代码，4326是wgs84地理坐标系
    :param selectFields: 需要保留的字段列表如果都保留，则为None
    :param geometryType: 几何类型,"POLYGON","POINT"。。。
    :param dim: 新矢量文件坐标纬度,建议查阅官方API。
    :return:

    """
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    data = ogr.Open(shapeFilePath)
    layer = data.GetLayer()
    spatial = layer.GetSpatialRef()
    layerName = layer.GetName()
    data.Destroy()
    dstSRS = osr.SpatialReference()
    dstSRS.ImportFromEPSG(int(dstSrsESPG))
    if format == "GeoJSON":
        destDataName = layerName + ".geojson"
        destDataPath = os.path.join(saveFolderPath, destDataName)
    elif format == "ESRI Shapefile":
        destDataName = os.path.join(saveFolderPath, layerName)
        flag = os.path.exists(destDataName)
        os.makedirs(destDataName) if not flag else None
        destDataPath = os.path.join(destDataName, layerName + ".shp")
    else:
        print("不支持该格式！")
        return
    options = gdal.VectorTranslateOptions(
        format=format,
        accessMode=accessMode,
        srcSRS=spatial,
        dstSRS=dstSRS,
        reproject=True,
        selectFields=selectFields,
        layerName=layerName,
        geometryType=geometryType,
        dim=dim
    )
    gdal.VectorTranslate(
        destDataPath,
        srcDS=shapeFilePath,
        options=options
    )
    return destDataPath


