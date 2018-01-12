# -*- encoding: utf-8 -*-
# ! python3

import shutil

from invoke import task, run


@task
def publish(ctx):
    shutil.rmtree('./published', ignore_errors=True)

    ctx.run("gulp js --production")
    ctx.run("gulp less --production")
    ctx.run("pelican -s publishconf.py -o published")
    ctx.run("gulp minify")


@task
def content(ctx):
    ctx.run("pelican content --autoreload")


@task
def server(ctx):
    ctx.run("python -m pelican.server")
