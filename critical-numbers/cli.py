# Author: M. Schaub, 2018, GIScience Heidelberg
import click
import webapp


@click.group()
def cli():
    pass


@cli.command('serve')
def serve():
    webapp.serve()


if __name__ == '__main__':
    cli()
