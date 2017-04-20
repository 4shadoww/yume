
# Import python modules
import datetime
import time
import subprocess

# Import core modules
import core.config
from core import ores_api

# Import pywikibot
import pywikibot
from pywikibot.site import APISite

class Worker:

	def run(self):
		try:
			oldtime = datetime.datetime.utcnow() - datetime.timedelta(hours=12, minutes=0, seconds=0)
			api = APISite("fi")
			site = pywikibot.Site()
			first_scan = True
			first_scan = True
			print("now checking...")
			while True:
				timeutc = datetime.datetime.utcnow()
				timenow = datetime.datetime.now()

				counter = 0

				for rev in api.recentchanges(start=timeutc, end=oldtime):
					if counter >= core.config.scan_limit:
						break

					print(rev["revid"])
					response = ores_api.get(str(rev["revid"]))

					if not response:
						continue

					print("checking:", rev["title"], str(rev["revid"]))
					if core.config.max_false >= response[0] and core.config.min_true <= response[1]:
						subprocess.Popen(['notify-send', "possibly found vandalism"])
						print(response, end=" ")
						print("https://fi.wikipedia.org/w/index.php?title="+rev["title"].replace(" ", "_")+"&diff="+str(rev["revid"]))

					counter += 1

				oldtime = timeutc
				if datetime.datetime.utcnow() - oldtime <= datetime.timedelta(hours=0, minutes=core.config.sleeptime, seconds=0):
					sl = datetime.timedelta(hours=0, minutes=core.config.sleeptime, seconds=0) - (datetime.datetime.utcnow() - oldtime)
					print("sleeping for:", sl)
					time.sleep((sl.seconds))

		except KeyboardInterrupt:
			print("yume terminated...")
