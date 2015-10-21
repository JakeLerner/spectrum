import requests
import json
import matplotlib.pyplot as plt
import math
import numpy
import sys


### ~ Classes ~ ###

# Minimalistic representation of a legislator
class person:
	def __init__(self, id, lastname, party = 'i', ideology = 0, leadership = 0):
		self.id = id
		self.lastname = lastname
		self.party = party
		self.ideology = ideology
		self.leadership = leadership


#Association between a person and a bill. Easier to read than tuples.
class personBill:
	def __init__(self, person, bill, option = 1):
		self.person = person
		self.bill = bill
		self.option = option


### ~ Constants ~ ###

record_limit = 200
high_limit = '&limit=' + str(record_limit)
date_limit = '&congress__gt=110'
order = '&order_by'
senate_bill_types = ["senate_bill", "senate_resolution"]
house_bill_types = ["house_bill", "house_resolution"]
senate_members = [400034, 400040, 400054, 400194, 400222, 400284, 400325, 400408, 400418, 300011, 300030, 300048, 300065, 300071, 300073, 300075, 300076, 300082, 300087, 300089, 300100, 400546, 300002, 402675, 412330, 412490, 412491, 412492, 412493, 412494, 412495, 412496, 400432, 412582, 412573, 412556, 412554, 412545, 412542, 412391, 412281, 412251, 412248, 412247, 412246, 412244, 412243, 412242, 412223, 412218, 412205, 412200, 412194, 300093, 300078, 300052, 300043, 300019, 300018, 400357, 400272, 400134, 400064, 400050, 400013, 300023, 300025, 300027, 300038, 300041, 300047, 300055, 300072, 300081, 300083, 300088, 400061, 400253, 400413, 412269, 412305, 412671, 412321, 412322, 412323, 412325, 412378, 412390, 412406, 412464, 412471, 412507, 412508, 412549, 412598, 412665, 412666, 412667, 412668, 412669]
house_members = [412306, 400004, 400018, 400021, 400029, 400030, 400032, 400033, 400036, 400041, 400046, 400047, 400048, 400052, 400057, 400062, 400063, 400068, 400071, 400074, 400075, 412670, 400077, 400080, 400081, 400086, 400087, 400089, 400090, 400093, 400097, 400100, 400101, 400103, 400108, 400111, 400114, 400116, 400122, 400124, 400129, 400130, 400137, 400141, 400142, 400145, 400154, 400157, 400158, 400160, 400162, 400163, 400170, 400175, 400179, 400185, 400189, 400195, 400196, 400199, 400204, 400206, 400209, 400211, 400218, 400219, 400220, 400224, 400230, 400232, 400233, 400237, 400238, 400240, 400244, 400245, 400246, 400247, 400249, 400251, 400259, 400262, 400263, 400271, 400273, 400276, 400279, 400285, 400289, 400290, 400291, 400295, 400297, 400308, 400309, 400313, 400314, 400316, 400320, 400326, 400333, 400340, 400341, 400343, 400344, 400347, 400348, 400349, 400350, 400351, 400352, 400355, 400356, 400360, 400361, 400363, 400364, 400365, 400366, 400367, 400371, 400373, 400376, 400378, 400379, 400380, 400381, 400402, 400403, 400404, 400406, 400411, 400414, 400415, 400416, 400417, 400419, 400422, 400431, 400433, 400440, 400441, 400606, 400607, 400616, 400618, 400623, 400626, 400627, 400630, 400636, 400639, 400640, 400641, 400643, 400644, 400646, 400648, 400651, 400652, 400653, 400654, 400655, 400656, 400657, 400659, 400660, 400661, 400663, 408211, 409888, 412186, 412189, 412190, 412191, 412192, 412193, 412195, 412196, 412199, 412202, 412209, 412211, 412212, 412213, 412214, 412215, 412217, 412221, 412226, 412236, 412239, 412250, 412254, 412255, 412256, 412257, 412258, 412259, 412261, 412263, 412270, 412271, 412272, 412275, 412276, 412278, 412280, 412282, 412283, 412284, 412286, 412290, 412292, 412293, 412294, 412295, 412302, 412303, 412307, 412308, 412309, 412310, 412311, 412312, 412315, 412317, 412318, 412319, 412327, 412331, 412379, 412382, 412385, 412388, 412392, 412393, 412394, 412395, 412396, 412397, 412399, 412400, 412402, 412403, 412404, 412405, 412407, 412409, 412410, 412411, 412412, 412416, 412417, 412419, 412420, 412421, 412422, 412426, 412427, 412428, 412429, 412430, 412431, 412432, 412434, 412435, 412436, 412437, 412438, 412443, 412444, 412445, 412446, 412447, 412453, 412454, 412457, 412460, 412461, 412462, 412463, 412465, 412466, 412468, 412469, 412470, 412472, 412473, 412474, 412475, 412476, 412477, 412478, 412479, 412480, 412482, 412483, 412484, 412485, 412486, 412487, 412488, 412489, 412498, 412500, 412501, 412503, 412505, 412506, 412509, 412510, 412511, 412512, 412513, 412514, 412515, 412516, 412517, 412519, 412520, 412521, 412522, 412523, 412524, 412525, 412526, 412527, 412529, 412531, 412532, 412533, 412536, 412537, 412538, 412539, 412540, 412541, 412543, 412544, 412546, 412548, 412550, 412551, 412552, 412553, 412555, 412557, 412558, 412560, 412561, 412562, 412563, 412564, 412565, 412566, 412567, 412568, 412569, 412570, 412571, 412572, 412574, 412575, 412576, 412578, 412579, 412580, 412581, 412583, 412584, 412585, 412595, 412596, 412600, 412601, 412603, 412604, 412605, 412606, 412607, 412608, 412609, 412610, 412611, 412612, 412613, 412614, 412615, 412616, 412617, 412618, 412619, 412620, 412621, 412622, 412623, 412624, 412625, 412626, 412627, 412628, 412629, 412630, 412631, 412632, 412633, 412634, 412635, 412636, 412637, 412638, 412639, 412640, 412641, 412642, 412643, 412644, 412645, 412646, 412647, 412648, 412649, 412650, 412651, 412652, 412653, 412654, 412655, 412656, 412657, 412658, 412659, 412660, 412661, 412662, 412663, 412664, 412672, 412673]


