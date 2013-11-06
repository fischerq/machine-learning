class Split:
    def __init__(self, feature, value):
        self.feature = feature
        self.value = value

    def check(self, sample):
        return sample.feature(self.feature) <= self.value

    def separate(self, samples):
        samples_left = []
        samples_right = []
        for sample in samples:
            if self.check(sample):
                samples_left.append(sample)
            else:
                samples_right.append(sample)
        return samples_left, samples_right


def gini_index(distribution):
    total = 0
    for count in distribution:
        total += count

    if total == 0:
        return 0

    result = 1
    for count in distribution:
        result -= (float(count)/total)*(float(count)/total)
    return result


MAX_DEPTH = 2


class TreeBuilder:
    def __init__(self, samples):
        self.samples = samples
        self.impurity_measure = gini_index
        self.classifications = dict()
        for sample in self.samples:
            if sample.classification not in self.classifications:
                self.classifications[sample.classification] = len(self.classifications)
        print self.classifications

    def build(self):
        tree = DecisionTree()
        tree.root = self.greedy_split(self.samples, 0)
        return tree

    def greedy_split(self, samples, depth):
        if depth < MAX_DEPTH:
            current_score = self.impurity_measure(self.determine_distribution(samples))
            print "current score {}".format(current_score)
            split, score = self.find_split(samples)
            if score < current_score:
                print "split {}<={}, score {}".format(split.feature, split.value, score)
                samples_left, samples_right = split.separate(samples)
                return DecisionBranch(split,
                                      self.greedy_split(samples_left, depth+1),
                                      self.greedy_split(samples_right, depth+1))

        distribution = self.determine_distribution(samples)
        print "Leaf with dist. {}".format(distribution)
        classification_probabilities = dict()
        for classification, index in self.classifications.iteritems():
            classification_probabilities[classification] = float(distribution[index])/len(samples)
        return DecisionLeaf(classification_probabilities)

    @staticmethod
    def possible_splits(samples):
        features = samples[0].features.keys()
        for feature in features:
            for sample in samples:
                yield Split(feature, sample.feature(feature))

    def determine_distribution(self, samples):
        distribution = []
        for _ in self.classifications:
            distribution.append(0)
        for sample in samples:
            distribution[self.classifications[sample.classification]] += 1
        return distribution

    def find_split(self, samples):
        best_score = float("inf")
        best_split = None
        for split in TreeBuilder.possible_splits(samples):
            samples_left, samples_right = split.separate(samples)
            score = float(len(samples_left))/len(samples) * self.impurity_measure(self.determine_distribution(samples_left)) +\
                    float(len(samples_right))/len(samples) * self.impurity_measure(self.determine_distribution(samples_right))
            if score < best_score:
                best_split = split
                best_score = score
        if best_split is None:
            print "Warning: found no split"
        return best_split, best_score


class DecisionNode:
    def __init__(self):
        print "bad"

    def classify(self, sample):
        print "bad"

    def to_string(self):
        print "bad"


class DecisionBranch(DecisionNode):
    def __init__(self, split, left, right):
        self.split = split
        self.branch_left = left
        self.branch_right = right

    def classify(self, sample):
        if self.split.check(sample):
            return self.branch_left.classify(sample)
        else:
            return self.branch_right.classify(sample)

    def to_string(self):
        return "{} <= {}:\nL: {}\nR: {}".format(self.split.feature,self.split.value,\
               self.branch_left.to_string(),self.branch_right.to_string())


class DecisionLeaf(DecisionNode):
    def __init__(self, probabilities):
        self.probabilities = probabilities
        self.classification = None
        max_probability = 0
        for classification, probability in probabilities.iteritems():
            if probability > max_probability:
                self.classification = classification
                max_probability = probability

    def classify(self, sample):
        return self.classification, self.probabilities

    def to_string(self):
        return "{}, {}".format(self.classification, self.probabilities)


class DecisionTree:
    def __init__(self):
        self.root = None

    def classify(self, sample):
        return self.root.classify(sample)

    def to_string(self):
        return self.root.to_string()