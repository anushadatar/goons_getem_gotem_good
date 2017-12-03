
var config = {
    apiKey: "AIzaSyCLMTgHQbT0qkFjNnF6VyFEC8r7xZgjNms",
    authDomain: "newsblind-1.firebaseapp.com",
    databaseURL: "https://newsblind-1.firebaseio.com",
  };

firebase.initializeApp(config);	
var ref = firebase.database();

var urlDest = "";

function finalURL(x) {
	n = x.rfind('/');
}

$( "#yes" ).click(function() {

});


$( "#no" ).click(function() {
  
});

function addToFirebase(url, condition) {
	url_ending = finalURL(url);

}

$(document).keypress(function(e) {
    if(e.which == 13) {
        var searchstring  = $("#search").val();
        urlDest=searchstring;
        $("#entry_main").fadeOut(100);
        $("#loading_main").fadeIn(1000);
        xdr("http://127.0.0.1:5000/check_selected","POST",JSON.stringify(searchstring),getFStat,errThrow)
    }
});


function getFStat(x) {

	xx = JSON.parse(JSON.parse(x));

	$("#loading_main").fadeOut(100);
	
	$("#status_main").fadeIn(1000);



	$( "#bar" ).animate({
	    width: ((Math.round(10*Math.abs(xx.final_score*100)))/10).toString()+'%',
	    opacity: "+=0.1"
	  }, 500, function() {
	    // Animation complete.
	  });

	if(xx.final_score < 0) {
		$("#status").attr("class","reliable");
		$("#status").text("Credible");
	} else if (xx.final_score >= 0 && xx.final_score < 0.5) {
		$("#status").attr("class","questionable");
		$("#status").text("Questionable");
	} else if (xx.final_score >= 0.5) {
		$("#status").attr("class","fake");
		$("#status").text("Fake");
	} else {
		$("#status").attr("class","unknown");
	}
	
	$("#subbar").text(((Math.round(10*Math.abs(xx.final_score*100)))/10).toString()+'%');
	if(xx.final_score <= 0) {
		$("#walnut").text("We are " + ((Math.round(10*Math.abs(xx.final_score*100)))/10).toString()+'%' + " confident the provided site is a credible source.");
	} else {
		$("#walnut").text("We are " + ((Math.round(10*Math.abs(xx.final_score*100)))/10).toString()+'%' + " confident the provided site is an untrustworthy source.");
	}
	
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