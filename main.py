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
		logging.info(data)
		context = {'data':data}
		self.render_response('index.html', **context)

	def data_passer(self): # decides which data to pass to client
		# create data object containing all year information
		data = {"2007":[],"2008":[],"2009":[],"2010":[]}
		for year in data:
			data[year] = self.get_year_data(year)
		years = ["2007","2008","2009","2010"]
		passing = []
		num_activities = len(data["2007"]) # arbitrary year
		for i in xrange(num_activities):
			passing.append(self.get_data_for_activity(data,i,years,
				"Average Hours per Weekend and Holiday",True))
		return passing


	# Returns [activity, [value per year]]
	def get_data_for_activity(self,data,index,years,key,sub_activity):
		# TODO: figure out how to recurse through this
		d = []
		for year in years:
			info = {}
			info["year"] = year
			info["value"] = data[year][index][key]
			d.append(info)
		return [data[years[0]][index]["Activity"], d]

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

	def post(self):
		context = {}
		self.render_response('index.html', **context)

app = webapp2.WSGIApplication([
    ('.*', MainHandler)
], debug=True)
