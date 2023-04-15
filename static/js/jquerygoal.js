$(document).ready(function(){

   
     
    
    $("#next").click(function(){

        sessionStorage.setItem("goal",$('input[name="goal"]:checked').val());
        window.location.href = "/PersonalityTest";

      });

});