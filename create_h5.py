import argparse as ap
import cv2
import h5py as h5
import numpy as np

def img_stats(t):
    t = np.array(t)
    print("max, min, mean, std: {} / {} / {} / {}"
          .format(t.max(), t.min(), np.mean(t), np.std(t)))
    
def read_images(dirname, fname, jpeg_compress=False):
    with open(dirname + "/" + fname, 'r') as file:
        for line in file:
            # ignore comments
            if line[0] == '#':
                continue
            img_name = line.split()[1]

            img = cv2.imread(dirname + "/" + img_name, -1)

            if jpeg_compress:
                _, img = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
            else:
                _, img = cv2.imencode(".png", img, [cv2.IMWRITE_PNG_COMPRESSION, 9])

            break

    
if __name__ == "__main__":
    p = ap.ArgumentParser(description="""Insert a dataset of rgb, 
    depth, and pose samples into the given hdf5 file""")

    p.add_argument("--h5_file", help="hdf5 file name")
    p.add_argument("--data_dir", help="directory containing data to add")
    args = p.parse_args()

    # Read in the rgb images
    read_images(args.data_dir, "rgb.txt.assoc", jpeg_compress=True)
    read_images(args.data_dir, "depth.txt.assoc", jpeg_compress=False)
