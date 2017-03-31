
# Import python modules
import datetime
import time

# Import core modules
from core import ores_api

# Import pywikibot
import pywikibot
from pywikibot import pagegenerators

class Worker:
	limit = 100
	counter = 0
	checked = []

	def run(self):
		try:
			oldtime = datetime.timedelta(hours=12, minutes=0, seconds=0)
			timenow = datetime.datetime.now()
			site = pywikibot.Site()
			print(timenow-oldtime)
			gen = pagegenerators.RecentChangesPageGenerator(start=timenow, end=timenow-oldtime)
			print("now checking")

			for page in gen:
				if self.counter >= self.limit:
					break
				if page.exists() and not any(page.title() == s for s in self.checked):

					print(ores_api.get(str(page.latest_revision_id)), end=" ")
					print("https://fi.wikipedia.org/w/index.php?title="+page.title().replace(" ", "_")+"&diff="+str(page.latest_revision_id))
					self.checked.append(page.title())

					self.counter += 1

		except KeyboardInterrupt:
			print("yume terminated...")
