$(document).ready(function(){
  
    // get personality type variable from local storage
    let pKey = 'personality_type';
    let pType = sessionStorage.getItem(pKey); 
    // get temperament type variable from local storage
    let tKey = 'temperament_type';
    let tType = sessionStorage.getItem(tKey);
    
    //get goal variable from local storage
    let gkey = 'goal';
    let goal = sessionStorage.getItem(gkey);
     
    // created JSON object & then create a string from it
    // Note that we have to use Computed Property Name for keys..
    var testResults = {[pKey]:pType, [tKey]:tType,[gkey]:goal};
    testResults = JSON.stringify(testResults);
    

    
    // send POST request to the URL where calculations will be carried out
    $.ajax({ 
        url: "/CareerRecommendationResult", 
        type: 'POST', 
        async: false,
        data: testResults,
        contentType: "application/json",
        success: function(response){ 
            console.log(response)
            let careers = JSON.parse(response);
            careers = JSON.parse(careers["data"]);
            console.log(typeof careers);
            
            // display career recommendations
            
            $("#career_rec").append("<ul></ul>");
            for (const [key,value] of Object.entries(careers)) {
                // console.log(key,value)
              let career = `<li>${key}</li>`;
              career += `<p>${value[0]} ${value[1]} ${value[2]}</p>`;
              career += `<p>${value[3]}</p>`;
              $("#career_rec ul").append(career);
            }
           
        } 
    });

});
