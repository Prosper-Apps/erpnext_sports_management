// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Venue', {
	// Upon change of the venue_name create a short name of maximun 3 characters and being capital case, and set it to the field short_name
	// I want the short name to be the first letter of each word in the venue_name
	// If less than three words then take the first three letters of the first two words
	// If only one word then take the first three letters of the word
	// If no words then leave blank
	// The maximun length of the short name is 3 characters
	venue_name: function(frm) {
		var venue_name = frm.doc.venue_name;
		var short_name = "";
		var words = venue_name.split(" ");
		if (words.length > 0) {
			if (words.length == 1) {
				short_name = words[0].substring(0, 3);
			} else if (words.length == 2) {
				short_name = words[0].substring(0, 1) + words[1].substring(0, 2);
			} else {
				short_name = words[0].substring(0, 1) + words[1].substring(0, 1) + words[2].substring(0, 1);
			}
		}
		frm.set_value("short_name", short_name.toUpperCase());
	}
});
