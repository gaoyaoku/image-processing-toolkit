from fastapi import FastAPI, Query
from typing import List

from tools import resize
from tools import contrast_up
from tools.multi2label import main as multi2label

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/resize")
async def get_resize(input_folder: str,
                     output_folder: str,
                     image_type: str,
                     height: int = 512,
                     width: int = 512):
    resize.resize(input_folder, output_folder, image_type, height, width)

    return {"message": "ok"}


@app.get("/contrast")
async def get_contrast(original_folder: str,
                       enhanced_folder: str,
                       contrast_factor: int = 2):
    contrast_up.enhance_contrast(original_folder, enhanced_folder, contrast_factor)

    return {"message": "ok"}


@app.get("/multi2label")
async def get_multi2label(shapefile_path: str,
                          output_label_path: str,
                          output_sar_path: str,
                          output_optics_path: str,
                          output_rgb_path: str,
                          sar_path: List[str] = Query(),
                          optics_path: List[str] = Query(),
                          block_size: int = 512,
                          stride: int = 0.5,
                          UCS: bool = False,
                          tif2RGB: bool = False):
    multi2label.main(shapefile_path, sar_path, optics_path, output_label_path, output_sar_path, output_optics_path,
                     output_rgb_path, block_size, stride, UCS, tif2RGB)

    return {"message": "ok"}


@app.get("/test")
async def test(name: List[str] = Query()):
    print(name)
    return {"message": "ok"}
