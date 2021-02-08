import flask
from datetimerange import DateTimeRange
from datetime import date
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
    print(f"{today}T{to_verify}:00+0800" in time_range)
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
    data = loads(
        open(
            'schedule.json', 'r'
        ).read()
    )[day]

    param = flask.request.args.get('block')

    if param != None:
        try:
            res = {
                'data': data[param]
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
            

app.run(debug=True)