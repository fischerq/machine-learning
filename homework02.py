from utils import *

import samples
import decisiontrees
import knn

filename = "data/homework02.csv"
types = [float, float, float, int]
features = ["x1", "x2", "x3", "z"]
sample_format = samples.ClassifiedSampleFormat(features, types, "z")
samples_classification = parse_csv(filename, sample_format)

builder = decisiontrees.TreeBuilder(samples_classification)
tree = builder.build()

print "Problem 1"
print tree.to_string()

data_a = ["4.1", "-0.1", "2.2", None]
data_b = ["6.1", "0.4", "1.3", None]

x_a = sample_format.parse(data_a)
x_b = sample_format.parse(data_b)

print "Problem 2"
z_a, p_a = tree.classify(x_a)
print "Classified x_a as {}, probabilities {}".format(z_a, p_a)
z_b, p_b = tree.classify(x_b)
print "Classified x_b as {}, probabilities {}".format(z_b, p_b)

knn_classify = knn.KNNClassification(samples_classification, 3)

print "Problem 3"
knn_a = knn_classify.classify(x_a)
print "KNN classified x_a as {}".format(knn_a)
knn_b = knn_classify.classify(x_b)
print "KNN classified x_b as {}".format(knn_b)

regression_format = samples.SampleFormat(features, [float, float, float, float])
samples_regression = parse_csv(filename, regression_format)

knn_regression = knn.KNNRegression(samples_regression, 3, "z")

reg_a = regression_format.parse(data_a)
reg_b = regression_format.parse(data_b)

print "Problem 4"
print "Regression z for a: {}".format(knn_regression.estimate(reg_a))
print "Regression z for b: {}".format(knn_regression.estimate(reg_b))