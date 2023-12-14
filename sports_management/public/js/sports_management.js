if (frappe.session.user !== 'Guest') {
    frappe.call({
		method: 'sports_management.sports_management.web_form.my_tournaments.my_tournaments.get_all_website_item_route',
		args: {},
		callback: function(response) {
			var website_item_routes = response.message;
			
			// loop through all website_item_routes
			website_item_routes.forEach(function(website_item_route) {

				// Add a button to the page that links to the website_item_route
				$('<a class="btn btn-primary btn-sm ml-2" href="/' + website_item_route + '">PAY NOW</a>').insertBefore('.webpage-content');

				// Add a message to the page indicating that product is not paid
				$('<div class="alert alert-warning" role="alert">This registration has not been accepted yet. If you did not pay please do.<br/>If you already paid and more than 5 work days passed contact with us.</div>').insertBefore('.webpage-content');
			});
		}
	});
}
