'''
ディレクトリに対して、その中にあるすべての画像ファイルにモザイクをかける
画像ファイルごとに、ランダム領域に同サイズのモザイクをかけるようにする
モザイク領域のサイズの大きさは、mosaic_sizeで調整可能
モザイクをかける強さの度合いは、intensityで調整
intensity
'''

import os
import cv2
import numpy as np
import random
import os
# import cv2
from PIL import Image
import numpy as np
import random

def apply_random_mosaic(image, mosaic_size, intensity):
    # 画像の高さと幅を取得
    # height = image.height
    # width = image.width
    height, width, channel = image.shape
    
    # ランダムな位置でモザイクをかける
    start_x = random.randint(0, width - mosaic_size)
    start_y = random.randint(0, height - mosaic_size)
    end_x = start_x + mosaic_size
    end_y = start_y + mosaic_size

    # モザイク領域の元画像
    original = image[start_y:end_y, start_x:end_x].copy()
    # 画像サイズをintensity分の1に縮小
    small = cv2.resize(
        original,
        (
            round(mosaic_size / intensity),
            round(mosaic_size / intensity)
        )
    )
    # 元画像のサイズに拡大してモザイク処理
    mosaic = cv2.resize(
        small,
        (
            mosaic_size,
            mosaic_size
        ),
        interpolation=cv2.INTER_NEAREST # 最近傍補間
    )
    # 出力初期化
    ret = image.copy()
    ret[start_y:end_y, start_x:end_x] = mosaic
    mask = np.zeros((height, width)) # 黒で初期化
    mask[start_y:end_y, start_x:end_x] = 255 # モザイク領域白
    return (ret, mask)

def apply_mosaic_to_directory(input_dir, output_dir, mask_dir, mosaic_size, intensity):
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(mask_dir):
        os.makedirs(mask_dir)

    # 入力ディレクトリ内の画像ファイルを取得
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # 画像の読み込み
        image_path = os.path.join(input_dir, image_file)
        image = cv2.imread(image_path)
        # image = Image.open(image_path)

        # モザイクをかける
        result_image, mask_image = apply_random_mosaic(image.copy(), mosaic_size, intensity)

        # 出力ディレクトリに保存
        output_path = os.path.join(output_dir, f"mosaic_{image_file}")
        cv2.imwrite(output_path, result_image)
        mask_path = os.path.join(mask_dir, f"mask_{image_file}")
        cv2.imwrite(mask_path, mask_image)

# パラメータの設定
##########
# 入力ディレクトリ　ここ変更する
input_directory = "../datasets/horse"
##########
output_directory = input_directory + "_mosaic"
mask_directory = input_directory + "_mask"

##########
# モザイク領域の正方形サイズと、強さを変更できる
mosaic_size = 40  # モザイクのサイズ
intensity = 10  # モザイクの強さ(2以上整数)
##########
# モザイクをかけて保存
apply_mosaic_to_directory(input_directory, output_directory, mask_directory, mosaic_size, intensity)
