import os
import subprocess
import sys

def concate_videos_horizontally(video_list, output_path):
    if len(video_list) < 2:
        print("需要至少两个视频进行拼接！")
        return

    # 检查输入视频文件是否存在
    for video in video_list:
        if not os.path.exists(video):
            print(f"文件不存在: {video}")
            return

    # 构建 FFmpeg 命令
    input_args = []
    filter_complex = ""
    pad_width = f"iw*{len(video_list)}"
    filter_complex += f"[0:v]pad={pad_width}:ih[a0];"

    for i in range(1, len(video_list)):
        input_args.extend(["-i", video_list[i]])
        overlay_x = f"{i}*w"
        filter_complex += f"[a{i-1}][{i}:v]overlay=x={overlay_x}:y=0[a{i}];"

    filter_complex = filter_complex.rstrip(";")

    command = [
        "ffmpeg", "-y",
        "-i", video_list[0],
        *input_args,
        "-filter_complex", filter_complex,
        "-map", f"[a{len(video_list) - 1}]",
        "-c:v", "libx264",
        output_path
    ]

    print("执行命令:", " ".join(command))

    # 执行 FFmpeg 命令
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"视频拼接完成: {output_path}")
        else:
            print("拼接失败！错误信息:")
            print(result.stderr)
    except Exception as e:
        print(f"执行 FFmpeg 过程中发生错误: {e}")

def concate_videos_vertically(video_list, output_path):
    if len(video_list) < 2:
        print("需要至少两个视频进行拼接！")
        return

    # 检查输入视频文件是否存在
    for video in video_list:
        if not os.path.exists(video):
            print(f"文件不存在: {video}")
            return

    # 构建 FFmpeg 命令
    input_args = []
    filter_complex = ""
    pad_height = f"ih*{len(video_list)}"
    filter_complex += f"[0:v]pad=iw:{pad_height}[a0];"

    for i in range(1, len(video_list)):
        input_args.extend(["-i", video_list[i]])
        overlay_y = f"{i}*h"
        filter_complex += f"[a{i-1}][{i}:v]overlay=x=0:y={overlay_y}[a{i}];"

    filter_complex = filter_complex.rstrip(";")

    command = [
        "ffmpeg", "-y",
        "-i", video_list[0],
        *input_args,
        "-filter_complex", filter_complex,
        "-map", f"[a{len(video_list) - 1}]",
        "-c:v", "libx264",
        output_path
    ]

    print("执行命令:", " ".join(command))

    # 执行 FFmpeg 命令
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"视频拼接完成: {output_path}")
        else:
            print("拼接失败！错误信息:")
            print(result.stderr)
    except Exception as e:
        print(f"执行 FFmpeg 过程中发生错误: {e}")


def main():
    os.environ['PATH'] = "/usr/bin:" + os.environ['PATH']
        # concate_videos_horizontally(
    #     [
    #         "/home/zh/master_thesis_supplementary/syncnet_python/thesis_evaluate/306_angry1/ours_v2_text.mp4",
    #         "/home/zh/master_thesis_supplementary/syncnet_python/thesis_evaluate/306_angry1/wav2lip_text.mp4",
    #         "/home/zh/master_thesis_supplementary/syncnet_python/thesis_evaluate/306_angry1/sadtalker_512_text.mp4",
    #         "/home/zh/master_thesis_supplementary/syncnet_python/thesis_evaluate/306_angry1/aniportrait_text.mp4",
    #     ],
    #     "/home/zh/master_thesis_supplementary/syncnet_python/thesis_evaluate/306_angry1/方法对比.mp4",
    # )
    # concate_videos_vertically(
    #     [
    #         "output/306_dataset_flame_teeth/test_6_iter_600000/renders_rgb_result.mp4",
    #         "output/306_dataset_flame_teeth/test_6_iter_600000/renders_parsed_mesh.mp4",
    #         "output/306_dataset_flame_all_parsing/test_6_iter_600000/renders_rgb_result.mp4",
    #         "output/306_dataset_flame_all_parsing/test_6_iter_600000/renders_parsed_mesh.mp4",
    #     ],
    #     "output/306_dataset_flame_teeth/test_6_iter_600000/check_result.mp4",
    # )