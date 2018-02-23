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
from numba import jit

from analysis import check_consistent_3
from analysis import tstamp_stats_3
from read_data import read_data

@jit(nopython=True)
def associate(a_keys, b_keys, c_keys, max_diff):
    """
    Associate three dictionaries of times stamps
    
    Input:
    a_keys -- first list of keys
    b_keys -- second list of keys
    c_keys -- third list of keys
    max_diff -- search radius for candidate generation

    Output:
    matches -- list of matched tuples (tstamp1, tstamp2, tstamp3)"""

    diffs = []
    for a in a_keys:
        for b in b_keys:
            for c in c_keys:
                ab_diff = abs(a-b)
                ac_diff = abs(a-c)
                bc_diff = abs(b-c)
                total_diff = abs(a-b) + abs(a-c) + abs(b-c)
                if (total_diff / 3.0) < max_diff:
                    diffs.append((total_diff, a, b, c))

    # sort the triplet candidates by total difference
    diffs.sort()

    # Note that we assume there are no matching
    # timesteps within each set of timestamps
    matches = []
    a_used = set()
    b_used = set()
    c_used = set()

    def check_free(a, b, c):
        if not a in a_used:
            if not b in b_used:
                if not c in c_used:
                    return True
        return False
    
    for diff, a, b, c in diffs:
        if check_free(a, b, c):
            matches.append((a, b, c))
            a_used.add(a)
            b_used.add(b)
            c_used.add(c)

    matches.sort()
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
    parser.add_argument('third_file',
                        help='second text file (format: timestamp data)')
    parser.add_argument('--max_difference',
                        help="""maximally allowed time difference for matching 
                        entries (default: 0.02)""", default=0.02)
    args = parser.parse_args()

    a_list = read_data(args.first_file)
    b_list = read_data(args.second_file)
    c_list = read_data(args.third_file)
    matches = associate(a_list.keys(), b_list.keys(), c_list.keys(), float(args.max_difference))    

    # Check for inconsistencies. Algorithm should guarantee 0
    check_consistent_3(matches)
    tstamp_stats_3(matches)

    f1 = open(args.first_file + ".assoc", "w+")
    f2 = open(args.second_file + ".assoc", "w+")
    f3 = open(args.third_file + ".assoc", "w+")
    for a, b, c in matches:
        f1.write("{} {}\n".format(a, " ".join(a_list[a])))
        f2.write("{} {}\n".format(b, " ".join(b_list[b])))
        f3.write("{} {}\n".format(c, " ".join(c_list[c])))
