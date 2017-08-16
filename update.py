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


def load_submissions(directory, task, mode):
    source = os.path.join(directory, task, mode)
    print("Results from " + source)

    paths = glob(os.path.join(source, "*.json"))
    print("Found {} submissions".format(len(paths)))
    records = []
    for path in paths:
        with open(path) as file:
            record = json.load(file)
            timestamp = datetime.strptime(record['timestamp'], '%Y-%m-%d')
            record['timestamp'] = timestamp.strftime('%b %Y')
            records.append(record)
    return records


def filter_and_rank(submissions, task, metric, limit=10, reverse=False):
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

    return submissions


@click.command()
@click.argument('results_dir')
@click.option('--html-dir', '-h', default='src/html')
@click.option('--templates-dir', '-t', default='src/templates')
@click.option('--limit', '-l', default=3)
def update(results_dir, html_dir, templates_dir, limit):
    print("Templates: " + templates_dir)
    print("Output: " + html_dir)
    env = Environment(loader=loaders.FileSystemLoader(templates_dir))

    # Could use TASK_THRESHOLD.keys()
    for task in ['CIFAR10', 'SQuAD']:
        submissions = {}
        # Could use KEY_MAP.keys()
        train = load_submissions(results_dir, task, 'train')
        inference = load_submissions(results_dir, task, 'inference')
        for metric in ['time', 'cost', 'latency', 'throughput']:

            records = train if metric in ['time', 'cost'] else inference
            records = [record.copy() for record in records]
            submissions[metric + '_submissions'] = filter_and_rank(
                records, task, metric, limit=limit,
                reverse=(metric == 'throughput'))

        print('Render ' + task + ' Index Page')
        index = env.get_template(task + '/index.html')
        with open(os.path.join(html_dir, task + '.html'), 'w') as file:
            file.write(index.render(task=task, **submissions))

        print('Render ' + task + ' Training Table')
        train_table = env.get_template(task + '/train.html')
        with open(os.path.join(html_dir, task, 'train.html'), 'w') as file:
            file.write(train_table.render(task=task, submissions=train))

        print('Render ' + task + ' Inference Table')
        infer_table = env.get_template(task + '/inference.html')
        with open(os.path.join(html_dir, task, 'inference.html'), 'w') as file:
            file.write(infer_table.render(task=task, submissions=inference))


if __name__ == '__main__':
    update()
