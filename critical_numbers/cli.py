# Author: M. Schaub, 2018, GIScience Heidelberg 
import logic
import click
import webapp


@click.group()
def cli():
    pass


@cli.command('new')
def new():
    '''Creates a new analysis. Removes previous one.'''
    remover.removes()


@cli.command('add')
@click.option('--projectid', '-i', default=(4222, 4212), multiple=True, type=int,
              help='takes a projectId as input. Multiple parameters are\
                    supported. E.g. <-i 4222 -i 4212>')
def add(projectid):
    '''Adds statistical data of HOT Takas Manager Projects\
       to your current analysis. (Makes API requests)'''
    click.echo(api_requests.add(projectid))


@cli.command('delete')
@click.option('--projectid', '-i', multiple=True, type=int,
              help='Takes a projectId as input.\
                    Multiple parameters are supported. E.g. <-i 4222 -i 4212>')
def delete(projectid):
    '''Deletes projects from your current analysis.'''
    click.echo(get_data.delete(projectid))


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
