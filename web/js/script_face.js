$(document).keypress(function(e) {
    if(e.which == 13) {
        var searchstring  = $("#search").val();
        postPython(searchstring);
    }
});

function postPython(st) {

		$.ajaxSetup({
		    type: "POST",
		    data: {st},
		    dataType: 'json',
		    xhrFields: {
		       withCredentials: true
		    },
		    crossDomain: true,
		    contentType: 'application/json; charset=utf-8'
		});

		$.ajax({
		    url: "http://127.0.0.1:5000/check_selected?"+st,
		    xhrFields: {
		       withCredentials: true
		    },
		}).done(function (data) {
		    console.log(data);
		});
}

