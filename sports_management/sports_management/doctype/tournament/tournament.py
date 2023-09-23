# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.model.document import Document

class Tournament(Document):
	pass

@frappe.whitelist()
def create_matches(tournament):
	# Get the tournament document
	tournament_doc = frappe.get_doc('Tournament', tournament)

	# Get the necessary fields from the tournament document
	schedule_type = tournament_doc.schedule_type
	time_for_games = tournament_doc.time_for_games
	game_day_interval = tournament_doc.game_day_interval
	starting_day = tournament_doc.starting_day
	teams = tournament_doc.teams

	# Calculate the number of rounds based on the number of teams
	num_teams = len(teams)
	num_rounds = num_teams - 1 if num_teams % 2 == 0 else num_teams

	# Create a list of team names
	team_names = [team.team for team in teams]

	# Create a list of game days
	game_days = []
	for i in range(num_rounds):
		game_days.append(starting_day)
		starting_day += datetime.timedelta(days=game_day_interval)

	# Create a list of matches for each round
	matches = []
	for i in range(num_rounds):
		round_matches = []
		for j in range(num_teams // 2):
			home_team = team_names[j]
			away_team = team_names[num_teams - j - 1]
			round_matches.append((home_team, away_team))
		matches.append(round_matches)

		# Rotate the team names for the next round
		team_names = [team_names[0]] + [team_names[-1]] + team_names[1:-1]

	# Create Game Day and Match documents and save them
	for game_day in game_days:
		game_day_doc = frappe.new_doc('Game Day')
		game_day_doc.tournament = tournament
		game_day_doc.start = game_day
		game_day_doc.end = game_day
		game_day_doc.insert()

		for home_team, away_team in matches[i]:
			match_doc = frappe.new_doc('Match')
			match_doc.tournament = tournament
			match_doc.game_day = game_day_doc.name
			match_doc.home = home_team
			match_doc.guest = away_team
			match_doc.date = game_day
			match_doc.insert()
	
	# Send a frappe message to the user
	frappe.msgprint('Matches created successfully!')