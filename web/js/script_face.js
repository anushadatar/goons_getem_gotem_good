$(document).keypress(function(e) {
    if(e.which == 13) {
        var searchstring  = $("#search").val();
        xdr("http://127.0.0.1:5000/check_selected","POST",JSON.stringify(searchstring),getFStat,errThrow)
        //postPython(searchstring);
    }
});

function getFStat(x) {
	alert(x);
}

function errThrow(x) {
	alert("Failed to retreive data.");
}

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
		    data: {query : st}
		}).done(function (data) {
		    console.log(data);
		});
}

function xdr(url, method, data, callback, errback) {
    var req;
    
    if(XMLHttpRequest) {
        req = new XMLHttpRequest();

        if('withCredentials' in req) {
            req.open(method, url, true);
            req.onerror = errback;
            req.onreadystatechange = function() {
                if (req.readyState === 4) {
                    if (req.status >= 200 && req.status < 400) {
                        callback(req.responseText);
                    } else {
                        errback(new Error('Response returned with non-OK status'));
                    }
                }
            };
            req.send(data);
        }
    } else if(XDomainRequest) {
        req = new XDomainRequest();
        req.open(method, url);
        req.onerror = errback;
        req.onload = function() {
            callback(req.responseText);
        };
        req.send(data);
    } else {
        errback(new Error('CORS not supported'));
    }
}