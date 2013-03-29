import re

def parseUrl(url):
	try:
		match = re.search(r"ll=(-?\d+\.\d+),(-?\d+\.\d+)", url)
		return [float(match.group(1)), float(match.group(2))]
	except:
		return None



print parseUrl("https://maps.google.ie/?ie=UTF8&ll=54.236583,-5.95157&spn=0.000825,0.002642&t=h&z=19&vpsrc=6")
