import requests
import json
import matplotlib.pyplot as plt
import math
import numpy


##### Current Problems:
####### Too Many People - Should be just house OR senate, and only current people
#			Solution - pre-compute person ids, and only grab voter votes/ cosponsors with those ids
####### Only counting aye votes - Should subtract for differing votes?

####### Too Many Votes - Should only look at non-procedural votes?
####### Cosponsorship not working
####### not getting all bills


#### Things to work on later:
#####Multiple axis
##### Better runtime


class person:
	def __init__(self, id, lastname, party = 'i', ideology = 0, leadership = 0):
		self.id = id
		self.lastname = lastname
		self.party = party
		self.ideology = ideology
		self.leadership = leadership


class personBill:
#Association between a person and a bill. could have used length two tuples, but this is easier to read.
	def __init__(self, person, bill, option = 1):
		self.person = person
		self.bill = bill
		self.option = option

record_limit = 200
high_limit = '&limit=' + str(record_limit)
date_limit = '&congress__gt=110'
order = '&order_by'


senate_bill_types = ["senate_bill", "senate_resolution"]
house_bill_types = ["house_bill", "house_resolution"]
senate_members = [400034, 400040, 400054, 400194, 400222, 400284, 400325, 400408, 400418, 300011, 300030, 300048, 300065, 300071, 300073, 300075, 300076, 300082, 300087, 300089, 300100, 400546, 300002, 402675, 412330, 412490, 412491, 412492, 412493, 412494, 412495, 412496, 400432, 412582, 412573, 412556, 412554, 412545, 412542, 412391, 412281, 412251, 412248, 412247, 412246, 412244, 412243, 412242, 412223, 412218, 412205, 412200, 412194, 300093, 300078, 300052, 300043, 300019, 300018, 400357, 400272, 400134, 400064, 400050, 400013, 300023, 300025, 300027, 300038, 300041, 300047, 300055, 300072, 300081, 300083, 300088, 400061, 400253, 400413, 412269, 412305, 412671, 412321, 412322, 412323, 412325, 412378, 412390, 412406, 412464, 412471, 412507, 412508, 412549, 412598, 412665, 412666, 412667, 412668, 412669]
house_members = [412306, 400004, 400018, 400021, 400029, 400030, 400032, 400033, 400036, 400041, 400046, 400047, 400048, 400052, 400057, 400062, 400063, 400068, 400071, 400074, 400075, 412670, 400077, 400080, 400081, 400086, 400087, 400089, 400090, 400093, 400097, 400100, 400101, 400103, 400108, 400111, 400114, 400116, 400122, 400124, 400129, 400130, 400137, 400141, 400142, 400145, 400154, 400157, 400158, 400160, 400162, 400163, 400170, 400175, 400179, 400185, 400189, 400195, 400196, 400199, 400204, 400206, 400209, 400211, 400218, 400219, 400220, 400224, 400230, 400232, 400233, 400237, 400238, 400240, 400244, 400245, 400246, 400247, 400249, 400251, 400259, 400262, 400263, 400271, 400273, 400276, 400279, 400285, 400289, 400290, 400291, 400295, 400297, 400308, 400309, 400313, 400314, 400316, 400320, 400326, 400333, 400340, 400341, 400343, 400344, 400347, 400348, 400349, 400350, 400351, 400352, 400355, 400356, 400360, 400361, 400363, 400364, 400365, 400366, 400367, 400371, 400373, 400376, 400378, 400379, 400380, 400381, 400402, 400403, 400404, 400406, 400411, 400414, 400415, 400416, 400417, 400419, 400422, 400431, 400433, 400440, 400441, 400606, 400607, 400616, 400618, 400623, 400626, 400627, 400630, 400636, 400639, 400640, 400641, 400643, 400644, 400646, 400648, 400651, 400652, 400653, 400654, 400655, 400656, 400657, 400659, 400660, 400661, 400663, 408211, 409888, 412186, 412189, 412190, 412191, 412192, 412193, 412195, 412196, 412199, 412202, 412209, 412211, 412212, 412213, 412214, 412215, 412217, 412221, 412226, 412236, 412239, 412250, 412254, 412255, 412256, 412257, 412258, 412259, 412261, 412263, 412270, 412271, 412272, 412275, 412276, 412278, 412280, 412282, 412283, 412284, 412286, 412290, 412292, 412293, 412294, 412295, 412302, 412303, 412307, 412308, 412309, 412310, 412311, 412312, 412315, 412317, 412318, 412319, 412327, 412331, 412379, 412382, 412385, 412388, 412392, 412393, 412394, 412395, 412396, 412397, 412399, 412400, 412402, 412403, 412404, 412405, 412407, 412409, 412410, 412411, 412412, 412416, 412417, 412419, 412420, 412421, 412422, 412426, 412427, 412428, 412429, 412430, 412431, 412432, 412434, 412435, 412436, 412437, 412438, 412443, 412444, 412445, 412446, 412447, 412453, 412454, 412457, 412460, 412461, 412462, 412463, 412465, 412466, 412468, 412469, 412470, 412472, 412473, 412474, 412475, 412476, 412477, 412478, 412479, 412480, 412482, 412483, 412484, 412485, 412486, 412487, 412488, 412489, 412498, 412500, 412501, 412503, 412505, 412506, 412509, 412510, 412511, 412512, 412513, 412514, 412515, 412516, 412517, 412519, 412520, 412521, 412522, 412523, 412524, 412525, 412526, 412527, 412529, 412531, 412532, 412533, 412536, 412537, 412538, 412539, 412540, 412541, 412543, 412544, 412546, 412548, 412550, 412551, 412552, 412553, 412555, 412557, 412558, 412560, 412561, 412562, 412563, 412564, 412565, 412566, 412567, 412568, 412569, 412570, 412571, 412572, 412574, 412575, 412576, 412578, 412579, 412580, 412581, 412583, 412584, 412585, 412595, 412596, 412600, 412601, 412603, 412604, 412605, 412606, 412607, 412608, 412609, 412610, 412611, 412612, 412613, 412614, 412615, 412616, 412617, 412618, 412619, 412620, 412621, 412622, 412623, 412624, 412625, 412626, 412627, 412628, 412629, 412630, 412631, 412632, 412633, 412634, 412635, 412636, 412637, 412638, 412639, 412640, 412641, 412642, 412643, 412644, 412645, 412646, 412647, 412648, 412649, 412650, 412651, 412652, 412653, 412654, 412655, 412656, 412657, 412658, 412659, 412660, 412661, 412662, 412663, 412664, 412672, 412673]

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
				print "No person with matching name!"
			else:
				associated_person = relevant_people[0]
				associated_person.leadership = member["y"]
				associated_person.ideology = member["x"]
				associated_person.party = party_string


