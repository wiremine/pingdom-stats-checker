from datetime import datetime, timedelta, date, time
import pingdom
from credentials import username, password, key

p = pingdom.PingdomConnection(username, password, key)

# Monday = 0, Sunday = 7
today = datetime.today().weekday()

# We want the previous range of Sunday to Sunday,
# so find the previous Sunday...
start_date = date.today() - timedelta(date.today().weekday() + 8)  # weekday() is 0 based
# ...and add 6 days to get to Saturday
end_date = start_date + timedelta(6)

start_date = datetime.combine(start_date, time())
end_date = datetime.combine(end_date, time(23, 59, 59))

print "Uptime/response time stats for %s to %s" % (start_date, end_date)

checks = p.get_all_checks()

print "%-40s%-10s%-20s%-10s" % ("Website/Check", "Uptime", "Downtime (Mins)", "Response (Msecs)")

for check in checks:
    stats_dict = p.get_check_averages(check.id,
        timefrom=start_date.strftime('%s'), timeto=end_date.strftime('%s'))
    #print stats_dict
    total_uptime = float(stats_dict['summary']['status']['totalup'])
    total_downtime = float(stats_dict['summary']['status']['totaldown'])
    downtime = (total_downtime / (total_uptime + total_downtime)) * 100.0
    uptime = 100.0 - downtime

    response_time = "N/A"
    for country in stats_dict['summary']['responsetime']['avgresponse']:
        if country['countryiso'] == 'US':
            response_time = country['avgresponse']
            break

    print "%-40s%-10.2f%-20d%-10s" % (check.name, uptime, total_downtime / 60, response_time)
