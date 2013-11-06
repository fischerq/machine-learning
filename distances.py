import math


def euclidean(a, b):
    features = a.features.keys()
    sum = 0
    for f in features:
        if a.feature(f) is None or b.feature(f) is None:
            continue
        sum += (a.feature(f)-b.feature(f))*(a.feature(f)-b.feature(f))
    return math.sqrt(sum)