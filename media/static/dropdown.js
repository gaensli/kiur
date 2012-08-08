$(document).ready(function() {
	createDropDown();
	$(".dropdown dt a").click(function() {
		$(".dropdown dd ul").toggle();
		$(".dropdown dt a img").css({opacity:0.0, visibility:"visible"});
	});

	$(document).bind('click', function(e) {
		var $clicked = $(e.target);
		if (! $clicked.parents().hasClass("dropdown"))
	{
		$(".dropdown dd ul").hide();
		$(".dropdown dt a img").css({opacity:1.0, visibility:"visible"});
	}
	});

	$(".dropdown dd ul li a").click(function() {
		var text = $(this).html();
		$(".dropdown dt a").html(text);
		$(".dropdown dd ul").hide();

		var source = $("#id_models");
		source.val($(this).find("span.value").html())
		$(".dropdown dt a img").css({opacity:1.0, visibility:"visible"});
	});


});

function createDropDown(){
	var source = $("#id_models");
	var selected = source.find("option[selected]");
	var options = $("option", source);

	source.hide();
	$("td#source-cell").hide();

	$("#model-cell").append('<dl id="target" class="dropdown"></dl>')
		$("#target").append('<dt><a href="#"><img class="icon" src="/media/static/' + selected.text() + '-black-icon.png" /><span class="value">' + selected.val() + 
				'</span></a></dt>')
		$("#target").append('<dd><ul></ul></dd>')

		options.each(function(){
			$("#target dd ul").append('<li><a href="#">' + $(this).text() + '<img class="icon" src="/media/static/' + 
				$(this).text() + '-black-icon.png" /><span class="value">' + 
				$(this).val() + '</span></a></li>');
		});
}
