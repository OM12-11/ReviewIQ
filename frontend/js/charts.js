// =====================================
// ReviewIQ Chart Visualizations
// =====================================

let sentimentChartInstance = null;
let aspectChartInstance = null;


// =====================================
// 1. SENTIMENT DOUGHNUT CHART
// =====================================

export function renderSentimentChart(distribution) {

    const canvas = document.getElementById("sentimentChart");

    if (!canvas || typeof Chart === "undefined") {
        console.error("Chart.js or sentiment canvas not found.");
        return;
    }

    const labels = ["Positive", "Negative", "Neutral"];

    const values = [
        distribution.positive.count,
        distribution.negative.count,
        distribution.neutral.count
    ];

    if (sentimentChartInstance) {
        sentimentChartInstance.destroy();
    }

    sentimentChartInstance = new Chart(canvas, {

        type: "doughnut",

        data: {
            labels: labels,

            datasets: [{
                data: values,

                backgroundColor: [
                    "#16a34a",
                    "#ef4444",
                    "#f59e0b"
                ],

                borderWidth: 0,
                hoverOffset: 8
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "70%",

            plugins: {

                legend: {
                    position: "bottom",

                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },

                tooltip: {
                    callbacks: {

                        label: function(context) {

                            const total = values.reduce(
                                (sum, value) => sum + value,
                                0
                            );

                            const percentage = (
                                context.raw / total * 100
                            ).toFixed(2);

                            return `${context.label}: ${context.raw.toLocaleString("en-IN")} (${percentage}%)`;
                        }

                    }
                }

            }

        }

    });

}


// =====================================
// 2. ASPECT ANALYSIS BAR CHART
// =====================================

export function renderAspectChart(aspectData) {

    const canvas = document.getElementById("aspectChart");

    if (!canvas || typeof Chart === "undefined") {
        console.error("Chart.js or aspect canvas not found.");
        return;
    }

    const aspects = Object.keys(aspectData);

    const positive = aspects.map(
        aspect => aspectData[aspect].positive
    );

    const negative = aspects.map(
        aspect => aspectData[aspect].negative
    );

    const neutral = aspects.map(
        aspect => aspectData[aspect].neutral
    );

    if (aspectChartInstance) {
        aspectChartInstance.destroy();
    }

    aspectChartInstance = new Chart(canvas, {

        type: "bar",

        data: {

            labels: aspects,

            datasets: [

                {
                    label: "Positive",
                    data: positive,
                    backgroundColor: "#16a34a"
                },

                {
                    label: "Negative",
                    data: negative,
                    backgroundColor: "#ef4444"
                },

                {
                    label: "Neutral",
                    data: neutral,
                    backgroundColor: "#f59e0b"
                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            indexAxis: "y",

            interaction: {
                mode: "index",
                intersect: false
            },

            scales: {

                x: {
                    beginAtZero: true,

                    stacked: true,

                    title: {
                        display: true,
                        text: "Number of Predictions"
                    }
                },

                y: {
                    stacked: true
                }

            },

            plugins: {

                legend: {
                    position: "bottom",

                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                }

            }

        }

    });

}