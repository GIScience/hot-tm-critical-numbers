# Critical Numbers

A GIScience Heidelberg project for the HOT Tasking Manager.

* [Introduction and examples](blog-post.md)


## Installation

### Requirements

\> Python 3.6

Following python packages and their dependences are required:
- click
    - creates beautiful command line interfaces
- requests
    - API Requests
- pygal
    - sexy charts
- geomet
    - GeoJSON to WKT conversion
- flask
    - website
- flask-wtf
    - website forms
- wtfforms
    - form handling
- flask-bootstrap
    - website template
- folium
    - python data, leaflet.js maps
- gunicorn
    - robust production server
- shaply
    - manipulation and analysis of geometric objects

Install requirements via setup.py (See installation steps).


### Installation Steps

- Clone repository
    - `git clone https://github.com/GIScience/hot-tm-critical-numbers.git`
- Change to hot-tm-critical-numbers directory
    - `cd hot-tm-critical-numbers/`
- Create and activate virtual environment
    - `python3 -m venv venv` (or use `virtualenv -p python3.6 venv`)
    - `source venv/bin/activate`
- Install via setup.py
    - `pip install .`


## Usage

- Run `python -m cli --help` to show:

```shell
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  getall  gets all projects from the HOT Tasking...
  serve   serves webapp to 127.0.0.1:5000
```

- Run `python -m cli serve` to serve the website locally on port 5000
    - Until fixed the server will listen to `127.0.0.1:5000/critical_numbers/`
- Run `python -m cli getall` to get all projects from the HOT Tasking Manager as GeoJSON (This could take a while)


## Deployment

For deployment you should not use the build in web server of Flask (eg. `flask.run()` which `cli serve` is relying upon).

Recommend deployment stack for this application is either:
- Gunicorn
- Supervisor

Or use Docker.

See official docs for more information: http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/


### Gunicorn and Supervisor

#### Gunicorn

Gunicorn is a pure Python web server (robust production server).

`gunicorn -b 127.0.0.1:5000 -w 4 -t 300 critical_numbers:app`

- `-b`: option tells gunicorn where to listen for requests
- `-w`: option configures how many workers gunicorn will run
- `-t`: option to set timeout. Should be set to 300s. Has to be configured in ngix also.
- `name_of_app_to_run:app`


#### Supervisor

The supervisor utility uses configuration files that tell it what programs to monitor and how to restart them when necessary. Configuration files are stored at `/etc/supervisor/conf.d/`.
Here is a configuration file for hot-tm-critical-numbers (`hot-tm-critical-numbers.conf`).

```
[program:hot-tm-critical-numbers]
command=/var/www/hot-tm-critical-numbers/venv/bin/gunicorn -b 127.0.0.1:5000 -w 4 -t 300 critical_numbers:app
directory=/var/www/hot-tm-critical-numbers
user=username
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/hot-tm-critical-numbers/out.log
stdout_logfile=/var/log/hot-tm-critical-numbers/err.log
```

Logs can be viewed at `/var/log/hot-tm-critical-numbers/`.

To run or rerun supervisor and configured programs (e.g. hot-tm-critical-numbers) it is enough to run:

```
supervisorctl reload
```

Following commands could be also be useful:
- `supervisorctl start hot-tm-critical-numbers`
- `supervisorctl stop hot-tm-critical-numbers`
- `supervisorctl reread`
- `supervisorctl update`


### Docker

To build a container image use following command inside of hot-tm-critical-numbers folder (where the dockerfile is located):

```
docker build -t critical_numbers .
```

List container images with:

```
docker images
```

To run the container:

```
docker run --name critical_numbers -d -p 5000:5000 --restart always critical_numbers:latest
```

- `d`: run in background (detach)
- `p`: maps container ports to host ports (publish)
- the last argument is the container image name and tag

List running containers with:

```
docker ps
```

To stop the container (use `docker ps` to get the Container Id):

```
docker stop <Container Id>
```

To remove a container:

```
docker rm <image name>
```