def fetch_relevant_bill_ids(term_list, chamber = "senate"):
	try:
		offset = 0
		fetch_url = 'http://www.govtrack.us/api/v2/bill?q=' + '|'.join(term_list) + date_limit + high_limit + '&offset=' + str(offset)
		#url_fetch_string = requests.get('http://www.govtrack.us/api/v2/bill?q=' + '|'.join(term_list) + date_limit + high_limit)
		bill_json= requests.get(fetch_url).json()
		total_bills = bill_json['meta']['total_count']
		print "There are " + str(total_bills) + " total bills"
		relevant_ids = [item['id'] for item in bill_json['objects'] if item['bill_type'] in senate_bill_types]
		#print [item['bill_type'] for item in bill_json['objects']]
		offset = 0
		seen = record_limit
		while seen < total_bills:
			offset += record_limit
			seen += record_limit
			fetch_url = 'http://www.govtrack.us/api/v2/bill?q=' + '|'.join(term_list) + date_limit + high_limit + '&offset=' + str(offset)
			bill_json= requests.get(fetch_url).json()
			relevant_ids += [item['id'] for item in bill_json['objects'] if item['bill_type'] in senate_bill_types]
			#print [item['bill_type'] for item in bill_json['objects']]
		print ("Fetched " + str(len(relevant_ids)) + " bills!")
		return relevant_ids
	except ValueError:
		print "Value Error for initial Bill Query: "

# Takes in a list of bill_ids and returns a list of personBills representing yes votes
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

