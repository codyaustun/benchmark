import os
import json
from glob import glob
from collections import namedtuple
from datetime import datetime

import click
from jinja2 import Environment, loaders


KEY_MAP = {
    'time': 'trainingTime',
    'cost': 'cost',
    'latency': 'latency',
    'throughput': 'batchThroughput'
}


Threshold = namedtuple('Threshold', ['field', 'cutoff'])


TASK_THRESHOLDS = {
    'CIFAR10': Threshold('accuracy', 93),
    'SQuAD': Threshold('f1Score', 0.73)
}


NULLS = ['None', 'N/A', 'null']


def load_submissions(directory, task, metric, limit=10, reverse=False):

    if metric in ['time', 'cost']:
        mode = 'train'
    elif metric in ['throughput', 'latency']:
        mode = 'inference'
    else:
        raise NotImplementedError('Unknown metric: %s' % metric)

    source = os.path.join(directory, task, mode)
    print("Task: " + task)
    print("Metric: " + metric)
    print("Results from " + source)

    paths = glob(os.path.join(source, "*.json"))
    print("Found {} submissions".format(len(paths)))
    submissions = []
    for path in paths:
        with open(path) as file:
            record = json.load(file)
            submissions.append(record)

    key = KEY_MAP[metric]
    threshold = TASK_THRESHOLDS[task]

    # Filter
    def filter_submission(submission):
        return ((submission[key] is not None) and
                (submission[key] not in NULLS) and
                (submission[threshold.field] > threshold.cutoff))

    threshold = TASK_THRESHOLDS[task]
    submissions = list(filter(filter_submission, submissions))

    # Rank
    submissions = sorted(submissions, key=lambda sub: sub[key],
                         reverse=reverse)
    submissions = submissions[:limit]
    for index, submission in enumerate(submissions):
        submission['rank'] = index + 1
        timestamp = datetime.strptime(submission['timestamp'], '%Y-%m-%d')
        submission['timestamp'] = timestamp.strftime('%b %Y')

    return submissions


@click.command()
@click.argument('results_dir')
@click.option('--html-dir', '-h', default='src/html')
@click.option('--templates-dir', '-t', default='src/templates')
@click.option('--limit', '-l', default=4)
def update(results_dir, html_dir, templates_dir, limit):
    print("Templates: " + templates_dir)
    print("Output: " + html_dir)
    env = Environment(loader=loaders.FileSystemLoader(templates_dir))

    # Could use TASK_THRESHOLD.keys()
    for task in ['CIFAR10', 'SQuAD']:
        submissions = {}
        # Could use KEY_MAP.keys()
        for metric in ['time', 'cost', 'latency', 'throughput']:

            submissions[metric + '_submissions'] = load_submissions(
                results_dir, task, metric, limit=limit,
                reverse=(metric == 'throughput'))

        print('Render ' + task + 'Index Page')
        index = env.get_template(task + '/index.html')
        with open(os.path.join(html_dir, task + '.html'), 'w') as file:
            file.write(index.render(task=task, **submissions))


if __name__ == '__main__':
    update()
