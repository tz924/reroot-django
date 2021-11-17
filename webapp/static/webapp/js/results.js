const counties = JSON.parse(document.getElementById('counties').textContent);
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [-93.771556, 44.967243],
  zoom: 3,
});

// Create a new marker.
counties.forEach(county => {
  new mapboxgl.Marker()
    .setLngLat(county.longlat)
    .setPopup(new mapboxgl.Popup({
        offset: 25
      }) // add popups
      .setHTML(
        `<h3>${county.county_name}</h3>`
      ))
    .addTo(map);
});

// Ensure maximum checked
const MAX_CHECKED = 3;
document.addEventListener('DOMContentLoaded', () => {
  const county_list = document.getElementById('county_list');
  let checkboxes = county_list.querySelectorAll("input[type=checkbox]");

  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
      let checked = county_list.querySelectorAll('input[type="checkbox"]:checked');

      let unchecked = [];
      checkboxes.forEach(c => {
        if (!c.checked) unchecked.push(c);
      });

      if (checked.length >= MAX_CHECKED) {
        unchecked.forEach(c => c.disabled = true);
      } else {
        unchecked.forEach(c => c.disabled = false);
      }
    });
  });

});