# Takes in a list of bill_ids and returns a list of personBills representing bill sponsors
"""
def fetch_cosponsors(bill_ids):
	for bill_id in bill_ids:
		XXXbill_string = 'http://www.govtrack.us/api/v2/vote?related_bill=' + str(bill_id) + high_limit
		try:
			fetch = requests.get(bill_string).json()
			cosponsor_ids = [item['id'] for item in fetch['objects']]
			print ("Found " + str(len(vote_ids)) + " cosponsors!")
			for vote in vote_ids:
				#get voter votes
				vote_url = 'http://www.govtrack.us/api/v2/vote_voter?vote=' + str(vote) + high_limit
				try:
					votes = requests.get(vote_url).json()['objects']
					total_votes += len(votes)
					for person_vote in votes:
						person = XXX
						if not person in people:
							people.append person
						people[person].append person_vote
				except ValueError:
					print "Value Error for Vote with url" + vote_url
		except ValueError:
			print "Value Error for bill with url" + bill_string
"""

def fetch_people(person_ids):
	full_people = {}
	for person in person_ids:
		person_url = "https://www.govtrack.us/api/v2/person/" + person
		person_raw_request = requests.get(person_url)
		person_info = person_raw_request.json()
		full_people[person] = person_info


##once we've fetch all the bills, votes/cosponsorships, and people, we 
#filter out people not present in current congress, then


#build cosponsorship matrix by
#for each person, going through all their bills and make an array of all other people and increment each one that shows up

def build_matrix(person_bill_list, person_list = None, bill_list = None):
	m = [] # Resultant Matrix

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

	for person in person_list:
		#value in each cell is the number of bill voted/sponsored in common by the two candidates
		their_array = [len([bill for bill in p2b[person] if other_person in b2p[bill]]) for other_person in person_list]
 		m.append(their_array)

 	return m


#Then, just do math magic on the matrix
#directly lifted from govtrack ideology analysis
def matrix_to_spectrum(P):
	u, s, vh = numpy.linalg.svd(P)
	spectrum = vh[1,:]

	def rescale(u, log=False):
		# Re-scale the vector to range from 0 to 1, and convert it out of
		# numpy data format.
		u = (u - min(u)) / (max(u) - min(u))
		
		# If log is True, then rescale the values on an essentially logarithmic
		# axis, such that the median value comes out as linearly halfway
		# between the min and maximum values. Note that the unscaled
		# min and max are 0 and 1, respectively, since we already rescaled
		# above. Thus:
		#    1/2*(log(0 + s) + log(1 + s)) = log(median + s)
		# Wolfram|Alpha says the solution is:
		#    s = -m^2/(2m-1)
		if log:
			m = numpy.median(u)
			s = -m**2/(2*m - 1)
			u = numpy.log(u + s)
			u = (u - min(u)) / (max(u) - min(u))
		return [float(v) for v in u]

	# Scale the values from 0 to 1.
	spectrum = rescale(spectrum)
	
	return spectrum

def draw_chart(spectrum, people):
	chart = plt.figure()
	for i in range(len(spectrum)):
		person = people[i]
		x = person.ideology# x coordinate, general ideology
		y = spectrum[i]# y coordinate, specific ideology
		color = 'g'
		print person.party
		if person.party == "Republican":
			color = 'r'
		if person.party == "Democrat":
			color = 'b'
		plt.scatter(x, y, c=color)
		plt.annotate(person.lastname, (x,y))
	plt.show()

def is_current(person):
	res = False
	current_congress = 114
	try:
		for role in person["roles"]:
			if current_congress in role["congress_numbers"]:
				res = True
	except KeyError:
		print person
	return res

def generate_vote_spectrum(terms, chamber = "senate"):
	bills = fetch_relevant_bill_ids(terms)
	print "Fetched "  + str(len(bills)) + " Bills!"
	votes, people = fetch_votes(bills)
	print "Fetched "  + str(len(votes)) +  " person votes accross " + str(len(people)) + " people!"
	#current_people = [ person for person in people.values() if is_current(person)]
	people_list = people.values()
	import_scores_from_json(people_list, chamber)
	people_id_list = [person.id for person in people_list]
	m = build_matrix(votes, people_id_list)
	s = matrix_to_spectrum(m)
	print "AAAAAYYYYYY we did it!!"
	print s
	draw_chart(s, people_list)


search_terms = ['nuclear']
generate_vote_spectrum(search_terms)


