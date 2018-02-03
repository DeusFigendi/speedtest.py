import subprocess
import random
import requests
import re

def get_node_info():
	# JSON von http://10.15.8.1/cgi-bin/nodeinfo herunter laden und öffnen
	# parse and return
	r = requests.get('http://10.15.8.1/cgi-bin/nodeinfo')
	return(r.json())

def get_url_mediaccc():
	# INDEX herunter laden und öffnen
	r = requests.get('https://cdn.media.ccc.de/INDEX')
	# Zufällige Zeile lesen und URL zusammen bauen
	random_line = random.choice(r.text.split("\n"))
	# return
	return("https://cdn.media.ccc.de/"+random_line)
	
def get_url_podcast():
	# Frage die API nach einem von 15.000 Podcasts
	r = requests.get('https://api.fyyd.de/0.2/podcasts', params={"count" : "1" , "page" : random.randrange(15000)})
	print(r.text)
	this_podcast_id = r.json()["data"][0]["id"]
	r = requests.get('https://api.fyyd.de/0.2/podcast/episodes', params={"podcast_id" : this_podcast_id})
	this_return_url = random.choice(r.json()["data"]["episodes"])["enclosure"]
	return(this_return_url)

def get_url_debian():
	r = requests.get('http://debian-cd.debian.net/debian-cd/current/multi-arch/iso-cd/')
	# href="debian-9.3.0-amd64-i386-netinst.iso"
	this_return_regexp = re.search(r'href="debian.*\.iso"', r.text, flags=0)
	return('http://debian-cd.debian.net/debian-cd/current/'+random.choice(["amd64/", "arm64/", "armel/", "armhf/", "i386/", "mips/", "mips64el/", "mipsel/", "multi-arch/", "ppc64el/", "s390x/", "source/"])+'iso-cd/'+this_return_regexp.group(0).strip("href=").strip('"'))

def get_url_freifunk():
	random_domain = "d"+str(random.randrange(1,4))
	r = requests.get('http://download.freifunk-lippe.de/images/'+random_domain+'/lip/stable/factory/')
	this_return_regexp = re.search(r'href="gluon-fflip.*\.(bin|iso|img)"', r.text, flags=0)
	return('http://download.freifunk-lippe.de/images/'+random_domain+'/lip/stable/factory/'+this_return_regexp.group(0).strip("href=").strip('"'))


def recordaspeedtest():
	this_node_info = get_node_info()
	print(this_node_info)
	speedtest_type = random.random()
	if speedtest_type < 0.25:
		speedtest_url = get_url_mediaccc()
	elif speedtest_type < 0.5:
		speedtest_url = get_url_podcast()
	elif speedtest_type < 0.75:
		speedtest_url = get_url_debian()
	elif speedtest_type < 1:
		speedtest_url = get_url_freifunk()
	download_test = subprocess.run(["wget", speedtest_url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	print("-------------")
	print("-------------")
	print("-------------")
	print(download_test.stdout.decode("utf8"))

# foo = subprocess.run(["wget", "http://cdn.media.ccc.de/events/privacyweek/2017/h264-hd/pw17-177-deu-I_GOOGLE_YOU_hd.mp4"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# print(foo.stdout.decode("utf8"))

def find_out_if_connected_to_freifunk():
	ip_result = subprocess.run(["ip", "address"], stdout=subprocess.PIPE)
	if "brd 10.15.15.255" in ip_result.stdout.decode("utf8"):
		return(True)
	else:
		return(False)

if find_out_if_connected_to_freifunk():
	recordaspeedtest()
else:
	print("Nicht mit Freifunk verbunden")
