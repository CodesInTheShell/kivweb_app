from django.shortcuts import render
import requests
import random
from bs4 import BeautifulSoup

# Create your views here.

def index(request):

	#job_listings = JobListing.objects.all()

	if request.method == "POST":

		discoUrl = request.POST.get("discoveryUrl", "")
		feedname = request.POST.get("feedname", "")
		username = request.POST.get("username", "")
		password = request.POST.get("password", "")
		tempfrom = request.POST.get("fromDate", "")
		to = request.POST.get("toDate", "")

		headers = {'Content-Type': 'application/xml',
                   'User-Agent': 'Kivred - TAXII Client Applicatiion',
                   'Accept': 'application/xml',
                   'X-TAXII-Accept': 'urn:taxii.mitre.org:message:xml:1.1',
                   'X-TAXII-Content-Type': 'urn:taxii.mitre.org:message:xml:1.1',
                   'X-TAXII-Protocol': 'urn.taxii.mitre.org:protocol:https:1.0'}
		msgID = str(random.randint(111111, 9999999999))
		args = {'feed_name': feedname, 'msg_ID': msgID, 'begin_Stamp': tempfrom + "T00:00:00Z", 'end_Stamp': to + "T12:00:00Z"}
		initxmldata = """<?xml version='1.0' encoding='utf-8'?>
        <taxii_11:Poll_Request
            xmlns:taxii_11="http://taxii.mitre.org/messages/taxii_xml_binding-1.1"
            message_id="{msg_ID}"
            collection_name="{feed_name}">""".format(**args)
		initfrom = """
            <taxii_11:Exclusive_Begin_Timestamp>{begin_Stamp}</taxii_11:Exclusive_Begin_Timestamp>
            """.format(**args)
		initto = """
            <taxii_11:Inclusive_End_Timestamp>{end_Stamp}</taxii_11:Inclusive_End_Timestamp>
            """.format(**args)
		inittailxml = """
            <taxii_11:Poll_Parameters allow_asynch="false">
                <taxii_11:Response_Type>FULL</taxii_11:Response_Type>
            </taxii_11:Poll_Parameters>
        </taxii_11:Poll_Request>
        """.format(**args)
		if tempfrom:
			initxmldata += initfrom
		if to:
			initxmldata += initto
		xmldata = initxmldata + inittailxml
		try:
			r = requests.post(discoUrl, auth=(username, password), headers=headers, data=xmldata)
		except Exception as e:
			print (e)
		soup = BeautifulSoup(r.content, features="xml")
		rawOutput = soup.prettify()
		
		indicators = soup.find_all('Indicators')
		
		##################################################################
		iocTitles = []
		iocDescriptions = []
		iocs = {}

		for i in indicators:

			tiTleString = i.Title.string
			decriptionString = i.Description.string

			if tiTleString:
				iocTitles.append(str(tiTleString))
				iocDescriptions.append(str(decriptionString))

		iocs = {
			'iocTitles': iocTitles,
			'iocDescriptions': iocDescriptions,
		}

		# Render only ioc's description
		return render(request, "kivweb_app/results.html", {'iocDescriptions': iocDescriptions})
	
	else:
		return render(request, "kivweb_app/index.html")


	
	