#!/usr/bin/env python
import datetime, time, calendar, dateutil.relativedelta
import argparse
import parsedatetime

def generateMonth(year, month, until=-1):
	untilDay = calendar.monthrange(year, month)[1] if until == -1 else until
	return [datetime.datetime(year=year, month=month, day=thisDay) for thisDay in range(1, untilDay+1)]

def parseString(arg):
	if (("last week" == arg.string) or ("lastweek" == arg.string)):
		dayOfTheWeek = calendar.weekday(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
		lastSunday = datetime.date.today() - datetime.timedelta(days=(dayOfTheWeek+1))
		return list(reversed([lastSunday - datetime.timedelta(days=i) for i in range(7)]))
	elif (("this week" == arg.string) or ("thisweek" == arg.string)):
		dayOfTheWeek = calendar.weekday(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day)
		lastMonday = datetime.date.today() - datetime.timedelta(days=dayOfTheWeek)
		return [lastMonday + datetime.timedelta(days=i) for i in range(0,dayOfTheWeek)]
	elif ("yesterday" == arg.string):
		return [datetime.date.today() - datetime.timedelta(days=1)]
	elif (("last month" == arg.string) or ("lastmonth" == arg.string)):
		dateLastMonth = datetime.date.today() + dateutil.relativedelta.relativedelta(months=-1)
		return generateMonth(dateLastMonth.year, dateLastMonth.month)
	elif (("this month" == arg.string) or ("thismonth" == arg.string)):
		return generateMonth(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day - 1) # -1 since today can't be retrieved (it might not be synced yet)
	elif (("last 10 days" == arg.string) or ("last10days" == arg.string)):
		return list(reversed(list(datetime.date.today() - datetime.timedelta(days=i) for i in range(1,10))))
	else:
		return [datetime.date.fromtimestamp(time.mktime(parsedatetime.Calendar().parse(arg.string)[0]))]

def parse():
	parser = argparse.ArgumentParser(description='Update Fitbit data. If no arguments are given, the current day (' + datetime.date.today().strftime('%Y-%m-%d') +') is assumed.')
	parser.add_argument('-t', '--table', default='Fitbit', help='Name of SQL table name')
	parser.add_argument('-y', '--year', type=int, help='Year to be requested')
	parser.add_argument('-m', '--month', type=int, help='Month to be requested')
	parser.add_argument('-d', '--day', type=int, help='Day to be requested')
	parser.add_argument('-s', '--string', type=str, help='Shortcode string of requested time or period. EXAMPLES: yesterday, last week, 2 days ago, this month.')
	args = parser.parse_args()

	currentYear = datetime.date.today().year
	currentMonth = datetime.date.today().month
	currentDay = datetime.date.today().day

	datesToBeRequested = []

	if (not args.string and not args.year and not args.month and not args.day):
		''' No arguments = today '''
		datesToBeRequested = [datetime.date(year=currentYear, month=currentMonth, day=currentDay)]

	elif (args.day and not args.string):
		''' One single date. '''
		singleDateDay = args.day
		singleDateMonth = args.month if args.month else currentMonth
		singleDateYear = args.year if args.year else currentYear
		datesToBeRequested = [datetime.date(year=singleDateYear, month=singleDateMonth, day=singleDateDay)]

	elif (args.month and not args.day and not args.string):
		''' One whole month. '''
		wholeMonthYear = args.year if args.year else currentYear
		datesToBeRequested = generateMonth(wholeMonthYear, args.month)

	elif (args.year and not args.day and not args.month and not args.string):
		''' Whole year. Does not make sense because of Fitbit API limit, though. '''
		for month in range(1, 12+1):
			datesToBeRequested = datesToBeRequested + [datetime.datetime(year=args.year, month=month, day=thisDay) for thisDay in range(1, calendar.monthrange(args.year, month)[1]+1)]

	elif (args.string and not args.year and not args.month and not args.day):
		''' Parse strings '''
		datesToBeRequested = parseString(args)

	else: # all parameter
		datesToBeRequested = "Giving ALL the parameters makes no sense."

	return (datesToBeRequested, args.table)

if __name__ == '__main__':
	dates, tablename = parse()
	print dates, tablename
