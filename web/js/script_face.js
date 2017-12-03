
$(document).on( "click", "#yes", function() {
  	var searchstring = $("search").val();
  	console.log("yes");
    xdr("http://127.0.0.1:5000/update_polls_pos", "POST", searchstring, getResults, errThrow)
});

$(document).on( "click", "#no", function() {
  	var searchstring = $("search").val();
  	console.log("no");
    xdr("http://127.0.0.1:5000/update_polls_neg", "POST", searchstring, getResults, errThrow)
});

$(document).keypress(function(e) {
    if(e.which == 13) {
        var searchstring  = $("#search").val();
        urlDest=searchstring;
        $("#entry_main").fadeOut(100);
        $("#loading_main").fadeIn(1000);
        xdr("http://127.0.0.1:5000/check_selected","POST",JSON.stringify(searchstring),getFStat,errThrow)
    }
});

function getResults(x) {
    $(".left").fadeOut();
    console.log(x);
    a = parseInt(str(x));
    console.log(a);
}


function getFStat(x) {

	xx = JSON.parse(JSON.parse(x));

	$("#loading_main").fadeOut(100);

	$("#status_main").fadeIn(1000);
	console.log(xx.grammar_metric);


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

  if (xx.sentiment_metric < 0){
    $("#metric0").attr("class","reliable1");
    $("#metricPercent0").text(Math.round(Math.abs(xx.sentiment_metric) * 10).toString() + "%");
    $("metricText0").text("This source is relatively unbiased in stance and neutral in tone");
  } else {
    $("#metric0").attr("class","fake1");
    $("#metricPercent0").text(Math.round(Math.abs(xx.sentiment_metric) * 10).toString() + "%");
    $("metricText0").text("This source is relatively biased in stance and emotional in tone");
  }

  if (xx.title_metric > 0){
    $("#metric1").attr("class","fake1");
    $("#metricPercent1").text("Clickbait");
    $("#metricText1").text("This article is likely clickbait");
  } else {
    $("#metric1").attr("class","reliable1");
    $("#metricPercent1").text("Not Clickbait");
    $("#metricText1").text("This article is probably not clickbait");
  }

  if (xx.grammar_metric == 0){
    $("#metric2").attr("class","reliable1");
    $("#metricPercent2").text("Normal");
    $("#metricText2").text("The grammar structure of this article is relatively strong");
  } else {
    $("#metric2").attr("class","fake1");
    $("#metricPercent2").text("Poor");
    $("#metricText2").text("The grammar structure of this article is relatively poor");
  }

  if (xx.domain_score < 0){
    $("#metric3").attr("class","reliable1");
    $("#metricPercent3").text(Math.round(Math.abs(xx.domain_score) * 6.6666).toString() + "%");
    $("#metricText3").text("The article's domain isn't widely known to be inauthentic");
  } else {
    $("#metric3").attr("class","fake1");
    $("#metricPercent3").text(Math.round(Math.abs(xx.domain_score) * 6.6666).toString() + "%");
    $("#metricText3").text("The article's domain is known to be inauthentic");
  }

  if (xx.TLD_score < 0){
    $("#metric4").attr("class","reliable1");
    $("#metricPercent4").text("Standard TLD");
    $("#metricText4").text("The article's Top Level Domain is a standard one and likely very safe");
  } else if (xx.TLD_score < 10){
    $("#metric4").attr("class","questionable1");
    $("#metricPercent4").text("Non-Standard TLD");
    $("#metricText4").text("The article's Top Level Domain is a non-standard one");
  } else {
    $("#metric4").attr("class","fake1");
    $("#metricPercent4").text("Dangerous TLD");
    $("#metricText4").text("The article's Top Level Domain is known to be qutie dangerous");
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
