document.addEventListener("DOMContentLoaded", () => {

    const scoreElement = document.querySelector(".gauge-value");
    const chartCanvas = document.getElementById("scoreChart");

    if (!scoreElement || !chartCanvas || typeof Chart === "undefined") {
        return;
    }

    let score = parseInt(scoreElement.textContent) || 0;
    score = Math.max(0, Math.min(score, 100));

    const ctx = chartCanvas.getContext("2d");

    let startColor, endColor;

    if (score >= 85) {
        startColor = "#22c55e";
        endColor = "#10b981";
    } else if (score >= 70) {
        startColor = "#f59e0b";
        endColor = "#fbbf24";
    } else {
        startColor = "#ef4444";
        endColor = "#f87171";
    }

    const gradient = ctx.createLinearGradient(
        0,
        0,
        chartCanvas.width,
        chartCanvas.height
    );

    gradient.addColorStop(0, startColor);
    gradient.addColorStop(1, endColor);

    new Chart(ctx, {
        type: "doughnut",

        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [
                    gradient,
                    "rgba(255,255,255,0.08)"
                ],
                borderWidth: 0,
                borderRadius: 14,
                spacing: 3,
                hoverOffset: 8
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "78%",

            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1400,
                easing: "easeOutQuart"
            },

            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });

});