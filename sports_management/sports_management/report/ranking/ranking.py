# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("Team") + ":Link/Team",
        _("Team Name") + ":Data",
        _("Rank") + ":Int",
        _("Played") + ":Int",
        _("Wins") + ":Int",
        _("Draws") + ":Int",
        _("Losses") + ":Int",
        _("Points") + ":Int",
        _("Score For") + ":Int",
        _("Score Against") + ":Int",
        _("Difference") + ":Int"
    ]

def get_data(filters):
    # Get the rankings of the tournament
    teams = frappe.get_all('Ranking', 
        filters={'tournament': filters.tournament}, fields=['team', 'team.team_name', 'team.route', 'team.picture', 'rank', 'played', 'wins', 'draws', 'losses', 'points', 'score_for', 'score_against', 'difference'], order_by='rank')	
        
    rankings = sorted(teams, key=lambda x: x.rank, reverse=False)

    return rankings