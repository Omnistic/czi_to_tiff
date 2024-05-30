import filecmp
import numpy as np
import os
import tifffile as tiff
import xml.etree.ElementTree as ET
from bioio import BioImage

TIFF_EXTENSIONS = (".tif", ".tiff")

def extract_barcode(metadata):
    barcode_element = metadata.find("Metadata/AttachmentInfos/AttachmentInfo/Label/Barcodes/Barcode/Content")

    if barcode_element is None:
        barcode = None
    else:
        barcode = barcode_element.text.split(" ")[-1]

    return barcode

def extract_timestamp(metadata):
    timestamp_element = metadata.find("Metadata/Information/Image/AcquisitionDateAndTime")

    if timestamp_element is None:
        timestamp = None
    else:
        timestamp = timestamp_element.text

    return timestamp

def czi_to_tiff(czi_path, destination_folder):
    img = BioImage(czi_path)

    print(extract_barcode(img.metadata))
    print(extract_timestamp(img.metadata))

    prefix = "Image_H(0)_"

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for scene_id, scene in enumerate(img.scenes):
        img.set_scene(scene)

        for time_point in range(img.dims.T):
            for z_slice in range(img.dims.Z):
                for channel in range(img.dims.C):
                    filename = destination_folder + prefix + f"S{scene_id:04d}({scene})_T{time_point:06d}_Z{z_slice:04d}_C{channel:02d}_M0000_ORG.tif"
                    tiff.imwrite(filename, img.get_image_data("YX", T=time_point, Z=z_slice, C=channel))

def tiffs_filenames_in_folder(folder):
    tiffs_filenames = []

    for file in os.listdir(folder):
        if file.lower().endswith(TIFF_EXTENSIONS):
            tiffs_filenames.append(file)
    return tiffs_filenames

if __name__ == "__main__":
    tiffs_folder_from_CD7 = "//scopem-staff.ethz.ch/staff/Nguyen.David/work/240207_NA_5-unprocessed-202402071603/"

    czi_path = "//scopem-staff.ethz.ch/staff/Nguyen.David/work/240207_NA_5-unprocessed-202402071603.czi"
    destination_folder = "//scopem-staff.ethz.ch/staff/Nguyen.David/work/extracted_tiffs/"

    czi_to_tiff(czi_path, destination_folder)

    print("TIFFs folder from CD7:  ", tiffs_folder_from_CD7)
    print("Extracted TIFFs folder: ", destination_folder)
    print("Filenames are the same: ", tiffs_filenames_in_folder(tiffs_folder_from_CD7) == tiffs_filenames_in_folder(destination_folder))

    # error = 0

    # for file in tiffs_filenames_in_folder(tiffs_folder_from_CD7):
    #     tiff_from_cd7 = tiff.imread(tiffs_folder_from_CD7 + file)
    #     tiff_extracted = tiff.imread(destination_folder + file)
    #     error += np.amax(np.abs(tiff_from_cd7 - tiff_extracted))

    # print("Total difference across all files in folders: ", error)