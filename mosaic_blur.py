# モザイク処理
# ぼかし処理


import os
import glob
from PIL import Image

dir_target_jpg = '/home/yuya/m1/mosaic/cyclegan/pytorch-CycleGAN-and-pix2pix/datasets/horse_mosaic2/trainA/*.jpg'
# dir_target_jpg = '/home/yuya/m1/mosaic/cyclegan/pytorch-CycleGAN-and-pix2pix/datasets/horse_mosaic2/testA/*.jpg'

list_filepath_src = glob.glob(dir_target_jpg, recursive=True)
print(list_filepath_src)

intensity = 5 # 加工の強さ

for filepath_src in list_filepath_src:
    

    original = Image.open(filepath_src)

    # 画像サイズをintensity分の1に縮小
    small = original.resize(
        (round(original.width / intensity), round(original.height / intensity))
    )

    # モザイク処理の場合
    """"""
    # 元画像のサイズに拡大してモザイク処理
    mosaic = small.resize(
        (original.width,original.height),
        resample=Image.NEAREST # 最近傍補間
    )
    mosaic.save(filepath_src)

    # ぼかし処理の場合
    """
    # 元画像のサイズに拡大してぼかし処理
    blur = small.resize(
        (original.width,original.height),
        resample=Image.BILINEAR # 双線形補間
    )
    blur.save(filepath_src)
    """