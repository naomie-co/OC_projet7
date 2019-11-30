//initialize the leaflet map
var mymap = L.map('mapid');

//animate the progress bar
function progress() {		
var progressBar = $('.progress-bar');
var percentVal = 0;
window.setInterval(function(){
 	document.getElementById("progress").style.opacity=1;
  	percentVal += 25;
    progressBar.css("width", percentVal+ '%').attr("aria-valuenow", percentVal+ '%').text(percentVal+ '%'); 
    if (percentVal >= 101)
	    {
	       document.getElementById("progress").style.opacity=0; 
	    }
	}, 500);
	}     

//initialize the click or enter button to call the search function
$("button#btn").click(function(){progress(), search()});
$("input#question").keydown(function(event){
    if (event.key === "Enter") {
    	progress(), search()
    }})

function search(){
				
	//The question is display in the page
	var question = document.createElement("p");
    question.setAttribute("class", "userContainer");
    var dialogue = document.getElementById("answer");
    question.textContent = $("input#question").val();
    dialogue.insertBefore(question, dialogue.childNodes[0]);

    //An AJAX request is sent to the url /test_ajax/
    $.ajax({
        url: "/test_ajax/",
        type: "POST",
        data: {"question": $("input#question").val()},
		

      //API Data are sent back to the template  
        success: function(resp){

           //creates <p> elements to insert the answer in the answer's div                     
            var address = document.createElement("p");
            address.textContent = "Bien sûr mon poussin ! Voici ce que je trouve : " + resp.address;
            address.setAttribute("class", "botContainer");
            var answer = document.createElement("p");
            answer.textContent = "J'ai quelque chose à ajouter : " + resp.final_answer;
            answer.setAttribute("class", "botContainer");
            var wiki_link = document.createElement("a");
            wiki_link.textContent = "Pour en savoir plus, tu peux cliquer sur ce lien";
            wiki_link.setAttribute("class", "botContainer");
            wiki_link.href = resp.link;
            var dialogue = document.getElementById("answer");
            dialogue.insertBefore(address, dialogue.childNodes[1]);
            dialogue.insertBefore(answer, dialogue.childNodes[2]);
            dialogue.insertBefore(wiki_link, dialogue.childNodes[3]);

           //Use the request data to update the map and displays it
            var lat = parseFloat(resp.lat);
            var long = parseFloat(resp.long);
            console.log(resp);
            console.log(lat, long);
        	var show = document.getElementById("mapid");
        	show.style.opacity = 1;
       
			//Use invalidateSize() to update the leaflet map
            mymap.invalidateSize().setView([lat, long], 13);
            var marker = L.marker([lat, long]).addTo(mymap);
            L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibmFvbWllLWNvIiwiYSI6ImNrMjR3aGI3dzFlZDAzbG55d283NjZxazMifQ.08l7cYOS_a-aGy_mfrMRAw', {
              attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
              maxZoom: 18,
              id: 'mapbox.streets',
              accessToken: 'pk.eyJ1IjoibmFvbWllLWNvIiwiYSI6ImNrMjR3aGI3dzFlZDAzbG55d283NjZxazMifQ.08l7cYOS_a-aGy_mfrMRAw'
        }).addTo(mymap);
      }
    })
}        