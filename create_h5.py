import argparse as ap
import cv2
import h5py as h5
import numpy as np

def img_stats(t):
    t = np.array(t)
    print("max, min, mean, std: {} / {} / {} / {}"
          .format(t.max(), t.min(), np.mean(t), np.std(t)))

def concat_to_array(data):
    tmp = [np.reshape(a, (1,) + a.shape) for a in data]
    return np.concatenate(tmp)

def read_images(dirname, fname):
    results = []
    with open(dirname + "/" + fname, 'r') as file:
        for line in file:
            # ignore comments
            if line[0] == '#':
                continue
            img_name = line.split()[1]

            img = cv2.imread(dirname + "/" + img_name, -1)

            results.append(img)
    return concat_to_array(results)

def read_pose(fpath):
    poses = []
    with open(fpath, 'r') as file:
        for line in file:
            # ignore comments
            if line[0] == '#':
                continue
            pose = np.array(line.split()[1:])
            poses.append(pose)
    return concat_to_array(poses)

if __name__ == "__main__":
    p = ap.ArgumentParser(description="""Insert a dataset of rgb, 
    depth, and pose samples into the given hdf5 file""")

    p.add_argument("--h5_file", help="hdf5 file name")
    p.add_argument("--data_dir", help="directory containing data to add")
    args = p.parse_args()

    f = h5.File(args.h5_file, "a")
    if args.data_dir in f:
        print("Dataset already exists in specified file.")
        exit(0)
        
    # Read in all rgb, depth, and pose samples
    rgb_imgs = read_images(args.data_dir, "rgb.txt.assoc")
    depth_imgs = read_images(args.data_dir, "depth.txt.assoc")
    poses = read_pose(args.data_dir + "/groundtruth.txt.assoc")
    
    # create the dataset
    rgb_dset = f.create_dataset(args.data_dir + "/rgb", data=rgb_imgs,
                                chunks=True, compression='gzip', compression_opts=4)
    depth_dset = f.create_dataset(args.data_dir + "/depth", data=depth_imgs,
                                  chunks=True, compression='gzip', compression_opts=4)
    pose_dset = f.create_dataset(args.data_dir + "/pose", data=poses,
                                 chunks=True, compression='gzip', compression_opts=4)
    f.close()
