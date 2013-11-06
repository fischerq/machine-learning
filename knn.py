from distances import euclidean


class SortedList:
    def __init__(self):
        self.list = []
        self.comparison = lambda x, y: x > y

    def insert(self, key, data):
        for i in range(len(self.list)):
            key_it, _ = self.list[i]
            if self.comparison(key, key_it):
                self.list.insert(i, (key, data))
                return
        self.list.insert(len(self.list), (key, data))

    def insert_pop(self, key, data):
        for i in range(len(self.list)):
            if i == len(self.list)-1:
                self.list[i] = (key, data)
            else:
                key_it, _ = self.list[i+1]
                if self.comparison(key, key_it):
                    self.list[i] = (key, data)
                    break
                else:
                    self.list[i] = self.list[i+1]
        #print [k for k, _ in self.list]

    def __len__(self):
        return len(self.list)

    def __getitem__(self, k):
        return self.list[k]

    def top(self):
        return self.list[-1]

    def back(self):
        return self.list[0]


class KNN:
    def __init__(self, samples, k):
        self.samples = samples
        self.k = k
        self.distance_metric = euclidean

    def get_neighbours(self, query):
        neighbours = SortedList()
        for sample in self.samples:
            distance = self.distance_metric(query, sample)
            if len(neighbours) < self.k:
                neighbours.insert(distance, sample)
            elif distance < neighbours.back()[0]:
                neighbours.insert_pop(distance, sample)
            else:
                continue
        return neighbours


class KNNClassification:
    def __init__(self, samples, k):
        self.knn = KNN(samples, k)

    def classify(self, query):
        neighbours = self.knn.get_neighbours(query)
        votes = dict()
        for _, sample in neighbours:
            if sample.classification in votes:
                votes[sample.classification] += 1
            else:
                votes[sample.classification] = 1
        max_votes = 0
        max_classification = None
        for votes, classification in votes.iteritems():
            if votes > max_votes:
                max_classification = classification
                max_votes = votes
        return max_classification


class KNNRegression:
    def __init__(self, samples, k, target_feature):
        self.knn = KNN(samples, k)
        self.target_feature = target_feature

    def estimate(self, query):
        neighbours = self.knn.get_neighbours(query)
        result = 0
        normalization_factor = 0
        if len(neighbours) == 0:
            print "Bad: found no neighbours"
        for distance, sample in neighbours:
            normalization_factor += 1/distance
            result += 1/distance * sample.feature(self.target_feature)
        return result / normalization_factor