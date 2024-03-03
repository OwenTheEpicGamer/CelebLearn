import os
import shutil
from base64 import b64encode
import moviepy.editor as mp


def get_video_resolution(video_path):
    """Function to get the resolution of a video"""
    import cv2
    video = cv2.VideoCapture(video_path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return (width, height)


def resize_video(video_path, new_resolution):
    """Function to resize a video"""
    import cv2
    video = cv2.VideoCapture(video_path)
    fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
    fps = video.get(cv2.CAP_PROP_FPS)
    width, height = new_resolution
    output_path = os.path.splitext(video_path)[0] + '_720p.mp4'
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    while True:
        success, frame = video.read()
        if not success:
            break
        resized_frame = cv2.resize(frame, new_resolution)
        writer.write(resized_frame)
    video.release()
    writer.release()


# @markdown ### Select an uploading method
upload_method = "Upload"  # @param ["Upload", "Custom Path"]

# remove previous input video
if os.path.isfile('/content/sample_data/input_vid.mp4'):
    os.remove('/content/sample_data/input_vid.mp4')

PATH_TO_YOUR_VIDEO = './assets/obama.mp4'

# video_duration = mp.VideoFileClip(PATH_TO_YOUR_VIDEO).duration
# if video_duration > 60:
#     print("WARNING: Video duration exceeds 60 seconds. Please upload a shorter video.")
#     raise SystemExit(0)

video_resolution = get_video_resolution(PATH_TO_YOUR_VIDEO)
print(f"Video resolution: {video_resolution}")
if video_resolution[0] >= 1920 or video_resolution[1] >= 1080:
    print("Resizing video to 720p...")
    os.system(f"ffmpeg -i {PATH_TO_YOUR_VIDEO} -vf scale=1280:720 ./assets/obama.mp4")
    PATH_TO_YOUR_VIDEO = './assets/obama.mp4'
    print("Video resized to 720p")
else:
    print("No resizing needed")




import os

upload_method = 'Upload'  # @param ['Record', 'Upload', 'Custom Path']







# Consider only the first file
PATH_TO_YOUR_AUDIO = './out.wav'

# Load audio with specified sampling rate
import librosa

audio, sr = librosa.load(PATH_TO_YOUR_AUDIO, sr=None)

# Save audio with specified sampling rate
import soundfile as sf

sf.write('./out.wav', audio, sr, format='wav')






# Set up paths and variables for the output file
output_file_path = './results/obama.mp4'

# Delete existing output file before processing, if any
if os.path.exists(output_file_path):
    os.remove(output_file_path)

pad_top =  0#@param {type:"integer"}
pad_bottom =  10#@param {type:"integer"}
pad_left =  0#@param {type:"integer"}
pad_right =  0#@param {type:"integer"}
rescaleFactor =  1#@param {type:"integer"}
nosmooth = True #@param {type:"boolean"}
#@markdown ___
#@markdown Model selection:
use_hd_model = False #@param {type:"boolean"}
checkpoint_path = '../Wav2Lip/checkpoints/wav2lip.pth' if not use_hd_model else '../Wav2Lip/checkpoints/wav2lip_gan.pth'

# Importing required module
import subprocess

# Using system() method to
# execute shell commands
if nosmooth:
    print(subprocess.run(["pwd"], shell=True))

    # subprocess.run(["python3", "../Wav2Lip/inference.py", f"--{checkpoint_path}", f"{checkpoint_path}", "--face", './results/obama.mp4', "--audio", "./out.wav", f"--pads", f"{pad_top}", f"{pad_bottom}", f"{pad_left}", f"{pad_right}", f"--resize_factor", f"{rescaleFactor}"])
    print("asd")

    command = [
        "python3", "../Wav2Lip/inference.py",
        "--checkpoint_path", checkpoint_path,
        "--face", './assets/obama (online-video-cutter.com).mp4',
        "--audio", "./out.wav",
        "--pads", str(pad_top), str(pad_bottom), str(pad_left), str(pad_right),
        "--resize_factor", str(rescaleFactor)
    ]

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    print("Asd")

#Preview output video
if os.path.exists(output_file_path):
    print("Success")
else:
    print("Processing failed. Output video not found.")



