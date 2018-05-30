# Critical Numbers

A GIScience Heidelberg project for the HOT Tasking Manager.


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
    - Website
- flask-wtf
    - Website form handlich
- flask-bootstrap
    - Website style
- folium
    - Python data, leaflet.js maps
- gunicorn
    - serve the website in production

Install requirements via setup.py (See Installtion Steps).


### Installation Steps

- Clone repository
    - `git clone https://github.com/GIScience/hot-tm-critical-numbers.git`
- Change to CriticalNumbers directory
    - `cd hot-tm-critical-numbers/`
- Create and activate virtual environment
    - `python3 -m venv venv` (or use `virtualenv -p python3.6 venv`)
    - `source venv/bin/activate`
- Install via setup.py
    - `pip install .`


## Usage

Run `python -m cli serve` to serve the website on port 5000.
Until fixed the server will listen to `127.0.0.1:5000/critical_numbers/`.


## Deployment

For deployment you should not use the build in web server of Flask (eg. `flask.run()` which `cli serve` is relying upon).

Recommend deployment stack for this application is:
- Gunicorn (Application runner)
- Nginx Reverse Proxy

See official docs for more information: http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/

Or have a look at following tutorials: 
- http://exploreflask.com/en/latest/deployment.html
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux


### Setting Up Gunicorn and Supervisor

#### Gunicorn

Gunicorn is a pure Python web server (robust production server).

`gunicorn -b 127.0.0.1:5000 -w 4 webapp:app`

- `-b`: option tells gunicorn where to listen for requests
- `-w`: option configures how many workers gunicorn will run
- `name_of_app_to_run:app`


#### Supervisor

The supervisor utility uses configuration files that tell it what programs to monitor and how to restart them when necessary. Configuration files must be stored in `/etc/supervisor/conf.d`.
Here is the configuration file for hot-tm-critical-numbers (`hot-tm-critical-numbers.conf`).

```
[program:hot-tm-critical-numbers]
command=/data/hot-tm-critical-numbers/venv/bin/gunicorn -b 127.0.0.1:5000 -w 4 webapp:app
directory=/data/hot-tm-critical-numbers/critical-numbers
user=username
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/hot-tm-critical-numbers/out.log
stdout_logfile=/var/log/hot-tm-critical-numbers/err.log
```

Logs can be viewed at `/var/log/hot-tm-critical-numbers/`.

To run or rerun supervisor and configured programs (e.g. hot-tm-critical-numbers) it is enough to run `supervisorctl reload`.

Following commands could be also be useful:
- `supervisorctl start hot-tm-critical-numbers`
- `supervisorctl stop hot-tm-critical-numbers`
- `supervisorctl reread`
- `supervisorctl update`
