# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Match(Document):
	# create function when saving a match to calculate the points for each team
	def on_update(self):

		# Get all the matches for the tournament with status completed ordered ascending by date
		matches = frappe.get_all('Match', filters={'tournament': self.tournament, 'status': 'Completed'}, fields=['name', 'home', 'guest', 'full_time_home_result', 'full_time_guest_result', 'date', 'time', 'venue'], order_by='date asc')
		# Get the tournament document win_points, draw_points and loss_points and the tournament teams
		tournament_doc = frappe.get_doc('Tournament', self.tournament)
		win_points = tournament_doc.win_points
		draw_points = tournament_doc.draw_points
		loss_points = tournament_doc.loss_points
		teams = tournament_doc.teams
		
		# for each team set the points to 0
		for team in teams:
			team.rank = 0
			team.played = 0
			team.points = 0
			team.wins = 0
			team.draws = 0
			team.losses = 0
			team.score_for = 0
			team.score_against = 0
			team.difference = 0

		# For each match calculate the points for each team
		for match in matches:
			# Get the home team from teams
			home_team = [team for team in teams if team.team == match.home]
			# Get the guest team from teams
			guest_team = [team for team in teams if team.team == match.guest]
			# Update the home team stats
			home_team[0].played += 1
			home_team[0].score_for += match.full_time_home_result
			home_team[0].score_against += match.full_time_guest_result
			home_team[0].difference += match.full_time_home_result - match.full_time_guest_result
			# Update the guest team stats
			guest_team[0].played += 1
			guest_team[0].score_for += match.full_time_guest_result
			guest_team[0].score_against += match.full_time_home_result
			guest_team[0].difference += match.full_time_guest_result - match.full_time_home_result
			# Update the wins, draws and losses			
			if match.full_time_home_result > match.full_time_guest_result:
				home_team[0].wins += 1
				guest_team[0].losses += 1
				home_team[0].points += win_points
				guest_team[0].points += loss_points
			elif match.full_time_home_result == match.full_time_guest_result:
				home_team[0].draws += 1
				guest_team[0].draws += 1
				home_team[0].points += draw_points
				guest_team[0].points += draw_points				
			else:
				home_team[0].losses += 1
				guest_team[0].wins += 1
				home_team[0].points += loss_points
				guest_team[0].points += win_points
		
		# Assign the rank for each team. The team with the most points is ranked first
		teams = sorted(teams, key=lambda x: x.points, reverse=True)
		for i in range(len(teams)):
			teams[i].rank = i + 1
			teams[i].save()