### ~ Json Parsing ~ ###

# Given govtrack API json for a person, make a (v. stripped down) person object.
def person_from_json(person_json):
	return person(person_json["id"], person_json["lastname"])

def import_scores_from_json(people, chamber = "senate"):
	my_file = open("./json/" + chamber + "_json_from_chart", "r")
	chamber_json = json.loads(my_file.read())
	for party in chamber_json:
		party_string = party["party"]
		members = party["data"]
		for member in members:
			name = member["name"]
			relevant_people = [person for person in people if person.lastname == name]
			if len(relevant_people) != 1:
				print "No person with name matching " + name
			else:
				associated_person = relevant_people[0]
				associated_person.leadership = member["y"]
				associated_person.ideology = member["x"]
				associated_person.party = party_string


### ~ API Access ~ ###

# Fetch Bills which contain a word in the given term list.
def fetch_relevant_bill_ids(term, chamber = "senate"):
	try:
		offset = 0
		fetch_url = 'http://www.govtrack.us/api/v2/bill?q=' + term + date_limit + high_limit + '&offset=' + str(offset)
		#url_fetch_string = requests.get('http://www.govtrack.us/api/v2/bill?q=' + '|'.join(term_list) + date_limit + high_limit)
		bill_json= requests.get(fetch_url).json()
		total_bills = bill_json['meta']['total_count']
		print "There are " + str(total_bills) + " bills containing " + term
		relevant_ids = [item['id'] for item in bill_json['objects'] if item['bill_type'] in senate_bill_types]
		#print [item['bill_type'] for item in bill_json['objects']]
		offset = 0
		seen = record_limit
		while seen < total_bills:
			offset += record_limit
			seen += record_limit
			fetch_url = 'http://www.govtrack.us/api/v2/bill?q=' + term + date_limit + high_limit + '&offset=' + str(offset)
			bill_json= requests.get(fetch_url).json()
			relevant_ids += [item['id'] for item in bill_json['objects'] if item['bill_type'] in senate_bill_types]
			#print [item['bill_type'] for item in bill_json['objects']]
		#print ("Fetched " + str(len(relevant_ids)) + " bills!")
		print "Kept " + str(len(relevant_ids))
		return relevant_ids
	except ValueError:
		print "Value Error for initial Bill Query: "

