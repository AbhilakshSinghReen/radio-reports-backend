from shutil import copy2


def run_total_segmentator_on_nii_image(nii_image_path, ts_out_file_path):
    # TODO (Abhilaksh): Would prefer to run this with os.system since it may be in a different env

    dummy_seg_path = "D:/Programming/Hackathons/Pragati/Stage 3/segmenting/1-tsoc.nii.gz"
    copy2(dummy_seg_path, ts_out_file_path)
