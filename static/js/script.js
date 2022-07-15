function showImg(thisimg) {
	var file = thisimg.files[0];
	if(window.FileReader) {
		var fr = new FileReader();
		
		var showimg = document.getElementById('showimg');
		fr.onloadend = function(e) {
		showimg.src = e.target.result;
	};
	fr.readAsDataURL(file);
	showimg.style.display = 'block';
	showimg.style.width = "300px";
	showimg.style.height = "300px";
	}
}
function showImg2(thisimg) {
	var file = thisimg.files[0];
	if(window.FileReader) {
		var fr = new FileReader();
		
		var showimg = document.getElementById('showimg2');
		fr.onloadend = function(e) {
		showimg.src = e.target.result;
	};
	fr.readAsDataURL(file);

	
	showimg.style.display = 'block';
	showimg.style.width = "300px";
	showimg.style.height = "300px";
	}
}


function sub() {  

	$.ajax({  
			cache: true,  
			type: "POST",  
			url:"http://172.31.4.149:5000/processes",  
			data:$('#formId').serialize(),// 你的formid  
			async: false,  
			error: function(request) {  
				alert("Connection error:"+request.error);  
			},  
			success: function(response) {  

			// $('#loader').append('<img src="' + "static/generate/style.jpeg" + '" width="300" height="300" />');
			  
			//   $("#show1").html(response);
			// $("#loader").html('<img src="' + "static/generate/style.jpeg" + '" width="300" height="300" />');
			// $("#loader").html('<img src="' + "static/generate/style.jpeg" + '" width="300" height="300" />');
			//$("#ig").show();
	
			// alert("SUCCESS!");  
			}  

		   
		});   
	}
// function ck() { 
// $(document).ready(function(){

// 	$(".btn2").click(function(){
// 		$("#ig").show();
// 	});
// 	});

// }
// 	function chartUrl(chartUrl){
    
//     $.ajax({
//         url :chartUrl,             
//           data: {"todo":todo,"CMD":"chartUrl"},
//           type: "GET",
//           contentType: "image/png",
//           dataType: "text",
//         success: function(data) { 
//         	/* alert(data); */
//               $("#imgalign").html('<img src="' + data + '" />');
//         }
//     });
// }