# Takes in a list of bill_ids and returns a list of personBills representing yes votes
# Note that this may include procedural votes.
# I decided procedural votes probably function as valid data points for delineating pols.
def fetch_votes(bill_ids):
	person_bills = []
	people = {}
	i = 1
	total_votes = 0
	for bill_id in bill_ids:
		print i,
		i += 1
		bill_string = 'http://www.govtrack.us/api/v2/vote?related_bill=' + str(bill_id) +  high_limit
		try:
			fetch = requests.get(bill_string).json()
			vote_ids = [item['id'] for item in fetch['objects']]
			print [item['vote_type'] for item in fetch['objects']]
			print ("Found " + str(len(vote_ids)) + " votes!")
			for vote in vote_ids:
				#get voter votes
				vote_url = 'http://www.govtrack.us/api/v2/vote_voter?vote=' + str(vote) + high_limit
				try:
					print ".",
					votes = requests.get(vote_url).json()['objects']
					total_votes += len(votes)
					for person_vote in votes:
						person = person_from_json(person_vote["person"])
						vote_option = person_vote["option"]["key"]
						if vote_option == "+" and person.id in senate_members:
							if not person.id in people.keys():
								people[person.id] = person
							person_bills.append(personBill(person.id, bill_id))
				except ValueError:
					print "Value Error for Vote with url" + vote_url
		except ValueError:
			print "Value Error for bill with url" + bill_string
	return person_bills, people

# Takes in a list of bill_ids and returns a list of personBills representing Co-Sponsorships
def fetch_cosponsors(bill_ids):
	person_bills = []
	people = {}
	bill_progress = 0
	for bill_id in bill_ids:
		bill_progress += 1
		bill_string = 'http://www.govtrack.us/api/v2/bill/' + str(bill_id)
		bill_json = requests.get(bill_string).json()
		cosponsoring_people = bill_json['cosponsors']
		print str(bill_progress) + " - Found " + str(len(cosponsoring_people)) + ' cosponsors!'
		for cosponsor in cosponsoring_people:
			person = person_from_json(cosponsor)
			if person.id in senate_members:
				people[person.id] = person
				person_bills.append(personBill(person.id, bill_id))
	return person_bills, people



#Fetches all person information based on govtrack id.
#Currently unused, because it turns out this is included in vote_voter.
def fetch_people(person_ids):
	full_people = {}
	for person in person_ids:
		person_url = "https://www.govtrack.us/api/v2/person/" + person
		person_raw_request = requests.get(person_url)
		person_info = person_raw_request.json()
		full_people[person] = person_info
	return full_people


### ~ Analysis ~ ###

#Build cosponsorship matrix from list of person-bill associations representing 'aye' votes.
#person_list and bill_list can be used to limit the people or bills in the matrix.
def build_matrix(person_bill_list, person_list = None, bill_list = None):
	m = [] # Resultant Matrix

	#Default to complete lists (with repeats removed) if no lists specified
	if not person_list:
		person_list = list(set([person_bill.person for person_bill in person_bill_list]))
	else:
		person_list = list(set(person_list))
		##This is a list of all people in arbitrary order, but it's the order we'll use for the matrix

	if not bill_list:
		bill_list = list(set([person_bill.bill for person_bill in person_bill_list]))
	else:
		bill_list = list(set(bill_list))


	#Make dictonary with people keys and lists of bills as values
	p2b = {}
	for person in person_list:
		p2b[person] = [item.bill for item in person_bill_list if item.person == person]

	#Dictionary with bills as keys and associated people as values
	b2p = {}
	for bill in bill_list:
		b2p[bill] = [item.person for item in person_bill_list if item.bill == bill]

	# Make an arracy for each person in the matrix, append it to the matrix
	for person in person_list:
		#value in each cell is the number of bill voted/sponsored in common by the two candidates
		their_array = [len([bill for bill in p2b[person] if other_person in b2p[bill]]) for other_person in person_list]
 		m.append(their_array)

 	return m


