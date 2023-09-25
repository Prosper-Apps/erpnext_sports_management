frappe.listview_settings['Ranking'] = {
    onload: function(listview) {
        // Add a button to the list view
        listview.page.add_menu_item(__('Calculate Rankings'), function() {
            // Call a server method to calculate the rankings
            frappe.call({
                method: 'sports_management.sports_management.doctype.ranking.ranking.calculate_rankings',
                callback: function(response) {
                    // Show a success message
                    frappe.show_alert({
                        message: __('Rankings calculated successfully'),
                        indicator: 'green'
                    });
                    // Refresh the list view
                    listview.refresh();
                }
            });
        });
    }
};
