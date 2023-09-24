# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.website.website_generator import WebsiteGenerator

class Tournament(WebsiteGenerator):
	def get_context(self, context):
		teams = self.teams
		# for each team get it's picture
		for team in teams:
			team.picture = frappe.get_value('Team', team.team, 'picture')
			team.route = frappe.get_value('Team', team.team, 'route')
			
		context.rankings = sorted(teams, key=lambda x: x.rank, reverse=False)

@frappe.whitelist()
def create_matches(tournament):
	# Get the tournament document
	tournament_doc = frappe.get_doc('Tournament', tournament)
	schedule_type = tournament_doc.schedule_type
	game_day_interval = tournament_doc.game_day_interval
	starting_day = tournament_doc.starting_day
	starting_day = generate_round(tournament, tournament_doc, 1, starting_day, game_day_interval)
	if schedule_type == "Double round robin tournament":
		generate_round(tournament, tournament_doc, 2, starting_day + datetime.timedelta(days=game_day_interval), game_day_interval)

	# Send a frappe message to the user
	frappe.msgprint('Matches created successfully!')


def generate_round(tournament, tournament_doc, round_number, starting_day, game_day_interval=7):

	# Get the necessary fields from the tournament document
	time_for_games = tournament_doc.time_for_games
	teams = tournament_doc.teams

	# Create a list of team names
	team_names = [team.team for team in teams]

	# If round_number is 2, reverse order of team_names
	if round_number == 2:
		team_names = team_names[::-1]

	# Create a list of game days
	num_teams = len(team_names)
	num_rounds = num_teams - 1 if num_teams % 2 == 0 else num_teams
	game_days = [starting_day + datetime.timedelta(days=i*game_day_interval) for i in range(num_rounds)]
	  
	rounds = circle_method(num_teams)
	  
	# Create the matches
	for r in range(len(rounds)):
		game_day_doc = frappe.new_doc('Game Day')
		game_day_doc.tournament = tournament
		game_day_doc.start = game_days[r]
		game_day_doc.insert()
		for match in rounds[r]:
			match_doc = frappe.new_doc('Match')
			match_doc.tournament = tournament
			match_doc.game_day = game_day_doc.name
			match_doc.home = team_names[match[0]-1]
			match_doc.guest = team_names[match[1]-1]
			match_doc.venue = frappe.get_value('Team', match_doc.home, 'venue')
			match_doc.date = game_days[r]
			match_doc.time = time_for_games
			match_doc.insert()

	return game_days[r]
	
def circle_method(teams):

	# If there is an odd amount of teams,
	# there will be 1 more 'non-existent' team, standing for no match-up
	rounds = teams - 1
	if teams % 2 == 1:
		rounds = teams
	# Matches per round
	mpr = int((rounds+1) / 2)

	# Table of teams [1, 2, ..., n]
	t = []
	for i in range(rounds+1):
		t.append(i+1)

	# Stores the rounds with the corresponding matches inside
	# e.g.: [[(1, 4), (2, 3)], [(1, 3), (4, 2)], [(1, 2), (3, 4)]]
	matches = []
	for r in range(rounds):
		matches.append([])
		for m in range(mpr):
			matches[r].append((t[m], t[-1-m]))
		t.remove(rounds-r+1)
		t.insert(1, rounds-r+1)

	# If there is an odd amount of teams,
	# there will be 1 more 'non-existent' team, standing for no match-up
	# Remove this non-existent team from the matches
	if teams % 2 == 1:
		for r in range(len(matches)):
			for m in range(len(matches[r])):
				if matches[r][m][0] == teams + 1 or matches[r][m][1] == teams + 1:
					del matches[r][m]
					break

	return matches
	