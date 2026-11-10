// =====================================
// ReviewIQ API Configuration
// =====================================

const API_BASE_URL = "http://127.0.0.1:8000";


// =====================================
// Common API Request Function
// =====================================

async function apiRequest(endpoint, options = {}) {

    try {

        const response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            options
        );

        if (!response.ok) {

            throw new Error(
                `API Error: ${response.status} ${response.statusText}`
            );

        }

        return await response.json();

    } catch (error) {

        console.error("API Request Failed:", error);

        throw error;

    }

}


// =====================================
// 1. Dashboard Summary API
// GET /api/summary
// =====================================

export async function getDashboardSummary() {

    return await apiRequest("/api/summary");

}


// =====================================
// 2. Aspect Analysis API
// GET /api/summary/aspects
// =====================================

export async function getAspectAnalysis() {

    return await apiRequest("/api/summary/aspects");

}


// =====================================
// 3. Product Analysis API
// GET /api/summary/products
// =====================================

export async function getProductAnalysis() {

    return await apiRequest("/api/summary/products");

}


// =====================================
// 4. Upload Dataset API
// POST /api/upload
// =====================================

export async function uploadDataset(file) {

    const formData = new FormData();

    formData.append("file", file);

    return await apiRequest("/api/upload", {

        method: "POST",

        body: formData

    });

}


// =====================================
// 5. Run Sentiment Analysis API
// POST /api/analyze
// =====================================

export async function runSentimentAnalysis() {

    return await apiRequest("/api/analyze", {

        method: "POST"

    });

}