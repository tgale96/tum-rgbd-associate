# Software License Agreement (BSD License)
#
# Copyright (c) 2013, Juergen Sturm, TUM
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of TUM nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import argparse

from analysis import check_consistent
from analysis import tstamp_stats
from read_data import read_data

def associate(first_list, second_list, offset, max_diff):
    """
    Associate two dictionaries of (stamp,data). As the time stamps never match exactly, 
    we aim to find the closest match for every input tuple.
    
    Input:
    first_list -- first dictionary of (stamp,data) tuples
    second_list -- second dictionary of (stamp,data) tuples
    offset -- time offset between both dictionaries (e.g., to model the delay between the sensors)
    max_diff -- search radius for candidate generation

    Output:
    matches -- list of matched tuples ((stamp1,data1),(stamp2,data2))"""

    # We need the keys to be sorted for this to work
    first_keys = first_list.keys()
    second_keys = second_list.keys()
    first_keys.sort()
    second_keys.sort()

    matches = []
    b_idx = 0
    for a_idx in range(0, len(first_keys)):
        # exit if we go out of range
        if b_idx >= len(second_keys):
            break
        
        a_val = first_keys[a_idx]
        while second_keys[b_idx] < a_val:
            b_idx += 1

        diff1 = abs(second_keys[b_idx] - a_val)
        diff2 = abs(second_keys[b_idx-1] - a_val)
        if diff1 < diff2 and diff1 <= max_diff:
            matches.append((a_val, second_keys[b_idx]))
            b_idx += 2
        elif diff2 <= diff1 and diff2 <= max_diff:
            matches.append((a_val, second_keys[b_idx-1]))
            b_idx += 1

    return matches
        
if __name__ == '__main__':    
    parser = argparse.ArgumentParser(description=
                                     """This script takes two data 
                                     files with timestamps and 
                                     associates them""")
    
    parser.add_argument('first_file',
                        help='first text file (format: timestamp data)')
    parser.add_argument('second_file',
                        help='second text file (format: timestamp data)')
    parser.add_argument('--first_only',
                        help='only output associated lines from first file',
                        action='store_true')
    parser.add_argument('--offset',
                        help="""time offset added to the timestamps of the 
                        second file (default: 0.0)""", default=0.0)
    parser.add_argument('--max_difference',
                        help="""maximally allowed time difference for matching 
                        entries (default: 0.02)""", default=0.02)
    args = parser.parse_args()

    first_list = read_data(args.first_file)
    second_list = read_data(args.second_file)

    matches = associate(first_list, second_list, float(args.offset), float(args.max_difference))    

    # Check for inconsistencies. Algorithm should guarantee 0
    check_consistent(matches)
    tstamp_stats(matches)

    f1 = open(args.first_file + ".assoc", "w+")
    f2 = open(args.second_file + ".assoc", "w+")
    for a,b in matches:
        f1.write("{} {}\n".format(a, " ".join(first_list[a])))
        f2.write("{} {}\n".format(b, " ".join(second_list[b])))

    # if args.first_only:
    #     for a,b in matches:
    #         print("%f %s"%(a, "".join(first_list[a])))
    # else:
    #     for a,b in matches:
    #         print("%f %s %f %s"%(a," ".join(first_list[a]),b-float(args.offset)," ".join(second_list[b])))
            
        
