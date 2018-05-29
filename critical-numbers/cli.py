# Author: M. Schaub, 2018, GIScience Heidelberg 
import logic
import click
import webapp
from shutil import rmtree


@click.group()
def cli():
    pass


@cli.command('new')
def new():
    '''Creates a new analysis. Removes previous one.'''
    rmtree('output')
    click.echo('Old analysis discontinued (removed output folder). New analysis can be started.')


@cli.command('add')
@click.option('--projectid', '-i', default=(4222, 4212), multiple=True, type=int,
              help='takes a projectId as input. Multiple parameters are\
                    supported. E.g. <-i 4222 -i 4212>')
def add(projectid):
    '''Adds statistical data of HOT Takas Manager Projects\
       to your current analysis. (Makes API requests)'''


@cli.command('visualize')
def visualize():
    '''Visualizes current analysis as a bar chart.'''
    click.echo(visualizer.visualize(get_data.get_data_from_disk()))


@cli.command('export')
@click.option('--fileformat', '-f', default=None, help='Specify disired fileformat. Supported fileformates: csv, wkt, geojson)')
def export(fileformat):
    '''Exports current analysis to disired fileformat.'''
    exporter.export(fileformat)


@cli.command('serve')
#@click.option('--production', '-p', is_flag=True)
def serve():
   webapp.serve()


if __name__ == '__main__':
    cli()
