
import pandas as pd
import svgwrite

# データの読み込み
df = pd.read_excel('/app/output_folder/test_04.xlsx')

# SVGファイルの作成
dwg = svgwrite.Drawing('output.svg', profile='tiny')

# ExcelデータからSVGのパスを作成
for i in range(1, df.shape[1] // 2 + 1):  # 列の数の半分だけループ（x, yペアごと）
    x_col = f'id_{i:03}_x'
    y_col = f'id_{i:03}_y'
    
    # NaN（空白のセル）を削除して、座標ペアを取得
    points = df[[x_col, y_col]].dropna().values.tolist()
    
    # 'd'属性の文字列を生成
    d_values = ['M'] + [f'{x},{y}' for x, y in points]  # 'M x,y L x,y ...' 形式の文字列リストを生成
    d_attribute = ' '.join(d_values)
    
    # SVGのPath要素を作成し、ドキュメントに追加
    path = svgwrite.path.Path(d=d_attribute, stroke='black', fill='none')
    dwg.add(path)

# SVGファイルを保存
dwg.save()
