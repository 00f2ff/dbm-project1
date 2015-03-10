#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, logging, urllib, json, csv, re
from webapp2_extras import jinja2

# csv_2003 = open('data/2003.csv')
# json_2003 = []
# headers = ["Activity","Total%","Men%","Women%","TotalH","MenH","WomenH"]
# reader = csv.DictReader(csv_2003, headers)
# for row in reader:
# 	json_2003.append(row)

# logging.info(json_2003)

# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):

	@webapp2.cached_property
	def jinja2(self):
		# Returns a Jinja2 renderer cached in the app registry.
		return jinja2.get_jinja2(app=self.app)

	def render_response(self, _template, **context):
		# Renders a template and writes the result to the response.
		rv = self.jinja2.render_template(_template, **context)
		self.response.write(rv)

class MainHandler(BaseHandler):
	def get(self): # right now I'm loading JSON on the client because json.encode still isn't working
		# year = "2003" # I need to loop through
		# fp = open("data/{0}.json".format(year))
		# response = json.load(fp)
		# logging.info(type(response))
		# # j_2003 = self.get_year_data('2003')
		# # context = {'data':json.encode(response)}
		# context = {'data':response}
		# f = open('data/four_years.json')
		# data = json.load(f)
		data = self.data_passer()
		# logging.info(data)
		context = {'data':data}
		self.render_response('index_old.html', **context)

	def data_passer(self):
		# create data object containing all year information
		# data = {"2006":[],"2007":[],"2008":[],"2009":[],"2010":[],"2011":[],"2012":[],"2013":[]}
		data = [ ["2006",[]], ["2007",[]], ["2008",[]], ["2009",[]], ["2010",[]], ["2011",[]], ["2012",[]], ["2013",[]] ]
		for y in xrange(len(data)):
			# array with year = data for that year
			data[y][1] = self.get_year_data(data[y][0]) 
		# Convert into new data structure
		data = self.regenerate_data(data)
		logging.info(data)

		return data

	def regenerate_data(self,data):
		# initialize
		weekend = self.add_activities("Weekend")
		weekday = self.add_activities("Weekday")
		#new = [weekend, weekday]
		# iterate through years
		for y in xrange(len(data)):
			# iterate through activities array (same for both weekend and weekday)
			for a in xrange(len(weekend)):
				# check if education (special case)
				if weekend[a][0] == "Educational Activities":
					# create arrays of all of the education data (see comment below)
					# education of [a][1] is an array of [ [], [] ], with percent being index 0 and hours 1
					weekend[a][1][0].append({"year":data[y][0], "percent":data[y][1][a]["Percent Engaged on Weekends and Holidays"]})
					weekend[a][1][1].append({"year":data[y][0], "hours":data[y][1][a]["Average Hours per Weekend and Holiday"]})
					weekday[a][1][0].append({"year":data[y][0], "percent":data[y][1][a]["Percent Engaged on Weekdays"]})
					weekday[a][1][1].append({"year":data[y][0], "hours":data[y][1][a]["Average Hours per Weekday"]})
					# weekend[a][1][0]["year"] = data[y][0]
					# weekend[a][1][0]["percent"] = data[y][1][a]["Percent Engaged on Weekends and Holidays"]
					# weekend[a][1][1]["year"] = data[y][0]
					# weekend[a][1][1]["hours"] = data[y][1][a]["Average Hours per Weekend and Holiday"]

					# weekday[a][1][0]["year"] = data[y][0]
					# weekday[a][1][0]["percent"] = data[y][1][a]["Percent Engaged on Weekdays"]
					# weekday[a][1][1]["year"] = data[y][0]
					# weekday[a][1][1]["hours"] = data[y][1][a]["Average Hours per Weekday"]
					# we = []
					# wd = []
					# we.append([data[y][0], data[y][1][a]["Percent Engaged on Weekends and Holidays"]])
					# we.append([data[y][0], data[y][1][a]["Average Hours per Weekend and Holiday"]])
					# wd.append([data[y][0], data[y][1][a]["Percent Engaged on Weekdays"]])
					# wd.append([data[y][0], data[y][1][a]["Average Hours per Weekday"]])
					# weekend[a][1].append(we)
					# weekday[a][1].append(wd)
				else:
					# array for the activity for the weekend = [year, engagement value for that activity]
					# weekend[a][1]["year"] = data[y][0]
					# weekend[a][1]["percent"] = data[y][1][a]["Percent Engaged on Weekends and Holidays"]
					weekend[a][1].append({"year":data[y][0], "percent":data[y][1][a]["Percent Engaged on Weekends and Holidays"]})
					# do same for weekday
					# weekday[a][1]["year"] = data[y][0]
					# weekday[a][1]["percent"] = data[y][1][a]["Percent Engaged on Weekdays"]
					weekday[a][1].append({"year":data[y][0], "percent":data[y][1][a]["Percent Engaged on Weekdays"]})
		return {"Weekend":weekend, "Weekday":weekday}

	# Takes a name, e.g. weekend or weekday, and creates an array with all important activites in it
	def add_activities(self,name):
		# d = {name: [{"Personal Activities": []}, {"Health-Related Self Care": []}, {"Watching TV": []}, 
		# {"Animals and Pets": []}, {"Travel Related to Household Activities": []}, {"Food Preparation": []},
		# {"Grocery Shopping": []}, {"Financial Services and Banking": []}, {"Organizational, Civic and Religious Activites": []},
		# {"Religious and Spiritual Activities": []}, {"Educational Activities": []}, {"Working and Work-Related Activities": []},
		# {"Job Search and Interviewing": []}, {"Travel Related to Work": []}]}
		d = [["Personal Activities",[]], 
		["Health-Related Self Care", []], 
		["Watching TV", []], 
		["Animals and Pets", []], 
		["Travel Related to Household Activities", []], 
		["Food Preparation", []],
		["Grocery Shopping", []], 
		["Financial Services and Banking", []], 
		["Organizational, Civic and Religious Activites", []],
		["Religious and Spiritual Activities", []], 
		["Educational Activities", [ [], [] ]], 
		["Working and Work-Related Activities", []],
		["Job Search and Interviewing", []], 
		["Travel Related to Work", []]]
		# Format: each index corresponds with the index data is accessed in get_year_data
		return d


	def get_year_data(self,year): 
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
		# Personal Activities
		k.append(j[4])
		k.append(j[3])
		# Leisure
		k.append(j[73])
		# Home Making
		k.append(j[16])
		k.append(j[19])
		k.append(j[11])
		k.append(j[22])
		# Finances
		k.append(j[24])
		# Religion
		k.append(j[56])
		k.append(j[57])
		# Education
		k.append(j[52])
		# Work
		k.append(j[46])
		k.append(j[50])
		k.append(j[51])
		# logging.info(k)
		return k

	def post(self):
		context = {}
		self.render_response('index_old.html', **context)

app = webapp2.WSGIApplication([
    ('.*', MainHandler)
], debug=True)
