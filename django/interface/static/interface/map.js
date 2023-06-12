/* eslint-disable no-undef */
/**
 * markers 60K
 */

// config map
let config = {
  minZoom: 1,
  maxZoom: 20,
};
// magnification with which the map will start
const zoom = 10;
// co-ordinates
const lat = 52.229675;
const lng = 21.012230;

// calling map
const map = L.map("map", config).setView([lat, lng], zoom);

// Used to load and display tile layers on the map
// Most tile servers require attribution, which you can set under `Layer`
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// we assign a marker layer to the variable
let markers = L.markerClusterGroup();

map.addLayer(markers);

fetch("/api/locationsAmount").then((response) => 
    response.json().then((data) => {
        let petsAmount = data["pets_number"]

        for (let i = 0; i < petsAmount; i++) {
            fetch("/api/locationsOne?pet_number=" + i).then((response) => {
                response.json().then((data) => {
                    let pets = data.pets;
                    for (let i = 0; i < pets.length; i++) {
                        let pet = pets[i];
                        let marker = L.marker([pet.geo_lat, pet.geo_lng]);
                        marker.bindPopup(
                            "<b>" + pet.name + "</b><br>" + "Link to pet page: " 
                            + "<a target='_blank' href='https://napaluchu.waw.pl" + pet.link + 
                            "'>https://napaluchu.waw.pl" + pet.link + "</a>"
                            );
                        marker.on("popupopen", (e) => {
                            let popup = e.popup;
                            let imageSrc = findImageSrc("https://napaluchu.waw.pl" + pet.link);
                            imageSrc.then((imageSrc) => {
                                popup.setContent(popup.getContent() + "<br>" + "<img src='" + imageSrc + "' width=auto height='200'>");
                                console.log("test");
                            });
                        });

                        markers.addLayer(marker);
                    }
                });
            });
        }
    }
)); 

let findImageSrc = async (petLink) => {
    let response = await fetch(petLink);
    let html = await response.text();

    console.log(html);

    let parser = new DOMParser();
    let doc = parser.parseFromString(html, "text/html");
    let imageSrc = doc.querySelector(".pet-detail-main-image").src;
    return imageSrc;

}