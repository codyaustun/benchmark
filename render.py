import os
import json
from glob import glob

import click
from jinja2 import Template


@click.command()
@click.argument('task')
@click.argument('metric')
@click.option('--dest')
@click.option('--html-dir', '-h', default='leaderboard')
@click.option('--results-dir', '-r', default='results')
@click.option('--templates-dir', '-t', default='templates')
@click.option('--key', '-k', default='time')
@click.option('--limit', '-l', default=10)
def render(task, metric, dest, html_dir, results_dir, templates_dir, key,
           limit):

    source = os.path.join(results_dir, task, metric)
    template = os.path.join(templates_dir, task, f"{metric}.html")
    dest = dest or os.path.join(html_dir, task, f"{metric}.html")

    print(f"Source: {source}")
    print(f"Template: {template}")
    print(f"Output: {dest}")

    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest))

    paths = glob(os.path.join(source, "*.json"))
    print("Found {} submissions".format(len(paths)))
    submissions = []
    for path in paths:
        with open(path) as file:
            record = json.load(file)
            submissions.append(record)

    submissions = sorted(submissions, key=lambda sub: sub[key])
    submissions = submissions[:limit]
    for index, submission in enumerate(submissions):
        submission['rank'] = index + 1

    with open(template, mode='r') as file:
        template = Template(file.read())

    rendered = template.render(submissions=submissions)
    with open(dest, 'w') as file:
        file.write(rendered)


if __name__ == '__main__':
    render()
