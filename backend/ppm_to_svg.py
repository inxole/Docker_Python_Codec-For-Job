import subprocess
import os

input_dir = 'input'
output_dir = 'output'

# 入力フォルダ内の全てのPPMファイルを検索
for filename in os.listdir(input_dir):
    if filename.endswith(".ppm"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.ppm', '.svg'))

        # Potraceコマンドを構築
        command = f"potrace {input_path} -s -o {output_path}"

        # コマンドを実行
        subprocess.run(command, shell=True)

print("変換が完了しました。")
