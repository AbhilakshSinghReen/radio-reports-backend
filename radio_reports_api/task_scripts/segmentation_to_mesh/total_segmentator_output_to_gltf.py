from shutil import copy2
import os


sh_script_path = os.path.join(os.path.dirname(__file__), "run_total_segmentator.sh")
sh_script_input_path = os.path.join(os.path.dirname(__file__), "seg.nii.gz")
sh_script_out_path = os.path.join(os.path.dirname(__file__), "model.gltf")

def total_segmentator_output_to_gltf(ts_out_file_path, model_out_path):
    copy2(ts_out_file_path, sh_script_input_path)
    os.system(f"bash {sh_script_path}")
    copy2(sh_script_out_path, model_out_path)

    # Need to get mesh metadata
    return "Need to implement getting meshes metadata."
