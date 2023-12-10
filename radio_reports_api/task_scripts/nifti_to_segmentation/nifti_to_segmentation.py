from shutil import copy2
import os


sh_script_path = os.path.join(os.path.dirname(__file__), "run_total_segmentator.sh")
sh_script_nii_image_path = os.path.join(os.path.dirname(__file__), "vol.nii.gz")
sh_script_out_path = os.path.join(os.path.dirname(__file__), "seg.nii.gz")

dummy_seg = "D:/Programming/Hackathons/Pragati/Stage 3/segmenting/1-tsoc.nii.gz"

def run_total_segmentator_on_nii_image(nii_image_path, ts_out_file_path):
    # copy2(nii_image_path, sh_script_nii_image_path)
    # os.system(f"bash {sh_script_path}")
    # copy2(sh_script_out_path, ts_out_file_path)

    copy2(dummy_seg, ts_out_file_path)
