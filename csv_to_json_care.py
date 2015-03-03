import csv, json

def get_year_data(year): 
	# Note: '#' char in csv strings is a stand-in for a comma
	# What to do with negative time values?
	f = open('data/{0}.csv'.format(year))
	j = []
	headers = ["Activity","Percent Engaged on Weekdays","Percent Engaged on Weekends and Holidays",
	"Average Hours per Weekday","Average Hours per Weekend and Holiday"]
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
	# Caring for and helping others
	act = j[32]
	act["Sub-Activities"] = []
	s_act = j[33]
	s_act["Sub-Activities"] = j[34:37]
	act["Sub-Activities"].append(s_act)
	s_act = j[37]
	s_act["Sub-Activities"] = j[38:40]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[40])
	act["Sub-Activities"].append(j[41])
	s_act = j[42]
	s_act["Sub-Activities"] = [j[43:45]]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[45])
	k.append(act)
	# Work and work-related activities
	act = j[46]
	act["Sub-Activities"] = j[47:52]
	k.append(act)
	# Educational activities
	act = j[52]
	act["Sub-Activities"] = j[53:56]
	k.append(act)
	# Organizational, civic, and religious activities
	act = j[56]
	act["Sub-Activities"] = [j[57]]
	s_act = j[58]
	s_act["Sub-Activities"] = []
	s_s_act = j[59]
	s_s_act["Sub-Activities"] = j[60:65]
	s_act["Sub-Activities"].append(s_s_act)
	s_act["Sub-Activities"].append(j[65])
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[66])
	k.append(act)
	# Leisure and sports
	act = j[67]
	act["Sub-Activities"] = []
	s_act = j[68]
	s_s_act = j[69]
	s_s_act["Sub-Activities"] = j[70:72]
	s_act["Sub-Activities"] = [s_s_act]
	s_s_act = j[72]
	s_s_act["Sub-Activities"] = [j[73]]
	s_act["Sub-Activities"].append(s_s_act)
	s_act["Sub-Activities"].append(j[74])
	act["Sub-Activities"].append(s_act)
	s_act = j[75]
	s_act["Sub-Activities"] = j[76:78]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[78])
	k.append(act)
	# Telephone calls, mail, and emails
	act = j[79]
	act["Sub-Activities"] = [j[80]]
	s_act = j[81]
	s_act["Sub-Activities"] = j[82:84]
	act["Sub-Activities"].append(s_act)
	act["Sub-Activities"].append(j[84])
	k.append(act)
	# Other activities, not elsewhere classified
	k.append(j[85])
	return k
	
# write all info to one JSON file
data = {"2007":[],"2008":[],"2009":[],"2010":[]}
# file won't have years in order because dictionaries don't store with indexes
for year in data:
	data[year] = get_year_data(year)

f = open("data/four_years.json", "w+")
json.dump(data, f)