
var mymap = L.map('mapid');
            $("button#btn").click(function(){
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
                        div#reponse is replace with API data 
                        
                        $("div#reponse").replaceWith(resp.data)*/


                        var question = document.createElement("p");
                        question.textContent = resp.search;
                        var answer = document.createElement("p");
                        answer.textContent = resp.final_answer;
                        var dialogue = document.getElementById("retour");
                        dialogue.appendChild(question);
                        dialogue.appendChild(answer);



                        
                        
                        var lat = parseFloat(resp.lat);
                        var long = parseFloat(resp.long);
                        console.log(resp);
                        console.log(lat, long);


                        mymap.setView([lat, long], 13)
                        var marker = L.marker([lat, long]).addTo(mymap);
                        marker.bindPopup("<b>Hello world!</b><br>I am a popup.").openPopup();

                        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibmFvbWllLWNvIiwiYSI6ImNrMjR3aGI3dzFlZDAzbG55d283NjZxazMifQ.08l7cYOS_a-aGy_mfrMRAw', {
                          attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                          maxZoom: 18,
                          id: 'mapbox.streets',
                          accessToken: 'pk.eyJ1IjoibmFvbWllLWNvIiwiYSI6ImNrMjR3aGI3dzFlZDAzbG55d283NjZxazMifQ.08l7cYOS_a-aGy_mfrMRAw'
                    }).addTo(mymap);
                       
                  }
                })
            })