# Then, just do math magic on the matrix
# directly lifted from govtrack ideology analysis
# https://github.com/govtrack/govtrack.us-web/blob/master/analysis/sponsorship_analysis.py
def matrix_to_spectrum(P):
	u, s, vh = numpy.linalg.svd(P)
	spectrum = vh[1,:]

	def rescale(u, log=False):
		u = (u - min(u)) / (max(u) - min(u))
		if log:
			m = numpy.median(u)
			s = -m**2/(2*m - 1)
			u = numpy.log(u + s)
			u = (u - min(u)) / (max(u) - min(u))
		return [float(v) for v in u]

	# Scale the values from 0 to 1.
	spectrum = rescale(spectrum)
	return spectrum

### ~ Visualization ~ ###

# Draw 2D pyplot chart from spectrum values and similarly ordered list of people
def draw_chart(spectrum, people):
	chart = plt.figure()
	for i in range(len(spectrum)):
		person = people[i]
		x = person.ideology# x coordinate, general/sponsorship ideology
		y = spectrum[i]# y coordinate, specific/vote ideology
		color = 'g' #We'll use green for Independants
		if person.party == "Republican":
			color = 'r'
		if person.party == "Democrat":
			color = 'b'
		plt.scatter(x, y, c=color)
		plt.annotate(person.lastname, (x,y))
	plt.show()

### ~ Main Runtime ~ ###


# Currently, prefer cosponsor spectrum
# Less grounded in literature, requires more API pulls, less clear results.
def generate_vote_spectrum(terms, chamber = "senate", save = False):
	bills = fetch_relevant_bill_ids(terms)
	print "Fetched "  + str(len(bills)) + " Bills!"
	votes, people = fetch_votes(bills)
	if save:
		save_file = open("saved_results/" + chamber + '_'.join(terms), 'w')
		save_json_string = ''
		save_json_string += "{ 'votes' : " + str(votes) + " , 'people' : " + str(people) + "}"
	print "Fetched "  + str(len(votes)) +  " person votes accross " + str(len(people)) + " people!"
	people_list = people.values()
	import_scores_from_json(people_list, chamber)
	people_id_list = [person.id for person in people_list]
	m = build_matrix(votes, people_id_list)
	s = matrix_to_spectrum(m)
	print "AAAAAYYYYYY we did it!!"
	print s
	draw_chart(s, people_list)

def generate_cosponsor_spectrum(terms, chamber = "senate", save = False, verbose = 1):
	print "~~~~~~~~~~~~~~~~"
	print "Beginning New Cosponsor Spectrum Analysis across members of the " + chamber
	print "Searching for bills containing terms: " + ", ".join(terms)
	
	if verbose: print "--> Fetching Bills"
	bills = []
	for term in terms:
		bills += fetch_relevant_bill_ids(term)
	if verbose: print "Fetched "  + str(len(bills)) + " Bills!"
	
	if verbose: print "--> Fetching Person Bills"
	relations, people = fetch_cosponsors(bills)
	if verbose: print "Fetched "  + str(len(relations)) +  " person bills accross " + str(len(people)) + " people!"
	
	if verbose: print "--> Playing with JSON"
	people_list = people.values()
	import_scores_from_json(people_list, chamber)
	people_id_list = [person.id for person in people_list]
	
	if verbose: print "--> Building Matrix"
	m = build_matrix(relations, people_id_list)
	
	if verbose: print "--> Converting to Spectrum"
	s = matrix_to_spectrum(m)
	
	if verbose: print "--> Drawing Chart"
	print s
	draw_chart(s, people_list)

####### What runs the code. #####
#Should probably someday be enclosed in a main function with commandline options or summat.

search_terms = sys.argv[1:]

#Should handle multiple search terms by running fetch_relevant_bill_ids multiple times and combining lists
generate_cosponsor_spectrum(search_terms)