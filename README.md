# Harker Bell Schedule API
A modern, lightweight, lighting-speed bell schedule API built for developers building applications needing the bell schedule, in a nice neat format.

## Why?
We were making a project ourselves that needed the bell schedule in JSON format, so we thought, "why not make it for others to use"?

## API Refrence

---------------

### `/all`
This endpoint returns the entire schedule for all five days of the week. \
Parameters:
* `block` (optional): Get timings for a time block in each day's schedule. Example: `p1` for period one.

---------------

### `/day/<day>`
This endpoint returns the schedule for a day. \
Parameters: 
* `block` (optional): Get timings for a time block in the day's schedule. Example: `p1` for period one.

---------------

### `/day/<day>/time/<time>`
This endpoint returns the period for a given time and day. For example, if you wanted to know what period is at 9:30 on Monday, you could make a request to `/day/monday/time/09:30`.

---------------

### `/current/schedule`
This endpoint returns the schedule of today.
Parameters: 
* `block` (optional): Get timings for a time block in today's schedule. Example: `p1` for period one.

---------------

### `/current/period`
This endpoint provides data for the current period.