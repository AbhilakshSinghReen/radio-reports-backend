from shutil import copy2
import os
import nibabel as nib
import numpy as np
import json
import platform
import subprocess

from radio_reports.settings import SLICER_EXE_PATH

convertor_script_path = os.path.join(os.path.dirname(__file__), "seg_to_mesh.py")
convertor_script_input_path = os.path.join(os.path.dirname(__file__), "seg.nii.gz")
convertor_script_out_path = os.path.join(os.path.dirname(__file__), "model.gltf")

current_os = platform.system()
if current_os == "Windows":
    run_convertor_script_cmd = f""" "{SLICER_EXE_PATH}" --python-script "{convertor_script_path}" --no-splash --no-main-window """
else:
    run_convertor_script_cmd = f""" "{SLICER_EXE_PATH}" --no-splash --no-main-window --python-script "{convertor_script_path}" """

segments_json_path = os.path.join(os.path.dirname(__file__), "segments.json")

segment_value_to_name = {}
segment_names = []
with open(segments_json_path, 'r') as file:
    data = json.load(file)
    segment_value_to_name = {int(key): value for key, value in data.items()}
    segment_names = [value for key, value in data.items()]

def get_average_index_of_value(volume_data, value):
    val_indices = np.where(volume_data == value)
    val_average_index = np.mean(val_indices, axis=1)
    return val_average_index.tolist()

def get_output_metadata(ts_out_file_path):
    nifti_image = nib.load(ts_out_file_path)
    voxel_spacing = nifti_image.header.get_zooms()
    volume_affine = nifti_image.affine
    volume_data = nifti_image.get_fdata()

    output_metadata = {
        'input_volume': {
            'shape': volume_data.shape,
            # 'voxel_spacing': voxel_spacing,
            # 'affine': volume_affine.tolist(),
        },
        'meshes': [],
    }

    segment_values = np.unique(volume_data)
    for segment_value in segment_values:
        if int(segment_value) == 0: # background
            continue

        segment_name = segment_value_to_name.get(int(segment_value), None)
        if segment_name is None:
            # print(f"No name found for segment value {segment_value}. Skipping this segment...")
            continue

        segment_geometric_origin = get_average_index_of_value(volume_data, segment_value)

        output_metadata['meshes'].append({
            'name': f"{segment_name}",
            'geometricOrigin': json.dumps(segment_geometric_origin),
        })

    # for key in output_metadata['input_volume']:
    #     print(key, type(output_metadata['input_volume'][key]))

    # for key in output_metadata['meshes'][0]:
    #     print(key, type(output_metadata['meshes'][0][key]))
    
    return output_metadata

def total_segmentator_output_to_gltf(ts_out_file_path, model_out_path):
    print(run_convertor_script_cmd)

    copy2(ts_out_file_path, convertor_script_input_path)
    # exit_code = os.system(run_convertor_script_cmd)
    subprocess.run([
        SLICER_EXE_PATH,
        "--python-script",
        convertor_script_path,
        "--no-splash",
        "--no-main-window"
    ])
    # print(exit_code)
    print("------------------> Script completed")
    copy2(convertor_script_out_path, model_out_path)

   

    output_metadata = get_output_metadata(ts_out_file_path)
    return output_metadata
