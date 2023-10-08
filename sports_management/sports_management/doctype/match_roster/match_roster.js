// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Match Roster', {

	// When the role is changed and there is selected team then filter the persons per team and role
	role: function (frm) {

		// Set the team value to empty
		frm.set_value("person", "");
		frm.set_value("position", "");

		// Get the list of Team Roster for the selected team and role
		var team_roster = frappe.db.get_list("Team Roster", {
			filters: [
				["Team Roster", "team", "=", frm.doc.team],
				["Team Roster", "role", "=", frm.doc.role]
			],
			fields: ["person"]
		}).then(function (team_roster) {
			// Set the persons
			frm.set_query("person", function () {
				return {
					"filters": [
						["Person", "name", "in", team_roster.map(function (d) { return d.person; })]
					]
				};
			}
			);
		});
	},

	// When the team is changed, refresh the frame
	team: function (frm) {

		// Set the team value to empty
		frm.set_value("person", "");
		frm.set_value("position", "");

		// Get the list of Team Roster for the selected team and role
		var team_roster = frappe.db.get_list("Team Roster", {
			filters: [
				["Team Roster", "team", "=", frm.doc.team],
				["Team Roster", "role", "=", frm.doc.role]
			],
			fields: ["person"]
		}).then(function (team_roster) {
			// Set the persons
			frm.set_query("person", function () {
				return {
					"filters": [
						["Person", "name", "in", team_roster.map(function (d) { return d.person; })]
					]
				};
			}
			);
		});
	},

	// Limit the team to the team of the match
	match: function (frm) {

		// Set the team value to empty
		frm.set_value("team", "");
		frm.set_value("person", "");
		frm.set_value("position", "");

		// Get the home and guest team on one call
		var teams = frappe.db.get_value("Match", frm.doc.match, ["home", "guest"], function (r) {
			// Set the home team
			frm.set_query("team", function () {
				return {
					"filters": [
						["Team", "name", "in", [r.home, r.guest]]
					]
				};
			}
			);
		});

		// Filter the positions based on selected role
		frm.set_query("position", function () {
			return {
				"filters": [
					["Position", "role", "=", frm.doc.role],
				]
			};
		}
		);

	},

});
