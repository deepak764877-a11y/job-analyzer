console.log("Dashboard JS Loaded Successfully");
 
const scoreElement = document.querySelector(".gauge-score-text");
const chartCanvas = document.getElementById("scoreChart");
 
if (scoreElement && chartCanvas && typeof Chart !== "undefined") {
    let score = parseInt(scoreElement.innerText);
    if (isNaN(score)) score = 0;
 
    const needlePlugin = {
        id: "needlePlugin",
        afterDatasetsDraw(chart) {
            const { ctx } = chart;
            const meta = chart.getDatasetMeta(0);
            const arc = meta.data[0];
            if (!arc) return;
 
            const cx = arc.x;
            const cy = arc.y;
            const outerRadius = arc.outerRadius;
            const value = chart.needleValue || 0;
            const max = 100;
            const needleLength = outerRadius * 0.78;
 
            const theta = Math.PI * (1 - value / max);
            const tipX = cx + needleLength * Math.cos(theta);
            const tipY = cy - needleLength * Math.sin(theta);
 
            ctx.save();
            ctx.shadowBlur = 12;
            ctx.shadowColor = "#ffffff";
 
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(tipX, tipY);
            ctx.lineWidth = 4;
            ctx.strokeStyle = "#f8fafc";
            ctx.lineCap = "round";
            ctx.stroke();
 
            ctx.beginPath();
            ctx.arc(cx, cy, 7, 0, Math.PI * 2);
            ctx.fillStyle = "#f8fafc";
            ctx.fill();
 
            ctx.beginPath();
            ctx.arc(tipX, tipY, 4, 0, Math.PI * 2);
            ctx.fillStyle = "#fff";
            ctx.fill();
 
            ctx.restore();
        }
    };
 
    const chart = new Chart(chartCanvas, {
        type: "doughnut",
        data: {
            needleValue: 0,
            datasets: [{
                data: [40, 30, 30],
                backgroundColor: ["#ef4444", "#f59e0b", "#10b981"],
                borderWidth: 0,
                borderRadius: 8,
                spacing: 4
            }]
        },
        options: {
            rotation: -90,
            circumference: 180,
            cutout: "70%",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        },
        plugins: [needlePlugin]
    });
 
    let current = 0;
    function animateNeedle() {
        current += (score - current) * 0.12;
        if (Math.abs(score - current) < 0.5) current = score;
 
        chart.needleValue = current;
        chart.update("none");
 
        if (current !== score) {
            requestAnimationFrame(animateNeedle);
        }
    }
    requestAnimationFrame(animateNeedle);
}
const downloadBtn = document.getElementById("downloadPdfBtn");
if (downloadBtn) {
    downloadBtn.addEventListener("click", (e) => {
        e.preventDefault();
        window.print();
    });
}
 