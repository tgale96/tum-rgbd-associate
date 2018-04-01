from __future__ import print_function

import argparse as ap
import h5py as h5
import numpy as np
import quat_util as quat

if __name__ == "__main__":
    p = ap.ArgumentParser()

    p.add_argument("--h5_file", help="hdf5 file name")
    args = p.parse_args()

    f = h5.File(args.h5_file, "a")

    for dataset in f:
        poses = np.array(f[dataset + "/pose"])
        poses = poses.astype(np.float32)

        poses_diff = []
        for i in range(1, len(poses)):
            
            p_pose = poses[i-1, :]
            p_x, p_y, p_z = p_pose[0], p_pose[1], p_pose[2]
            p_w, p_p, p_q, p_r = p_pose[3], p_pose[4], p_pose[5], p_pose[6]

            pose = poses[i, :]
            x, y, z = pose[0], pose[1], pose[2]
            w, p, q, r = pose[3], pose[4], pose[5], pose[6]

            # diff * q1 == q2
            # diff = q2 * inv(q1)
            # OR
            # q1 * diff = q2
            # diff = inv(q1) * q2
            # second one is q1 -> q2
            #
            # Calculate diff = inv(prev) * cur
            i_w, i_p, i_q, i_r = quat.inv(p_w, p_p, p_q, p_r)
            n_w, n_p, n_q, n_r = quat.mult(i_w, i_p, i_q, i_r, w, p, q, r)

            # Calculate translation difference
            n_x, n_y, n_z = x - p_x, y - p_y, z - p_z

            poses_diff.append([n_x, n_y, n_z, n_w, n_p, n_q, n_r])

        poses_diff = np.array(poses_diff)
        if not dataset + "/pose_diff" in f:
            _ = f.create_dataset(dataset + "/pose_diff", data=poses_diff,
                                 chunks=True, compression='gzip', compression_opts=4)
        else:
            print("pose_diff already exits.")
            exit()
    f.close()
