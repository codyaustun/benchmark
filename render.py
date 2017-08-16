import os
import json
from glob import glob
from collections import namedtuple
from datetime import datetime

import click
from jinja2 import Template


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


@click.command()
@click.argument('task')
@click.argument('metric')
@click.option('--dest')
@click.option('--html-dir', '-h', default='leaderboard')
@click.option('--results-dir', '-r', default='results')
@click.option('--templates-dir', '-t', default='src/templates')
@click.option('--limit', '-l', default=10)
@click.option('--reverse', is_flag=True)
def render(task, metric, dest, html_dir, results_dir, templates_dir,
           limit, reverse):

    if metric in ['time', 'cost']:
        mode = 'train'
    elif metric in ['throughput', 'latency']:
        mode = 'inference'
    else:
        raise NotImplementedError('Unknown metric: %s' % metric)

    source = os.path.join(results_dir, task, mode)
    template = os.path.join(templates_dir, task, metric+".html")
    dest = dest or os.path.join(html_dir, task, metric+".html")

    print("Source: "+source)
    print("Template: "+template)
    print("Output: "+dest)

    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))

    # Load
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

    with open(template, mode='r') as file:
        template = Template(file.read())

    rendered = template.render(submissions=submissions)
    with open(dest, 'w') as file:
        file.write(rendered)


if __name__ == '__main__':
    render()
