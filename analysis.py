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

def tstamp_stats(matches):
    diffs = np.array(map(lambda (x,y): abs(x-y), matches))
    mean = np.mean(diffs)
    std = np.std(diffs)
    maximum = diffs.max()
    minimum = diffs.min()

    print("num/mean/std/max/min deviation: {} / {} / {} / {} / {}"
          .format(len(matches), mean, std, maximum, minimum))
    
