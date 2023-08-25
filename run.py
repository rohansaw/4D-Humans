import os
import glob
import argparse
import shutil
import subprocess
os.environ["PYOPENGL_PLATFORM"] = "osmesa"

program = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=100))
program.add_argument('-t', '--in-path', help='select an target image or video', dest='input_path')
program.add_argument('-o', '--out-path', help='select output file or directory', dest='output_path')

args, unknown = program.parse_known_args()

output_folder = os.path.split(args.output_path)[0]
output_file_name = os.path.split(args.output_path)[1]
input_folder_name = os.path.split(args.input_path)[1]
input_file_name = os.path.split(args.input_path)[1]

local_out_dir = "/4dhumans-res"
if not os.path.exists(local_out_dir):
    os.mkdir(local_out_dir)
files = glob.glob(local_out_dir + "/*")
for f in files:
    os.remove(f)

vid_source = 'video.source="' + args.input_path + '"'
vid_out = 'video.output_dir="' + local_out_dir + '"'
res = subprocess.run(["python3", "track.py", vid_source, vid_out], shell=False, capture_output=True, cwd="/4D-Humans/", env=dict(os.environ))
print(res.stderr)
print(res.stdout)

local_result_file = os.path.join(local_out_dir, "PHALP_" + input_file_name)
if os.path.exists(local_result_file):
  shutil.move(local_result_file, args.output_path)
else:
  raise Exception("Invalid output produced from 4D Humans model")
