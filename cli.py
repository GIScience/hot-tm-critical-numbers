import click
import json
from critical_numbers import app
from critical_numbers.logic import api_requests, converter


@click.group()
def cli():
    pass


@cli.command('serve')
def serve():
    '''serves webapp to 127.0.0.1:5000'''
    app.run()


@cli.command('getall')
def getall():
    '''gets all projects from the HOT Tasking Manager as GeoJSON'''
    hot_tm_projects = api_requests.get_stats()
    hot_tm_projects = converter.convert_to_geojson(hot_tm_projects)
    with open('hot-tm-projects.geojson', 'w') as f:
         json.dump(hot_tm_projects, f)
         click.echo('GeoJSON of all hot-tm projects succsesfully written to "hot-tm-projects.geojson"')


if __name__ == '__main__':
    cli()
