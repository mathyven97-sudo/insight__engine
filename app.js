// Chart Configuration
Chart.defaults.color = '#9ca3af';
Chart.defaults.borderColor = '#374151';

let sentimentChartInstance = null;
let activityChartInstance = null;

// Initial Charts Helper
function initCharts() {
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded. Charts will not be displayed.');
        return;
    }

    // Sentiment Chart
    const sentimentCanvas = document.getElementById('sentimentChart');
    if (sentimentCanvas) {
        const sentimentCtx = sentimentCanvas.getContext('2d');
        sentimentChartInstance = new Chart(sentimentCtx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: ['#10b981', '#6b7280', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#9ca3af' } }
                }
            }
        });
    }

    // Activity Chart (Placeholder)
    const activityCanvas = document.getElementById('activityChart');
    if (activityCanvas) {
        const activityCtx = activityCanvas.getContext('2d');
        activityChartInstance = new Chart(activityCtx, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                datasets: [{
                    label: 'Posts',
                    data: [12, 19, 3, 5, 2, 3], // Mock data for visual completeness
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: '#374151' }, ticks: { color: '#9ca3af' } },
                    x: { grid: { display: false }, ticks: { color: '#9ca3af' } }
                }
            }
        });
    }
}

// Fetch Insights
async function refreshInsights() {
    try {
        const response = await fetch('/api/v1/insights');
        const insights = await response.json();

        const container = document.getElementById('insightsContainer');
        if (container && insights.length > 0) {
            container.innerHTML = insights.map(insight => `
                <div class="p-4 bg-gray-700/30 rounded-lg border border-gray-700/50 hover:bg-gray-700/50 transition-colors">
                    <div class="flex justify-between items-start mb-2">
                        <h4 class="font-semibold text-white">${insight.title}</h4>
                        <span class="px-2 py-1 rounded text-xs font-bold ${insight.risk === 'HIGH' ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}">
                            ${insight.risk} RISK
                        </span>
                    </div>
                    <p class="text-gray-400 text-sm mb-3">${insight.description}</p>
                    <div class="flex items-center text-xs text-gray-500 gap-4">
                        <span><i class="far fa-clock mr-1"></i> ${insight.time}</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (e) {
        console.error("Failed to fetch insights", e);
    }
}

// Fetch Stats
async function refreshStats() {
    try {
        const response = await fetch('/api/v1/stats');
        const data = await response.json();

        // Update Total
        const totalEl = document.getElementById('totalPosts');
        if (totalEl) totalEl.innerText = data.total_posts.toLocaleString();

        // Update Sentiment Chart
        if (data.sentiment_distribution) {
            const dist = data.sentiment_distribution;
            const pos = dist['Positive'] || 0;
            const neu = dist['Neutral'] || 0;
            const neg = dist['Negative'] || 0;

            if (sentimentChartInstance) {
                sentimentChartInstance.data.datasets[0].data = [pos, neu, neg];
                sentimentChartInstance.update();
            }

            // Update Activity Bar
            const total = pos + neu + neg;
            if (total > 0) {
                // Calculate simplified score (-1 to 1 mapped to 0-100%)
                const score = ((pos - neg) / total + 1) / 2 * 100;
                const bar = document.getElementById('sentimentBar');
                if (bar) bar.style.width = `${score}%`;
            }
        }

    } catch (e) {
        console.error("Failed to fetch stats", e);
    }
}

// Event Listeners
const ingestBtn = document.getElementById('ingestBtn');
if (ingestBtn) {
    ingestBtn.addEventListener('click', async () => {
        const btn = document.getElementById('ingestBtn');
        const originalText = btn.innerHTML;

        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/v1/ingest', { method: 'POST' });
            const data = await response.json();

            if (data.status === 'success') {
                alert(`Successfully processed ${data.count} posts!`);
                refreshStats();
            } else {
                alert('Error processing data');
            }
        } catch (e) {
            console.error(e);
            alert('Failed to connect to backend');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });

}

// Initialize
console.log("App.js loading...");
try {
    initCharts();
    refreshStats();
    refreshInsights();
    console.log("App.js initialized successfully");
} catch (e) {
    console.error("App.js initialization failed:", e);
    alert("Error initializing dashboard: " + e.message);
}
