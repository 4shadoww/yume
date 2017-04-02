
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

class Worker:
	counter = 0

	def run(self):
		try:
			oldtime = datetime.timedelta(hours=12, minutes=0, seconds=0)
			timenow = datetime.datetime.now()
			site = pywikibot.Site()
			print(timenow-oldtime)
			gen = pagegenerators.RecentChangesPageGenerator(start=timenow, end=timenow-oldtime)
			print("now checking...")

			for page in gen:
				if self.counter >= core.config.first_scan:
					break
				if page.exists():
					response = ores_api.get(str(page.latest_revision_id))

					if not response:
						continue

					print("checking:", page.title(), str(page.latest_revision_id))
					if core.config.max_false >= response[0] and core.config.min_true <= response[1]:
						subprocess.Popen(['notify-send', "possibly found vandalism"])
						print(response, end=" ")
						print("https://fi.wikipedia.org/w/index.php?title="+page.title().replace(" ", "_")+"&diff="+str(page.latest_revision_id))

					self.counter += 1

		except KeyboardInterrupt:
			print("yume terminated...")
