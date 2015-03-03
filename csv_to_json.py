import csv, json

def get_year_data(year): 
	# Note: '#' char in csv strings is a stand-in for a comma
	# What to do with negative time values?
	f = open('data/{0}.csv'.format(year))
	j = []
	headers = ["Activity","Total%","Men%","Women%","TotalH","MenH","WomenH"]
	reader = csv.DictReader(f, headers)
	# logging.info(reader)
	for row in reader:
		j.append(row)
	k = []
	# Personal care activities
	act = j[0]
	act["Sub-Activities"] = j[1:6]
	k.append(act)
	# Eating and drinking
	act = j[6]
	act["Sub-Activities"] = j[7:9]
	k.append(act)
	# Household activities
	act = j[9]
	act["Sub-Activities"] = j[10:20]
	k.append(act)
	# Purchasing goods and services
	act = j[20]
	act["Sub-Activities"] = []
	# Consumer goods purchases
	s_act = j[21]
	s_act["Sub-Activities"] = j[22]
	act["Sub-Activities"].append(s_act)
	# Professional and personal care services
	s_act = j[23]
	s_act["Sub-Activities"] = j[24:27]
	act["Sub-Activities"].append(s_act)
	# Household services
	s_act = j[27]
	s_act["Sub-Activities"] = j[28:30]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[30])
	act["Sub-Activities"].append(j[31])
	k.append(act)
	# Caring for and helping household members
	act = j[32]
	act["Sub-Activities"] = []
	s_act = j[33]
	s_act["Sub-Activities"] = j[34:37]
	act["Sub-Activities"].append(s_act)
	s_act = j[37]
	s_act["Sub-Activities"] = j[38:40]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[40])
	k.append(act)
	# Caring for and helping nonhousehold members
	act = j[41]
	act["Sub-Activities"] = [j[42]]
	s_act = j[43]
	s_act["Sub-Activities"] = j[44:46]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[46])
	k.append(act)
	# Work and work-related activities
	act = j[47]
	act["Sub-Activities"] = j[48:53]
	k.append(act)
	# Educational activities
	act = j[53]
	act["Sub-Activities"] = j[54:57]
	k.append(act)
	# Organizational, civic, and religious activities
	act = j[57]
	act["Sub-Activities"] = [j[58]]
	s_act = j[59]
	s_act["Sub-Activities"] = []
	s_s_act = j[60]
	s_s_act["Sub-Activities"] = j[61:66]
	s_act["Sub-Activities"].append(s_s_act)
	s_act["Sub-Activities"].append(j[66])
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[67])
	k.append(act)
	# Leisure and sports
	act = j[68]
	act["Sub-Activities"] = []
	s_act = j[69]
	s_s_act = j[70]
	s_s_act["Sub-Activities"] = j[71:73]
	s_act["Sub-Activities"] = [s_s_act]
	s_s_act = j[73]
	s_s_act["Sub-Activities"] = [j[74]]
	s_act["Sub-Activities"].append(s_s_act)
	s_act["Sub-Activities"].append(j[75])
	act["Sub-Activities"].append(s_act)
	s_act = j[76]
	s_act["Sub-Activities"] = j[77:79]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[79])
	k.append(act)
	# Telephone calls, mail, and emails
	act = j[80]
	act["Sub-Activities"] = [j[81]]
	s_act = j[82]
	s_act["Sub-Activities"] = j[83:85]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[85])
	k.append(act)
	# Other activities, not elsewhere classified
	k.append(j[86])
	# return k
	fj = open("data/{0}.json".format(year), "w+")
	json.dump(k, fj)

get_year_data("2003")