import os
import subprocess
import sys



def add_text_to_video(input_path, output_path, text):
    if os.path.exists(output_path):
        os.remove(output_path)
    # 设置 drawtext 参数
    font_file = "Arial"         # 字体名称或字体文件路径（如 "/path/to/font.ttf"）
    font_size = 50              # 字体大小
    font_color = "black"        # 字体颜色
    border_color = "white"      # 边框/背景色
    x_position = "(w-text_w)/2" # 水平居中
    y_position = "h-text_h-50"  # 距离底部 50px

    command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f"drawtext=fontfile={font_file}:"
               f"text='{text}':"
               f"fontsize={font_size}:"
               f"fontcolor={font_color}:"
               f"box=1:"
               f"boxcolor={border_color}@0.5:"
               f"x={x_position}:"
               f"y={y_position}",
        '-c:a', 'copy',         # 直接复制音频流
        output_path
    ]

    # 运行命令
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        print("✅ 添加文字成功！")
    else:
        print("❌ 添加文字失败！错误信息：")
        print(result.stderr.decode('utf-8'))


def main():
    os.environ['PATH'] = "/usr/bin:" + os.environ['PATH']
    # add_text_to_video(
    #     input_path="/home/zh/master_thesis_supplementary/syncnet_python/thesis_evaluate/306_angry1/sadtalker_512_still.mp4",
    #     output_path="/home/zh/master_thesis_supplementary/syncnet_python/thesis_evaluate/306_angry1/sadtalker_512_still_text.mp4",
    #     text="sadtalker"
    # )