# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.website.website_generator import WebsiteGenerator

class Tournament(WebsiteGenerator):
	def get_context(self, context):

		# Define the title of the page
		context.title = self.tournament_name

		# Define breadcrumbs
		context.parents = [{"name": "Home", "route":"/"}, {"name": "Tournaments", "route":"/tournaments"}]

		# Get the league name and route and assignt to context. Use frappe.get_all
		context.league_name = frappe.get_value('League', self.league, ['league_name'])
		context.league_route = frappe.get_value('League', self.league, ['route'])

		# Get the rankings of the tournament
		teams = frappe.get_all('Ranking', 
			filters={'tournament': self.name, 'disabled': 0}, fields=['team', 'team.team_name', 'team.route', 'team.picture', 'rank', 'played', 'wins', 'draws', 'losses', 'points', 'score_for', 'score_against', 'difference'], order_by='rank')	
			
		context.rankings = sorted(teams, key=lambda x: x.rank, reverse=False)

		# Get the game days with name and route
		context.game_days = frappe.get_all('Game Day', filters={'tournament': self.name}, fields=['name', 'route', 'start'], order_by='start')

		# Get the matches with name and route
		context.matches = frappe.get_all('Match', filters={'tournament': self.name}, fields=['name', 'route', 'home', 'home_name', 'guest', 'guest_name', 'date', 'time', 'venue', 'full_time_home_result', 'full_time_guest_result', 'status'], order_by='date')

		# Get the related website item
		if self.website_item:
			context.website_item = frappe.get_doc('Website Item', self.website_item)

@frappe.whitelist()
def create_matches(tournament):
	# Delete all the matches and game days of the tournament
	delete_matches(tournament, False)

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

# Create a function that will delete all the matches and game days of a tournament
# Before deleting the matches, check if there are any match roster entries for the matches and delete them.
# The same do for match referees and match events
@frappe.whitelist()
def delete_matches(tournament, show_message=True):
	# Get the matches of the tournament
	matches = frappe.get_all('Match', filters={'tournament': tournament}, fields=['name'])
	# Delete the match roster entries
	for match in matches:
		frappe.db.sql("delete from `tabMatch Roster` where `match`=%s", match.name)
		frappe.db.sql("delete from `tabMatch Referee` where `match`=%s", match.name)
		frappe.db.sql("delete from `tabMatch Event` where `match`=%s", match.name)
	# Delete the matches
	frappe.db.sql("delete from `tabMatch` where `tournament`=%s", tournament)
	# Delete the game days
	frappe.db.sql("delete from `tabGame Day` where `tournament`=%s", tournament)
	# Send a frappe message to the user
	if show_message:
		frappe.msgprint('Matches deleted successfully!')

def generate_round(tournament, tournament_doc, round_number, starting_day, game_day_interval=7):

	# Get the necessary fields from the tournament document
	time_for_games = tournament_doc.time_for_games
	# Get the ranking of the tournament
	rankings = frappe.get_all('Ranking', filters={'tournament': tournament, 'disabled': 0}, fields=['team', 'rank'])

	# Create a list of team names
	team_names = [team.team for team in rankings]

	# If round_number is 2, reverse order of team_names
	if round_number == 2:
		team_names = team_names[::-1]

	# Create a list of game days
	num_teams = len(team_names)
	if num_teams < 3:
		frappe.throw('You need at least 3 teams to create a tournament!')
	num_rounds = num_teams - 1 if num_teams % 2 == 0 else num_teams
	game_days = [starting_day + datetime.timedelta(days=i*game_day_interval) for i in range(num_rounds)]
	  
	rounds = circle_method(num_teams)
	  
	# Create the matches
	for r in range(len(rounds)):
		game_day_doc = frappe.new_doc('Game Day')
		game_day_doc.tournament = tournament
		game_day_doc.start = game_days[r]
		game_day_doc.published = 1
		game_day_doc.insert()
		for match in rounds[r]:
			match_doc = frappe.new_doc('Match')
			match_doc.tournament = tournament
			match_doc.game_day = game_day_doc.name
			match_doc.home = team_names[match[0]-1]
			match_doc.guest = team_names[match[1]-1]
			match_doc.date = game_days[r].strftime('%Y-%m-%d')
			match_doc.time = time_for_games
			match_doc.published = 1
			match_doc.insert()
			# Update route with match name. Do it with frappe.db.set_value
			if match_doc.route == None:
				frappe.db.set_value('Match', match_doc.name, 'route', match_doc.name)

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
	
@frappe.whitelist()
def calculate_rankings(tournament, send_message=False):
	# Get all the matches for the tournament with status completed ordered ascending by date
	matches = frappe.get_all('Match', filters={'tournament': tournament, 'status': 'Completed'}, fields=['name', 'home', 'guest', 'full_time_home_result', 'full_time_guest_result', 'date', 'time', 'venue'], order_by='date asc')
	# Get the tournament document win_points, draw_points and loss_points and the tournament rankings
	tournament_doc = frappe.get_doc('Tournament', tournament)
	win_points = tournament_doc.win_points
	draw_points = tournament_doc.draw_points
	loss_points = tournament_doc.loss_points
	# Get the ranking of the tournament
	rankings = frappe.get_all('Ranking', filters={'tournament': tournament}, fields=['name', 'team', 'rank', 'played', 'wins', 'draws', 'losses', 'points', 'score_for', 'score_against', 'difference'])	
	
	# for each team set the points to 0
	for ranking in rankings:
		ranking.rank = 0
		ranking.played = 0
		ranking.points = 0
		ranking.wins = 0
		ranking.draws = 0
		ranking.losses = 0
		ranking.score_for = 0
		ranking.score_against = 0
		ranking.difference = 0

	# For each match calculate the points for each team
	for match in matches:
		# Get the home team from rankings
		home_team = [team for team in rankings if team.team == match.home]
		# Get the guest team from rankings
		guest_team = [team for team in rankings if team.team == match.guest]
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
	rankings = sorted(rankings, key=lambda x: x.points, reverse=True)
	for i in range(len(rankings)):
		rankings[i].rank = i + 1		
		# Save the ranking with frappe.db.set_value. Include all the calculated fields but use only one command
		frappe.db.set_value('Ranking', rankings[i].name, {
			'rank': rankings[i].rank,
			'played': rankings[i].played,
			'wins': rankings[i].wins,
			'draws': rankings[i].draws,
			'losses': rankings[i].losses,
			'points': rankings[i].points,
			'score_for': rankings[i].score_for,
			'score_against': rankings[i].score_against,
			'difference': rankings[i].difference
		})

	# Calculate all persons points
	# Get a list of the match rosters for the tournament
	match_rosters = frappe.get_all("Match Roster", filters={"tournament": tournament}, fields=["person", "team", "starting_lineup"])
	for match_roster in match_rosters:
		# Get a list of the rankings that the team is a member of
		rankings = frappe.get_all("Ranking", filters={"team": match_roster.team}, fields=["points"])
		# Calculate the person points
		person_points = sum([ranking.points for ranking in rankings])
		# Save the person points
		frappe.db.set_value("Person", match_roster.person, "points", person_points)
		
	# Send a frappe message to the user
	if send_message:
		frappe.msgprint('Rankings calculated successfully!')

def get_list_context(context=None):

	context.update(
		{
			"show_sidebar": False,
			"show_search": True,
			"no_breadcrumbs": False,
			"title": "Tournaments",
			"parents": [{"name": "Home", "route":"/"}],
			"filters": {
				"published": True
			},
			"order_by": "ordering asc"
		}
	)
