# python2video

An utility script which executes single file Python program and creates a video file displaying execution steps.

## Prerequisites

```
sudo apt install expect ffmpeg
python3 -m pip install --upgrade Pillow
```
## Usage

### To run program and create video on the same machine

```
path_to_script/python2video.sh your_program.py
```
This will create `your_program.mp4` video file.

### To run program on one machine and generate video on the other

```
path_to_script/python2trace.py your_program.py > your_program.csv
```
This will create `your_program.csv` trace file. Copy it to machine where you want to generate video.

```
cat your_program.csv | path_to_script/trace2video.py your_program.py
```
This will create `your_program.mp4` video file.
