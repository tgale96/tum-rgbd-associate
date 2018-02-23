import numpy as np

def check_consistent(matches):
    if len(matches) < 2:
        return

    a_inc = []
    b_inc = []
    (prev_a, prev_b) = matches[0]
    for i in range(1, len(matches)):
        (a, b) = matches[i]
        if a < prev_a:
            a_inc.append(i)
        if b < prev_b:
            b_inc.append(i)

        prev_a = a
        prev_b = b

    print("{} inconsistencies in a".format(len(a_inc)))
    print("{} inconsistencies in b".format(len(b_inc)))

def check_consistent_3(matches):
    if len(matches) < 2:
        return

    a_inc = []
    b_inc = []
    c_inc = []
    (prev_a, prev_b, prev_c) = matches[0]
    for i in range(1, len(matches)):
        (a, b, c) = matches[i]
        if a < prev_a:
            a_inc.append(i)
        if b < prev_b:
            b_inc.append(i)
        if c < prev_c:
            c_inc.append(i)

        prev_a = a
        prev_b = b
        prev_c = c

    print("{} inconsistencies in a".format(len(a_inc)))
    print("{} inconsistencies in b".format(len(b_inc)))
    print("{} inconsistencies in c".format(len(c_inc)))
    
def tstamp_stats(matches):
    diffs = np.array(map(lambda (x,y): abs(x-y), matches))
    mean = np.mean(diffs)
    std = np.std(diffs)
    maximum = diffs.max()
    minimum = diffs.min()

    print("num/mean/std/max/min deviation: {} / {} / {} / {} / {}"
          .format(len(matches), mean, std, maximum, minimum))
    

def tstamp_stats_3(matches):
    diffs = np.array(map(lambda (x,y,z): (abs(x-y)+abs(x-z)+abs(y-z))/3.0, matches))
    mean = np.mean(diffs)
    std = np.std(diffs)
    maximum = diffs.max()
    minimum = diffs.min()

    print("num/mean/std/max/min deviation: {} / {} / {} / {} / {}"
          .format(len(matches), mean, std, maximum, minimum))
    
