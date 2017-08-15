# DAWNBench Submission Instructions

Thanks for the interest in DAWNBench!

To add your model to our leaderboard, open a Pull Request, with JSON files in the format
outlined below.

## CIFAR10

### Task Description

We evaluate image classification performance on the [CIFAR10 dataset](https://www.cs.toronto.edu/~kriz/cifar.html).

For training, we have two tasks:
- Training Time: Minimize the total time taken to train a model that has a test set accuracy of
  93% or greater
- Cost: Minimize the total cost of training a model that has a test set accuracy of 93% or greater on
  public cloud infrastructure

For inference, we have two tasks:
- Latency: Minimize the total time needed to classify a single image with a model that has a test
  set accuracy of 93% or greater
- Throughput: Minimize the total time (or maximize the total throughput) needed to classify 8192 images
  in the CIFAR10 test set with a model that has a total test set accuracy of 93% or greater

### JSON Format

Results for the CIFAR10 tasks can be reported using a JSON file with the following fields,

- `author`: Author name
- `authorEmail`: Author email
- `framework`: Framework on which training / inference was performed
- `codeURL`: [Optional] URL pointing to code for model
- `model`: Model name
- `hardware`: A short description of the hardware on which model training / inference was performed
- `trainingTime`: Training objective. Reported in hours. Time needed to train a model up to
  93% test set accuracy
- `cost`: Training objective. Reported in USD ($). Cost of training a model up to 93% test set accuracy
  on public cloud infrastructure
- `latency`: Inference objective. Reported in milliseconds. Time needed to classify one image
- `batchThroughput`: Inference objective. Reported in images / second. Throughput
  obtained while classifying any 8192 image subset of the CIFAR10 test dataset
- `accuracy`: Reported in percentage points from 0 to 100. Accuracy of model on CIFAR10 test dataset.
- `timestamp`: Date of submission in format `yyyy-mm-dd`
- `logFilename`: [Optional] URL pointing to training / inference logs
- `misc`: List of other miscellaenous notes, such as learning rate schedule, optimization algorithm,
  etc.
  
To make this more concrete, consider the following JSON files for training,
```JSON
{
    "author": "Stanford DAWN",
    "authorEmail": "dawn-bench@cs.stanford.edu",
    "framework": "TensorFlow",
    "codeURL": "https://github.com/stanford-futuredata/dawn-benchmark/tree/master/tensorflow",
    "model": "ResNet 56",
    "hardware": "1 K80 / 30 GB / 8 CPU (Google Cloud)",
    "trainingTime": 4.829735400478046,
    "accuracy": 93.17,
    "cost": 4.67035413226227,
    "timestamp": "2017-08-14",
    "misc": []
}
```

And for inference,
```JSON
{
    "author": "Stanford DAWN",
    "authorEmail": "dawn-bench@cs.stanford.edu",
    "framework": "TensorFlow",
    "codeURL": "https://github.com/stanford-futuredata/dawn-benchmark/tree/master/tensorflow",
    "model": "ResNet 56",
    "hardware": "1 K80 / 30 GB / 8 CPU (Google Cloud)",
    "latency": 43.45,
    "batchThroughput": 9289.245702363134,
    "accuracy": 93.45,
    "timestamp": "2017-08-14",
    "misc": []
}
```

### Submission Format

JSON files are named `[author name]_[model name]_[hardware]_[framework].json`, similar to
`dawn_resnet56_1k80_gc_tensorflow.json`. Put the JSON file in the `CIFAR10/train/` or `CIFAR10/inference`
depending on whether the JSON file is reporting training or inference results.

## SQuAD

### Task Description

We evaluate question answering performance on the [SQuAD dataset](https://rajpurkar.github.io/SQuAD-explorer/).

For training, we have two tasks:
- Training Time: Minimize the total time taken to train a model that has a development set F1 score of
  0.73 or greater
- Cost: Minimize the total cost of training a model that has a development set F1 score of 0.73 or greater on
  public cloud infrastructure

For inference, we have two tasks:
- Latency: Minimize the total time needed to answer a single question with a model that has a development
  set F1 score of 0.73 or greater
- Throughput: Minimize the total time (or maximize the total throughput) needed to all questions in the
  SQuAD development set with a model that has a total development set F1 score of 0.73 or greater

### JSON Fields

Results for the CIFAR10 tasks can be reported using a JSON file with the following fields,

- `author`: Author name
- `authorEmail`: Author email
- `framework`: Framework on which training / inference was performed
- `codeURL`: [Optional] URL pointing to code for model
- `model`: Model name
- `hardware`: A short description of the hardware on which model training / inference was performed
- `trainingTime`: Training objective. Reported in hours. Time needed to train a model up to
  0.73 F1 score on the SQuAD development dataset
- `cost`: Training objective. Reported in USD ($). Cost of training a model up to 0.73 F1 score on the
  SQuAD development dataset
- `latency`: Inference objective. Reported in milliseconds. Time needed to answer one question
- `batchThroughput`: Inference objective. Reported in questions / second. Throughput
  obtained while answering all the questions in the SQuAD development set
- `f1Score`: Reported in fraction from 0.0 to 1.0. F1 score of model on SQuAD development dataset
- `timestamp`: Date of submission in format `yyyy-mm-dd`
- `logFilename`: Optional. URL pointing to training / inference logs
- `misc`: List of other miscellaenous notes, such as learning rate schedule, optimization algorithm,
  etc.

### Submission Format

JSON files are named `[author name]_[model name]_[hardware]_[framework].json`, similar to
`dawn_bidaf_1k80_gc_tensorflow.json`. Put the JSON file in the `SQuAD/train/` or `SQuAD/inference`
depending on whether the JSON file is reporting training or inference results.
