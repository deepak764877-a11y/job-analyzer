console.log("Dashboard JS Loaded Successfully");

const scoreElement = document.querySelector(".score-value");
const chartCanvas = document.getElementById("scoreChart");

if (scoreElement && chartCanvas) {
    let score = parseInt(scoreElement.innerText);
    if (isNaN(score)) score = 0;

    new Chart(chartCanvas, {
        type: "doughnut",
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: ["#22c55e", "#dbe4f0"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "75%",
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}