# DAWNBench Submission Instructions

Thanks for the interest in DAWNBench!

To add your model to our leaderboard, open a Pull Request to this repository,
with JSON files in the format outlined below.

For the training tasks, use the following format:
```JSON
{
    "author": "Stanford DAWN",
    "framework": "TensorFlow",
    "codeURL": "https://github.com/stanford-futuredata/dawn-benchmark/tree/master/tensorflow",
    "model": "ResNet 56",
    "hardware": "1 K80 / 30 GB / 8 CPU (Google Cloud)",
    "trainingTime": 4.829735400478046,
    "accuracy": 93.17,
    "cost": 4.67035413226227,
    "timestamp": "11 August, 2017"
}
```

For the inference tasks, use the following format:
```JSON
{
    "author": "Stanford DAWN",
    "framework": "TensorFlow",
    "codeURL": "https://github.com/stanford-futuredata/dawn-benchmark/tree/master/tensorflow",
    "model": "ResNet 56",
    "hardware": "1 K80 / 30 GB / 8 CPU (Google Cloud)",
    "latency": 43.45,
    "batchThroughput": 9289.245702363134,
    "accuracy": 93.45,
    "timestamp": "11 August, 2017"
}
```

JSON files are named using the format
`[author name]_[model name]_[hardware]_[framework].json` similar to
`dawn_resnet56_1k80_gc_tensorflow.json`. Each dataset (`CIFAR10` and `SQuAD`)
has their own `train/` and `inference/` sub-directories.
