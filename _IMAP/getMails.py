#!/usr/bin/env python
import datetime
from imbox import Imbox
from dateutil.parser import parse
import pytz
import re

class getMails(object):
	"""Returns emails of a given host."""
	def __init__(self, host, keys):
		super(getMails, self).__init__()
		self.host = host
		self.keys = keys
	def convertRfcDateIncTimezone_Easier(self, date):
		# print date
		pattern = re.compile("(.*)\s(\(.*\))")
		matched = pattern.search(date)
		if (matched != None):
			date = matched.group(1)
		parsedDate = parse(date)
		# print parsedDate
		return parsedDate.astimezone(pytz.timezone("Europe/Berlin"))
	def mailsOfDay(self, day):
		imbox = Imbox(self.host, username = self.keys.username, password = self.keys.password, ssl=True)
		beforeDay = day - datetime.timedelta(days=1)
		afterDay = day + datetime.timedelta(days=1)
		rawMessages = imbox.messages(date__gt=beforeDay.strftime("%d-%b-%Y"), date__lt=afterDay.strftime("%d-%b-%Y"))
		data = []
		for uid, message in rawMessages:
			date = self.convertRfcDateIncTimezone_Easier(message.date)
			if (date.date() == day):
					data.append((uid, date, message))
		return data
