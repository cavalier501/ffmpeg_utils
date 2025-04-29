import subprocess
import os
import sys
from typing import Optional

def images_to_video(
    image_folder: str,
    output_video_path: str,
    framerate: int = 25,
    image_pattern: str = "*.png"
) -> bool:
    """
    将图片序列合成为视频（对应您图片中的"视频的合成"功能）
    
    :param image_folder: 存放图片的文件夹路径（如 "/path/to/images"）
    :param output_video_path: 输出视频路径（如 "output.mp4"）
    :param framerate: 帧率（默认25帧/秒）
    :param image_pattern: 图片匹配模式（默认"*.png"）
    :return: True表示成功，False表示失败
    """
    try:
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(framerate),
            "-f", "image2",
            "-pattern_type", "glob",
            "-i", f"{image_folder}/{image_pattern}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_video_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return False

def video_to_images(
    input_video: str,
    output_dir: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    output_framerate: Optional[int] = None,
    output_format: str = "%04d.jpg"
) -> bool:
    """
    使用ffmpeg切割视频到指定文件夹
    
    :param input_video: 输入视频文件路径
    :param output_dir: 输出目录路径
    :param start_time: 开始时间(格式: HH:MM:SS 或 秒数)，None表示从开头
    :param end_time: 结束时间(格式同上)，None表示到结尾
    :param output_framerate: 输出帧率，None保持原帧率
    :param output_format: 输出文件名格式(默认: %04d.jpg)
    :return: True表示成功，False表示失败
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = ["ffmpeg", "-y", "-i", input_video]
        
        # 添加时间范围参数
        if start_time:
            cmd.extend(["-ss", str(start_time)])
        if end_time:
            cmd.extend(["-to", str(end_time)])
        
        # 添加帧率参数
        if output_framerate:
            cmd.extend(["-r", str(output_framerate)])
        
        # 输出设置
        cmd.extend([
            "-f", "image2",
            os.path.join(output_dir, output_format)
        ])
        
        # 执行命令
        subprocess.run(cmd, check=True, capture_output=True)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode('utf-8')}")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def extract_crop_with_ffmpeg(video_path, save_dir, crop_box, target_fps=None):
    """
    使用ffmpeg提取视频帧并裁剪
    图片结果只保留裁剪区域的部分

    参数:
        video_path (str): 视频路径
        save_dir (str): 保存裁剪帧的路径
        crop_box (tuple): (x, y, w, h) 裁剪框
        target_fps (int or None): 目标帧率（可选）
    """
    os.makedirs(save_dir, exist_ok=True)

    x, y, w, h = crop_box
    crop_str = f"crop={w}:{h}:{x}:{y}"

    cmd = [
        "ffmpeg",
        "-i", video_path,
    ]

    if target_fps:
        cmd += ["-r", str(target_fps)]  # 设置输出帧率

    cmd += [
        "-vf", crop_str,
        os.path.join(save_dir, "%05d.jpg")
    ]

    print("运行命令：", " ".join(cmd))
    subprocess.run(cmd)



def main():
    # # 图片合成视频
    # images_to_video(
    #     image_folder="/tmp/images",
    #     output_video_path="output.mp4"
    # )
    # video_to_images(
    #     "/home/zh/master_thesis_supplementary/syncnet_python/thesis_evaluate/306_angry1/aniportrait_2.mp4",
    #     "./test",
    #     start_time="00:00:01",
    #     end_time="00:00:02",
    # )
    return
if __name__ == '__main__':
    main()

