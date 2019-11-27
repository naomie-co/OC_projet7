
var mymap = L.map('mapid');
            $("button#btn").click(function(){


            	/*The question is display in the page*/	
            	var question = document.createElement("p");
                question.textContent = $("input#question").val();
                var dialogue = document.getElementById("retour");
                dialogue.insertBefore(question, dialogue.childNodes[0]);
				
				/* STEP 3
                An AJAX request is sent to the url /test_ajax/
                */
                $.ajax({
                    url: "/test_ajax/",
                    type: "POST",
                    data: {"question": $("input#question").val()},
					

                    /* STEP 4
                    +++++ In Python file (run.py)+++++
                    Data are collected from the request and sent to an API
                    */
                    /* STEP 5
                    +++++ In Python file (run.py)+++++
                    API Data are sent back to the template 
                    */
                    success: function(resp){
                        /* STEP 6
                       creates <p> elements to insert the answer*/                     
                        var address = document.createElement("p");
                        address.textContent = "Bien sûr mon poussin ! La voici : " + resp.address;
                        var answer = document.createElement("p");
                        answer.textContent = resp.final_answer;
                        var wiki_link = document.createElement("a")
                        wiki_link.textContent = "Pour en savoir plus, tu peux cliquer sur ce lien"
                        wiki_link.href = resp.link;
                        var dialogue = document.getElementById("retour");
                        dialogue.insertBefore(address, dialogue.childNodes[1]);
                        dialogue.insertBefore(answer, dialogue.childNodes[2]);
                        dialogue.insertBefore(wiki_link, dialogue.childNodes[3]);

                       
                        var lat = parseFloat(resp.lat);
                        var long = parseFloat(resp.long);
                        var title = resp.address;
                        console.log(resp);
                        console.log(lat, long);

                        mymap.setView([lat, long], 13);
                        var marker = L.marker([lat, long]).addTo(mymap);
                        marker.bindPopup("<b>" + title + "</b>").openPopup();

                        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibmFvbWllLWNvIiwiYSI6ImNrMjR3aGI3dzFlZDAzbG55d283NjZxazMifQ.08l7cYOS_a-aGy_mfrMRAw', {
                          attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                          maxZoom: 18,
                          id: 'mapbox.streets',
                          accessToken: 'pk.eyJ1IjoibmFvbWllLWNvIiwiYSI6ImNrMjR3aGI3dzFlZDAzbG55d283NjZxazMifQ.08l7cYOS_a-aGy_mfrMRAw'
                    }).addTo(mymap);
                       
                  }
                })
            })
