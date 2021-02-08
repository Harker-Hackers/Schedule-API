import flask
from datetimerange import DateTimeRange
from datetime import date
from time import localtime, strftime
import calendar
from json import loads

app = flask.Flask(__name__)

def get_schedule(day=None):
    schedule = loads(
        open(
            'schedule.json',
            'r'
        ).read()
    )
    if day:
        return(schedule[day])
    else:
        return(schedule)

def check_range(block, day, to_verify):
    today = str(date.today())
    block_timings = get_schedule(day)[block]
    start = block_timings['start']
    end = block_timings['end']
    time_range = DateTimeRange(f"{today}T{start}:00+0800", f"{today}T{end}:00+0800")
    return(f"{today}T{to_verify}:00+0800" in time_range)

@app.route('/all')
def all():
    '''
    This endpoint returns the schedule for Monday - Friday.
    Optional parameters: 
        - 'block': Get timings for a time block in each day's schedule.
    '''
    data = loads(
        open(
            'schedule.json', 'r'
        ).read()
    )
    res = {}
    param = flask.request.args.get('block')
    if param != None:
        for day in data:
            res[day] = data[day][param]
    else:
        res = {
            'data': data
        }
    return(res)
        

@app.route('/day/<day>')
def day(day):
    '''
    This endpoint returns the schedule for a day.
    Optional parameters: 
        - 'block': Get timings for a time block in the day's schedule.
    '''
    try:
        data = loads(
            open(
                'schedule.json', 'r'
            ).read()
        )[day]
    except KeyError:
        return({
            'data': None
        })

    block = flask.request.args.get('block')

    if block != None:
        try:
            res = {
                'data': {
                    block: data[block]
                }
            }
        except KeyError:
            res = {
                'message': 'Time block not found.'
            }
    else:
        res = {
            'data': data
        }

    return(res)

@app.route('/day/<day>/time/<time>')
def time(day, time):
    schedule = get_schedule(day=day)
    del schedule['passing_periods']
    for block in schedule:
        if check_range(block, day, time):
            return({
                'data': {
                    block: schedule[block]
                }
            })
    return({
        'data': None
    })

@app.route('/current/schedule')
def current_schedule():
    try:
        res = get_schedule(
            day=calendar.day_name[date.today().weekday()].lower()
        )
    except KeyError:
        return({
            'data': None
        })

    block = flask.request.args.get('block')
    if block == None:
        return({
            'data': res
        })
    else:
        return({
            'data': {
                block: res[block]
            }
        })

@app.route('/current/period')
def current_period():
    day = calendar.day_name[date.today().weekday()].lower()
    schedule = get_schedule(
        day=day
    )
    del schedule['passing_periods']
    for block in schedule:
        if check_range(
            block, 
            day, 
            strftime('%H:%M', localtime())
        ):
            return({
                'data': {
                    block: schedule[block]
                }
            })
    return({
        'data': None
    })