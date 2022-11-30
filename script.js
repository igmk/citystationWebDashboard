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
    //update box-values
    document.querySelector("#datetime").innerHTML = " "+data["datetime"]+" MEZ"
    document.querySelector("#temperature").innerHTML = data["temperature"]+" °C"
    document.querySelector("#humidity").innerHTML = data["humidity"]+" %"
    document.querySelector("#pressure").innerHTML = data["pressure"]+" hPa"
    document.querySelector("#uv").innerHTML = data["uv"]
    document.querySelector("#speed").innerHTML = data["speed"]+" km/h"
    document.querySelector("#direction").innerHTML = data["direction"]
    document.querySelector("#cbh_cur").innerHTML = data["cbh_cur"]+" km"
    document.querySelector("#cbh_low").innerHTML = data["cbh_low"]+" km"
    document.querySelector("#cbh_mid").innerHTML = data["cbh_mid"]+" km"
    document.querySelector("#cbh_hig").innerHTML = data["cbh_hig"]+" km"
    //disable spinner
    document.querySelector("#spinner1").style.display ="none";
    document.querySelector("#spinner2").style.display ="none";
    document.querySelector("#spinner3").style.display ="none";
    document.querySelector("#spinner4").style.display ="none";
    document.querySelector("#spinner5").style.display ="none";
    document.querySelector("#spinner6").style.display ="none";
    document.querySelector("#spinner7").style.display ="none";
    document.querySelector("#spinner8").style.display ="none";
    document.querySelector("#spinner9").style.display ="none";
    document.querySelector("#spinner10").style.display ="none";
}

updateBoxes()

setInterval(function(){ 
  updateBoxes()
}, 30000);
