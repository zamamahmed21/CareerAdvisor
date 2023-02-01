$(document).ready(function(){

    // get personality type variable from local storage
    let pKey = 'personality_type';
    let pType = sessionStorage.getItem(pKey); 
    // get temperament type variable from local storage
    let tKey = 'temperament_type';
    let tType = sessionStorage.getItem(tKey);
    
    // create JSON object & then create a string from it
    // Note that we have to use Computed Property Name for keys..
    var testResults = {[pKey]:pType, [tKey]:tType};
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

            // display career recommendations
            $("#career_rec").append("<ul></ul>");
            for (const career of careers["data"]){
                $("#career_rec ul").append(`<li>${career}</li>`);
            }
        } 
    });

});