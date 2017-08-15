# DAWNBench Submission Instructions

Thanks for the interest in DAWNBench!

To add your model to our leaderboard, open a Pull Request, with JSON files in the format
outlined below.

## Format

For the training tasks, use the following format:
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

For the inference tasks, use the following format:
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

JSON files are named `[author name]_[model name]_[hardware]_[framework].json`, similar to
`dawn_resnet56_1k80_gc_tensorflow.json`. Each dataset (`CIFAR10` and `SQuAD`)
has its own `train/` and `inference/` sub-directories.

## Fields
We describe each of the fields in the submitted JSON file in more detail here.

- `author`: Author name.
- `authorEmail`: Author email.
- `framework`: Framework on which training / inference was performed.
- `codeURL`: Optional. URL pointing to code for model.
- `model`: Model name.
- `hardware`: A short description of the hardware on which model training / inference was performed.
- `trainingTime`: Training objective. Reported in hours. Time needed to train a model up to
  required accuracy target on test / development dataset.
- `cost`: Training objective. Reported in USD. Cost of training a model up to required accuracy target
  on public cloud infrastructure.
- `latency`: Inference objective. Reported in milliseconds. Time needed to classify one image or answer
  one question.
- `batchThroughput`: Inference objective. Reported in images / second or questions / second. Throughput
  obtained while classifying any 8192 image subset of the CIFAR10 test dataset, or answering all the
  questions in the SQuAD development set.
- `accuracy`: CIFAR10 only. Reported in percentage points from 0 to 100. Accuracy of model on CIFAR10
  test dataset.
- `f1Score`: SQuAD only. Reported in fraction from 0.0 to 1.0. F1 score of model on SQuAD validation
  dataset.
- `timestamp`: Date of submission in format `yyyy-mm-dd`.
- `logFileName`: Optional. URL pointing to training / inference logs.
- `misc`: List of other miscellaenous notes, such as learning rate schedule, optimization algorithm,
  etc.
