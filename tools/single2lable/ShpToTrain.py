from shapely.geometry import Polygon
import math
from osgeo import gdal
from osgeo import ogr
from PIL import Image, ImageDraw
from .utensil import specifics, counter


class DataSet:
    def __init__(self, image, img_points, Shapefile, block_size, OutputImagePath, OutputLabelPath, stride, field="Id"):
        self.block_size = block_size
        self.Image = image
        self.Shapefile = Shapefile
        self.OutputImagePath = OutputImagePath
        self.OutputLabelPath = OutputLabelPath
        self.target_field_name = field
        self.img_path = img_points
        self.stride = 1 - stride

    def getData(self):
        rX = specifics.get_image_transform(self.Image)[0]
        rY = abs(specifics.get_image_transform(self.Image)[1])
        width = specifics.get_image_transform(self.Image)[4]  # 列数
        height = specifics.get_image_transform(self.Image)[5]  # 行数
        block_size = self.block_size
        shapefile = self.Shapefile
        layer = shapefile.GetLayer()
        num = 0
        points = []
        attribute = []
        for feature in layer:
            num = num + 1
            target_field_name = self.target_field_name
            attribute_value = feature.GetField(target_field_name)
            attribute.append(attribute_value)
            geometry = feature.GetGeometryRef()
            coordinates = []
            for i in range(geometry.GetGeometryCount()):
                ring = geometry.GetGeometryRef(i)
                for j in range(ring.GetPointCount()):
                    x, y, _ = ring.GetPoint(j)
                    coordinates.append((x, y))
            points.append(coordinates)

        min_x, max_x, min_y, max_y = calculate_overall_bounding_box(points)

        lX = specifics.get_image_transform(self.Image)[2]
        lY = specifics.get_image_transform(self.Image)[3]
        bX = specifics.get_image_transform(self.Image)[6]
        bY = specifics.get_image_transform(self.Image)[7]
        min_x = max(min_x, lX)
        max_x = min(max_x, bX)
        min_y = max(min_y, bY)
        max_y = min(max_y, lY)
        feature_height = (max_y - min_y) / rY
        feature_width = (max_x - min_x) / rX
        block_size_2 = block_size * self.stride
        rows = math.ceil(feature_height / block_size_2)
        cols = math.ceil(feature_width / block_size_2)

        for i in range(rows):
            for j in range(cols):
                start_x = min_x + (j * block_size_2 * rX)
                start_y = min_y + (i * block_size_2 * rY)
                p1 = Polygon([(start_x, start_y), (start_x + (block_size * rX), start_y),
                              (start_x + (block_size * rX), start_y + (block_size * rY)),
                              (start_x, start_y + (block_size * rY)), (start_x, start_y)])
                points_in = []
                num_in = 0
                k_list = []

                for l in range(len(self.img_path)):
                    p3 = Polygon(self.img_path[l])

                    for k in range(0, num):
                        p2 = Polygon(points[k])
                        if p2.intersects(p1) and p3.intersects(p1):
                            points_in.append(points[k])
                            num_in = num_in + 1
                            k_list.append(k)
                        else:
                            continue
                if num_in > 0:
                    print(f"制作第{counter.a+1}张label")
                    self.get_label(start_x, start_y, points_in, counter.a, attribute, num_in, k_list)
                    print(f"制作第{counter.a+1}张image")
                    self.get_image(start_x, start_y, counter.a)
                    counter.a = counter.a + 1
                else:
                    continue

    def get_label(self, start_x, start_y, rounded_data, a, attribute_value, f_num, k_list):
        OutputLabelPath = self.OutputLabelPath
        rX = specifics.get_image_transform(self.Image)[0]
        rY = abs(specifics.get_image_transform(self.Image)[1])
        block_size = self.block_size

        image = Image.new("L", (block_size, block_size), color="black")
        draw = ImageDraw.Draw(image)

        for i in range(0, f_num):
            relative_polygon_coords = [((x - start_x) // rX, block_size - (y - start_y) // rY) for x, y in
                                       rounded_data[i]]

            draw.polygon(relative_polygon_coords, fill=255)

        file_name = f"{a}.png"
        file_path = f"{OutputLabelPath}/{file_name}"
        image.save(file_path)

    def get_image(self, start_x, start_y, a):
        rX = specifics.get_image_transform(self.Image)[0]
        rY = abs(specifics.get_image_transform(self.Image)[1])
        lX = specifics.get_image_transform(self.Image)[2]
        lY = specifics.get_image_transform(self.Image)[3]
        bX = specifics.get_image_transform(self.Image)[6]
        bY = specifics.get_image_transform(self.Image)[7]
        OutputImagePath = self.OutputImagePath
        block_size = self.block_size
        dataset = self.Image

        output_image_path = f"{OutputImagePath}/{a}.tiff"
        driver = gdal.GetDriverByName("GTiff")
        output_dataset = driver.Create(output_image_path, block_size, block_size, dataset.RasterCount,
                                       dataset.GetRasterBand(1).DataType)

        if output_dataset is None:
            print("Error: Unable to create the output raster image.")

        transform = (start_x, dataset.GetGeoTransform()[1], dataset.GetGeoTransform()[2],
                     (start_y+(block_size)*rY), dataset.GetGeoTransform()[4], dataset.GetGeoTransform()[5])

        output_dataset.SetGeoTransform(transform)

        output_dataset.SetProjection(dataset.GetProjectionRef())

        for i in range(1, dataset.RasterCount + 1):
            band = dataset.GetRasterBand(i)
            if start_x + (block_size * rX) <= bX and start_y + (block_size * rY) <= lY:
                data = band.ReadAsArray((abs(start_x - lX)) / rX, (abs(start_y + (block_size * rY) - lY)) / rY,
                                        block_size, block_size)
                output_band = output_dataset.GetRasterBand(i)
                output_band.WriteArray(data)

            elif start_y + (block_size * rY) > lY and start_x + (block_size * rX) > bX:
                dx = math.floor((bX - start_x)/rX)
                dy = math.floor((lY - start_y)/rY)
                data = band.ReadAsArray((abs(start_x - lX)) / rX, (abs(start_y + (dy * rY) - lY)) / rY,
                                        dx, dy)
                output_band = output_dataset.GetRasterBand(i)
                output_band.WriteArray(data, 0, block_size-dy)
            elif start_y + (block_size * rY) <= lY and start_x + (block_size * rX) > bX:
                dx = math.floor((bX - start_x) / rX)
                data = band.ReadAsArray((abs(start_x - lX)) / rX, (abs(start_y + (block_size * rY) - lY)) / rY,
                                        dx, block_size)
                output_band = output_dataset.GetRasterBand(i)
                output_band.WriteArray(data)
            elif start_y + (block_size * rY) > lY and start_x + (block_size * rX) <= bX:
                dy = math.floor((lY - start_y) / rY)
                data = band.ReadAsArray((abs(start_x - lX)) / rX, (abs(start_y + (dy * rY) - lY)) / rY,
                                        block_size, dy)
                output_band = output_dataset.GetRasterBand(i)
                output_band.WriteArray(data, 0, block_size-dy)
        output_dataset.FlushCache()


def calculate_bounding_box(coordinates):
    if not coordinates:
        return None

    min_x = min(point[0] for point in coordinates)
    max_x = max(point[0] for point in coordinates)
    min_y = min(point[1] for point in coordinates)
    max_y = max(point[1] for point in coordinates)

    top_left = (min_x, min_y)
    top_right = (max_x, min_y)
    bottom_left = (min_x, max_y)
    bottom_right = (max_x, max_y)

    bounding_box = [top_left, top_right, bottom_right, bottom_left]

    return bounding_box


def calculate_overall_bounding_box(coordinates_list):
    if not coordinates_list:
        return None

    all_x = [point[0] for coordinates in coordinates_list for point in coordinates]
    all_y = [point[1] for coordinates in coordinates_list for point in coordinates]
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    return min_x, max_x, min_y, max_y