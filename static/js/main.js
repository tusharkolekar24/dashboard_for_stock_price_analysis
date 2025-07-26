
function toggleSidebar() {
        const sidebar = document.querySelector('.sidenav');
        sidebar.classList.toggle('toggled');
        document.querySelector('.content').classList.toggle('toggled');
    }       
const config = {
                displaylogo: false,
                modeBarButtonsToRemove: [
                    'resetAxes', 'spikelines', 'zoomIn2d', 'zoomOut2d',
                    'zoom2d', 'pan2d', 'select2d'
                ]
            };

    document.querySelector('.dropdown-button').addEventListener('click', function() {
        var formContainer = this.nextElementSibling;
            if (formContainer.style.display === 'block') {
                formContainer.style.display = 'none';
            } else {
                formContainer.style.display = 'block';
            }
    });

document.addEventListener('DOMContentLoaded', function() {

    // Fetch and render line chart data
    fetch('/line-chart') // Ensure this matches your Flask route for pie chart
        .then(response => response.json())
        .then(data => {
            var graphJson = JSON.parse(data.graph_json);
            Plotly.react('line-chart', graphJson.data, graphJson.layout, config);
        })
        .catch(error => console.error('Error fetching pie chart data:', error));

    // Fetch and render line chart data
    fetch('/bar-chart') // Ensure this matches your Flask route for pie chart
        .then(response => response.json())
        .then(data => {
            var graphJson = JSON.parse(data.graph_json);
            Plotly.react('bar-chart', graphJson.data, graphJson.layout, config);
        })
        .catch(error => console.error('Error fetching pie chart data:', error));

    fetch('/tree-sectoral-chart')
    .then(response => response.json())
        .then(data => {
            var graphJson = JSON.parse(data.graph_json);
            Plotly.react('tree-sectoral-chart', graphJson.data, graphJson.layout, config);
        })
        .catch(error => console.error('Error fetching pie chart data:', error));

});