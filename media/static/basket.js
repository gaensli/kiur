$(document).ready(function() {
	//get the basket in case of back/forward button
	$.ajax({
		type:"GET",
		url:"/modify_basket/",
		success: function(response) {
			if (response.success) {
				$("#component-icon").html(response.libs);
				$("#footprint-icon").html(response.mods);
				console.log(response);
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
			url:"/modify_basket/?" + new Date().getTime(),
			data:dataString,
			success: function(response) {
				console.log(response.name);
				if (response.success) {
					$("#component-icon").html(response.libs);
					$("#footprint-icon").html(response.mods);
					//should really make sure it's toggled the right way
					//$(".modify_basket").find("input[value='"+response.name+"']").each( function() {
					//	if($(this).parent().find("input[value='"+response._type+"']")){
					//		$(this).prop("checked", response.in_basket);
					//	}
					//		});
				}	
				else {
					alert("A database problem occured changing the basket! Please contact the administrator.");
				}
			}
		});
		return false;
	});
});
