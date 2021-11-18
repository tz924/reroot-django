// <block:setup:1>
const counties = JSON.parse(document.getElementById('counties').textContent);
console.log(counties);
let county_names = []
counties.forEach((e) => {
  county_names.push(e.county_name);
});

// TODO Sample metrics
let sample_labels = ['diversity_cultural', 'diversity_economic', 'diversity_lgbt'];
let colors = ['red', 'blue', 'green'];

console.log(county_names);
const title_text = county_names.join(' vs ');
const labels = sample_labels;
let datasets = [];
for (const [index, county] of counties.entries()) {
  let data = [];
  sample_labels.forEach(label => {
    data.push(county[label]);
  });

  let dataset = {
    label: county.county_name,
    backgroundColor: colors[index],
    borderColor: colors[index],
    data: data,
  }

  datasets.push(dataset);
}

const data = {
  labels: labels,
  datasets: datasets,
};
// </block:setup>

// <block:config:0>
const config = {
  type: 'bar',
  data: data,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: title_text,
      }
    }
  }
};
// </block:config>

// === include 'setup' then 'config' above ===
const myChart = new Chart(
  document.getElementById('myChart'),
  config
);


// <block:action:2>
document.addEventListener('DOMContentLoaded', () => {

  // Add Data
  let add_btn = document.getElementById('environment_air');
  add_btn.addEventListener('click', () => {

    const data = myChart.data;
    if (data.datasets.length > 0) {
      sample_labels.push('environment_air');
      data.labels = sample_labels;

      for (let index = 0; index < data.datasets.length; ++index) {
        data.datasets[index].data.push(counties[index]['environment_air']);
      }

      myChart.update();
    }
  });

  // Remove Data
  let remove_btn = document.getElementById('remove_last');
  remove_btn.addEventListener('click', () => {
    myChart.data.labels.splice(-1, 1); // remove the label first

    myChart.data.datasets.forEach(dataset => {
      dataset.data.pop();
    });

    myChart.update();
  });
});
// <block:action>