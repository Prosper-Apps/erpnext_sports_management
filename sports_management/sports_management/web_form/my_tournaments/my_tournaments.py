import frappe

def get_context(context):
	# Get the current user
	current_user = frappe.session.user

	# Get all team_tournaments where the current user is the owner
	team_tournaments = frappe.get_all('Team Tournament', filters={'owner': current_user}, fields=['*'])

	# Get the Rankinkgs for each team_tournament
	for team_tournament in team_tournaments:
		rankings = frappe.get_all('Ranking', filters={'team': team_tournament['team']}, fields=['*'])
		# Get the first ranking
		if rankings:
			ranking = rankings[0]
			# If the ranking disabled get the tournament name
			if ranking['disabled']:
				tournament = frappe.get_doc('Tournament', ranking['tournament'])
				# Get the website item route
				context.website_item_route = frappe.get_doc('Website Item', tournament.website_item).route
		else:
			context.website_item_route = None

	pass

@frappe.whitelist(allow_guest=False)
def get_website_item_route(team_tournament_name):
	website_item_route = None

	# Get the tournament name
	team_tournament = frappe.get_doc('Team Tournament', team_tournament_name)
	rankings = frappe.get_all('Ranking', filters={'team': team_tournament.team, "tournament": team_tournament.tournament, "disabled": 1}, fields=['*'])
	# Get the first ranking
	if rankings:
		ranking = rankings[0]
		# If the ranking disabled get the tournament name
		tournament = frappe.get_doc('Tournament', ranking['tournament'])
		# Get the website item route
		website_item_route = frappe.get_doc('Website Item', tournament.website_item).route

	return website_item_route
		
@frappe.whitelist(allow_guest=False)
def get_all_website_item_route():
	website_item_routes = []

	# Get all team_tournaments where the current user is the owner
	team_tournaments = frappe.get_all('Team Tournament', filters={'owner': frappe.session.user}, fields=['*'])

	# Get the Rankinkgs for each team_tournament
	for team_tournament in team_tournaments:
		rankings = frappe.get_all('Ranking', filters={'team': team_tournament['team']}, fields=['*'])
		# Get the first ranking
		if rankings:
			ranking = rankings[0]
			# If the ranking disabled get the tournament name
			if ranking['disabled']:
				tournament = frappe.get_doc('Tournament', ranking['tournament'])
				# Get the website item route
				website_item_routes.append(frappe.get_doc('Website Item', tournament.website_item).route)

	return website_item_routes