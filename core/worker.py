
# Import python modules
import datetime
import time
import subprocess

# Import core modules
import core.config
from core import ores_api

# Import pywikibot
import pywikibot
from pywikibot import pagegenerators
from pywikibot.site import APISite

class Worker:
	counter = 0

	def run(self):
		try:
			oldtime = datetime.timedelta(hours=12, minutes=0, seconds=0)
			timenow = datetime.datetime.now()
			api = APISite("fi")
			site = pywikibot.Site()

			print("now checking...")

			for rev in api.recentchanges(start=timenow, end=timenow-oldtime):
				if self.counter >= core.config.first_scan:
					break
				response = ores_api.get(str(rev["revid"]))

				if not response:
					continue

				print("checking:", rev["title"], str(rev["revid"]))
				if core.config.max_false >= response[0] and core.config.min_true <= response[1]:
					subprocess.Popen(['notify-send', "possibly found vandalism"])
					print(response, end=" ")
					print("https://fi.wikipedia.org/w/index.php?title="+rev["title"].replace(" ", "_")+"&diff="+str(rev["revid"]))

				self.counter += 1

		except KeyboardInterrupt:
			print("yume terminated...")
