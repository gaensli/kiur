$(document).ready(function() {
	//get the basket in case of back/forward button
	$.ajax({
		type:"GET",
			url:"/modify_basket/?" + new Date().getTime(),
		success: function(response) {
			if (response.success) {
				$("#component-icon").html(response.libs);
				$("#footprint-icon").html(response.mods);
			}
			else {
				alert("A database problem occured querying the basket! Please contact the administrator.");
			}
		}});
	//modify basket on toggle buttons
	$(".modify_basket").submit(function(e) {
		var dataString = $(this).serialize();
		$.ajax({
			type:"POST",
			data:dataString,
			url:"/modify_basket/",
			success: function(response) {
				if (response.success) {
					$("#component-icon").html(response.libs);
					$("#footprint-icon").html(response.mods);
					$(".modify_basket").find("input[value='"+response.name+"']").each( function() {
						if($(this).parent().find("input[value='"+response._type+"']")){
							if (response.in_basket) {
								$(this).parent().find("input:submit").attr("value", "remove from basket").css("border-style", "inset");
							}
							else {
								$(this).parent().find("input:submit").attr("value", "add to basket").removeAttr("style");
							}

						}
							});
				}	
				else {
					alert("A database problem occured changing the basket! Please contact the administrator.");
				}
			}
		});
		return false;
	});
});
