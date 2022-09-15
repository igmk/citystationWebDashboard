async function queryAPI() {
    let url = 'data.json';
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}
async function updateBoxes() {
    
    let data = await queryAPI();
    document.querySelector("#datetime").innerHTML = data["datetime"]
    document.querySelector("#temperature").innerHTML = data["temperature"]+" °C"
    document.querySelector("#humidity").innerHTML = data["humidity"]+" %"
    document.querySelector("#pressure").innerHTML = data["pressure"]+" hPa"
    document.querySelector("#uv").innerHTML = data["uv"]
    document.querySelector("#speed").innerHTML = data["speed"]+" km/h"
    document.querySelector("#direction").innerHTML = data["direction"]
    
    document.querySelector("#spinner1").style.display ="none";
    document.querySelector("#spinner2").style.display ="none";
    document.querySelector("#spinner3").style.display ="none";
    document.querySelector("#spinner4").style.display ="none";
    document.querySelector("#spinner5").style.display ="none";
    document.querySelector("#spinner6").style.display ="none";
}

updateBoxes()

setInterval(function(){ 
  updateBoxes()
    //code goes here that will be run every 5 seconds.    
}, 5000);