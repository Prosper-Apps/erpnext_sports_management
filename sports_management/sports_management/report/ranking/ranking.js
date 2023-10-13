// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Ranking"] = {
	"filters": [
		// Add tournament filter
		{
			"fieldname": "tournament",
			"label": __("Tournament"),
			"fieldtype": "Link",
			"options": "Tournament",
			"reqd": 1
		},
	]
};
