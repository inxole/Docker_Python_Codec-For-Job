import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import svgwrite
from glob import glob

input_dir = '/app/uploads'
save_dir = '/app/output_folder'

# 出力フォルダが存在しない場合は作成
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 指定されたフォルダ内のすべてのPNGファイルを取得
file_paths = glob(os.path.join(input_dir, '*.png'))

# 各ファイルに対して処理を実行
for file_path in file_paths:
    file_name = os.path.basename(file_path)
    fname, ext = os.path.splitext(file_name)

    # 画像をOpenCVで読み込む
    img = cv2.imread(file_path)
    plt.imshow(img)

# グレースケールに変換する
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2値化フィルターによる輪郭の強調
contour = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 5)
plt.imshow(contour)

# 輪郭の座標を読み取る
contours, hierarchy = cv2.findContours(contour, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

# 必要な輪郭の(x,y)座標データを取得する
x_list = []
y_list = []
df_group_list = []

for i in range(len(contours)):
    # 階層が-1の場合に処理する
    if hierarchy[0][i][-1] == -1: 
        
        # numpyの多重配列になっているため、一旦展開する。
        buf_np = contours[i].flatten() 
        
        # (x, y)座標の取得
        for i, elem in enumerate(buf_np):
            if i%2 == 0: # 偶数の場合はx座標
                x_list.append(elem)
            else: # 奇数の場合はy座標
                y_list.append(elem * (-1))
        
        # pandasデータフレームへ変換
        mylist = list(zip(x_list, y_list))
        df_buf = pd.DataFrame(mylist, columns = ['x', 'y'])
        
        # データフレームをリストへ格納
        df_group_list.append(df_buf)
        
        # リストを空にして、次のオブジェクトの取得へ
        x_list.clear()
        y_list.clear()

# 抽出した輪郭をチェック
for i, df_buf in enumerate(df_group_list, start=1):
    plt.scatter(df_buf['x'], df_buf['y'], s = 0.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()

# 画像の縁の座標を削除する場合 True, 削除しない場合False
if True:
    for i, df_buf in enumerate(df_group_list):
        if not df_buf[(df_buf['x'] == 0) & (df_buf['y'] == 0)].empty:
            df_group_list.pop(i)

# 抽出した輪郭をチェック
DF_name_list = []
DF_list = []
for i, df_buf in enumerate(df_group_list, start=1):
    
    # 列名にid番号を付与して、DF_listリストへ格納
    DF_name_list.extend(['id_'+ '{0:03}'.format(i) + '_x', 'id_'+ '{0:03}'.format(i) + '_y'])
    DF_list.append(df_buf)

# データフレームを結合
DF = pd.concat(DF_list, axis=1)

# カラム名をリネーム
DF.columns = DF_name_list

# 座標をexcelファイルへ出力する。
DF.to_excel(os.path.join(save_dir, f'{fname}_04.xlsx'), index=False)

# ExcelファイルからSVGを作成する
outfile_name = os.path.join(save_dir, f'{fname}_05_Draw.svg')

# SVGファイルを作成するインスタンス生成
dwg = svgwrite.Drawing(outfile_name, profile='tiny')

# Excelファイルを読み込む
df = pd.read_excel(os.path.join(save_dir, f'{fname}_04.xlsx'))

# ExcelデータからSVGのパスを作成
for i in range(1, df.shape[1] // 2 + 1):  # 列の数の半分だけループ（x, yペアごと）
    x_col = f'id_{i:03}_x'
    y_col = f'id_{i:03}_y'
    
    # NaN（空白のセル）を削除して、座標ペアを取得
    points = df[[x_col, y_col]].dropna().values.tolist()
    
    # データを間引く場合はTrueを設定
    points = points[::10] if len(points) > 10 else points
    
    # 'd'属性の文字列を生成
    d_values = ['M'] + [f'{x},{-y}' for x, y in points]  # 'M x,-y L x,-y ...' 形式の文字列リストを生成
    d_attribute = ' '.join(d_values)
    
    # SVGのPath要素を作成し、ドキュメントに追加
    path = svgwrite.path.Path(d=d_attribute, stroke='black', fill='none')
    dwg.add(path)

# SVGファイルを保存
dwg.save()
del dwg