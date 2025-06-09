(function()
{
  if( window.localStorage )
  {
    if( !localStorage.getItem('firstLoad') )
    {
      localStorage['firstLoad'] = true;
      window.location.reload();
    }  
    else
      localStorage.removeItem('firstLoad');
  }
})();

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
    var datetime = new Date(data["datetime"]);
    var options = {
        timeZone: "Europe/Berlin",
        hour12: false,
        year: "2-digit",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
    };
    var formattedDatetime = datetime.toLocaleString("de-DE", options);

    document.querySelector("#datetime").innerHTML = " " + formattedDatetime + " Ortszeit";
    document.querySelector("#temperature").innerHTML = '<span">' + data["temperature"]["string"] + ' °C</span>';
    document.querySelector("#dewpoint").innerHTML = '<span">' + data["dewpoint"]["string"] + ' °C</span>';
    document.querySelector("#humidity").innerHTML = '<span">' + data["humidity"]["value"] + '</span><span class="mobile-font""> %</span>';
    document.querySelector("#pressure").innerHTML = '<span">' + data["pressure"]["value"] + '</span><span class="mobile-font""> hPa</span>';
    document.querySelector("#ground-pressure").innerHTML = data["ground-pressure"]["value"] + " " + data["ground-pressure"]["unit"]
    document.querySelector("#uv").innerHTML = data["uv"]["value"]
    document.querySelector("#speed").innerHTML = '<span">' + data["wind_speed"]["string"] + '</span><span class="mobile-font""> km/h</span>';
    document.querySelector("#direction").innerHTML = '<span class="mobile-font">' + data["wind_direction"]["string"] + '</span>';
    document.querySelector("#strahl").innerHTML = '<span">' + data["global_radiation"]["value"] + '</span><span class="mobile-font""> W/m²</span>';

    document.querySelector("#cbh_cur").innerHTML = '<span">' + data["cbh_cur"]["string"] + '</span><span class="mobile-font""> m</span>';

    document.querySelector("#precip").innerHTML = '<span">' + data["precip"]["precip_last_hour"]["string"] + '</span><span class="mobile-font""> mm</span>';
    document.querySelector("#ozone").innerHTML = '<span class="mobile-font"">Wartung</span>' /*'<span">' + data["ozone"]["value"] + '</span><span class="mobile-font""> ppb</span>';*/

    //disable spinner
    document.querySelector("#spinner1").style.display = "none";
    document.querySelector("#spinner2").style.display = "none";
    document.querySelector("#spinner3").style.display = "none";
    document.querySelector("#spinner4").style.display = "none";
    document.querySelector("#spinner5").style.display = "none";
    document.querySelector("#spinner6").style.display = "none";
    document.querySelector("#spinner7").style.display = "none";
    document.querySelector("#spinner8").style.display = "none";
    document.querySelector("#spinner9").style.display = "none";

}

updateBoxes()

setInterval(function () {
    updateBoxes()
}, 30000);
