// =====================================
// ReviewIQ Application Controller
// =====================================

import { loadDashboardData } from "./dashboard.js";

import {
    uploadDataset,
    runSentimentAnalysis
} from "./api.js";


// =====================================
// Dashboard Initialization
// =====================================

async function initializeApp() {
    console.log("Initializing ReviewIQ...");

    try {
        await loadDashboardData();
        console.log("ReviewIQ initialized successfully!");

    } catch (error) {
        console.error("Application initialization failed:", error);
    }
}


// =====================================
// Dataset Upload
// =====================================

function initializeUpload() {

    const fileInput = document.getElementById("datasetFile");
    const uploadButton = document.getElementById("uploadButton");
    const uploadMessage = document.getElementById("uploadMessage");

    uploadButton.addEventListener("click", async function () {

        const file = fileInput.files[0];

        if (!file) {
            uploadMessage.textContent = "Please select a CSV file.";
            return;
        }

        if (!file.name.toLowerCase().endsWith(".csv")) {
            uploadMessage.textContent = "Only CSV files are allowed.";
            return;
        }

        try {
            uploadButton.disabled = true;
            uploadButton.textContent = "Uploading...";

            const response = await uploadDataset(file);

            if (!response.success) {
                throw new Error(response.message || "Upload failed.");
            }

            uploadMessage.textContent =
                `Success! ${response.records_saved} reviews uploaded.`;

            uploadMessage.style.color = "green";

            await loadDashboardData();

            fileInput.value = "";

        } catch (error) {
            uploadMessage.textContent = error.message;
            uploadMessage.style.color = "red";

        } finally {
            uploadButton.disabled = false;
            uploadButton.textContent = "Upload Dataset";
        }
    });
}


// =====================================
// Run Sentiment Analysis
// =====================================

function initializeAnalysis() {

    const analyzeButton = document.getElementById("analyzeButton");
    const analysisMessage = document.getElementById("analysisMessage");

    analyzeButton.addEventListener("click", async function () {

        try {

            analyzeButton.disabled = true;
            analyzeButton.textContent = "Analyzing...";

            analysisMessage.textContent =
                "Running ML sentiment analysis. Please wait...";

            analysisMessage.style.color = "blue";

            const response = await runSentimentAnalysis();

            if (!response.success) {
                throw new Error(response.message || "Analysis failed.");
            }

            analysisMessage.textContent =
                `Analysis completed! ${response.new_predictions_saved} new predictions generated.`;

            analysisMessage.style.color = "green";

            console.log("Sentiment analysis result:", response);

            // Refresh dashboard with new predictions
            await loadDashboardData();

        } catch (error) {

            console.error("Sentiment analysis failed:", error);

            analysisMessage.textContent = error.message;
            analysisMessage.style.color = "red";

        } finally {

            analyzeButton.disabled = false;
            analyzeButton.textContent = "Run Sentiment Analysis";

        }
    });
}


// =====================================
// Start Application
// =====================================

initializeApp();

initializeUpload();
initializeAnalysis();