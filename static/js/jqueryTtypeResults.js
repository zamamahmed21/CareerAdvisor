$(document).ready(function(){

    // get Temperament type variable from local storage & insert into html
    let tType = sessionStorage.getItem("temperament_type");
    $("#t_type").text(tType); 

    if (sessionStorage.hasOwnProperty('goal')){
        $("#career_rec_btn").append('<a href="/CareerRecommendation"><input type="button" class="btn btn-primary btn-block btn-lg bg-nav " value="Get your career recommendation"></a>' )
    }
    

});