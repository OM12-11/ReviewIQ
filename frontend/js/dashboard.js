// =====================================
// ReviewIQ Dashboard Logic
// =====================================

import {
    getDashboardSummary,
    getAspectAnalysis,
    getProductAnalysis
} from "./api.js";

import {
    renderSentimentChart,
    renderAspectChart
} from "./charts.js";


// =====================================
// Utility Functions
// =====================================

function formatNumber(value) {
    return Number(value).toLocaleString("en-IN");
}


function updateElement(id, value) {

    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }

}


// =====================================
// Product Analytics Table
// =====================================

function renderProductTable(products) {

    const tableBody = document.getElementById("productTableBody");

    tableBody.innerHTML = "";

    products.forEach(product => {

        const row = document.createElement("tr");

        const sentiment = product.dominant_sentiment || "pending";

        const badge = document.createElement("span");

        badge.className = `sentiment-badge badge-${sentiment}`;
        badge.textContent = sentiment.toUpperCase();

        const values = [
            product.product_title,
            formatNumber(product.total_reviews),
            formatNumber(product.sentiment_distribution.positive),
            formatNumber(product.sentiment_distribution.negative),
            formatNumber(product.sentiment_distribution.neutral)
        ];


        values.forEach(value => {

            const cell = document.createElement("td");

            cell.textContent = value;

            row.appendChild(cell);

        });


        const sentimentCell = document.createElement("td");

        sentimentCell.appendChild(badge);

        row.appendChild(sentimentCell);

        tableBody.appendChild(row);

    });

}


// =====================================
// Load Dashboard Statistics
// =====================================

export async function loadDashboardData() {

    console.log("Fetching dashboard statistics...");


    // 1. Dashboard Summary

    const response = await getDashboardSummary();

    if (!response.success) {
        throw new Error("Dashboard summary API failed.");
    }

    const data = response.dashboard_summary;


    // KPI Cards

    updateElement(
        "totalReviews",
        formatNumber(data.total_reviews)
    );

    updateElement(
        "totalProducts",
        formatNumber(data.total_products)
    );

    updateElement(
        "analyzedReviews",
        formatNumber(data.analyzed_reviews)
    );

    updateElement(
        "totalPredictions",
        formatNumber(data.total_predictions)
    );


    // Sentiment Statistics

    const sentiment = data.sentiment_distribution;

    updateElement(
        "positiveCount",
        formatNumber(sentiment.positive.count)
    );

    updateElement(
        "negativeCount",
        formatNumber(sentiment.negative.count)
    );

    updateElement(
        "neutralCount",
        formatNumber(sentiment.neutral.count)
    );


    // Average Confidence

    updateElement(
        "averageConfidence",
        `${(data.average_confidence * 100).toFixed(2)}%`
    );


    // 2. Sentiment Chart

    renderSentimentChart(sentiment);


    // 3. Aspect Analysis

    console.log("Fetching aspect analysis...");

    const aspectResponse = await getAspectAnalysis();

    if (!aspectResponse.success) {
        throw new Error("Aspect analysis API failed.");
    }

    renderAspectChart(aspectResponse.aspect_analysis);


    // 4. Product Analytics

    console.log("Fetching product analytics...");

    const productResponse = await getProductAnalysis();

    if (!productResponse.success) {
        throw new Error("Product analysis API failed.");
    }

    renderProductTable(productResponse.product_analysis);


    console.log("ReviewIQ dashboard loaded successfully!");

}