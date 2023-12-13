frappe.ready(function() {

	frappe.call({
		method: 'sports_management.sports_management.web_form.my_tournaments.my_tournaments.get_website_item_route',
		args: {
			"team_tournament_name": frappe.web_form.doc.name
		},
		callback: function(response) {
			var website_item_route = response.message;

			// if website_item_route is not set, then return
			if (!website_item_route) return;

			// Add a button to the page that links to the website_item_route
			$('<a class="btn btn-primary btn-sm ml-2" href="/' + website_item_route + '">PAY NOW</a>').appendTo('.web-form-actions');

			// Add a message to the page indicating that product is not paid
			$('<div class="alert alert-warning" role="alert">This registration has not been accepted yet. If you did not pay please do.<br/>If you already paid and more than 5 work days passed contact with us.</div>').appendTo('.section-body');
		}
	});
});