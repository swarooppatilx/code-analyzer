document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript file is linked and loaded.");
    let timeComplexityChart = null;
    let spaceComplexityChart = null;

    document.getElementById('codeForm').addEventListener('submit', function (event) {
        event.preventDefault();
        const code = document.getElementById('codeInput').value;
        document.getElementById('spinner').style.display = 'flex';

        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('spinner').style.display = 'none';

            if (data.timeComplexity) {
                displayAnalysisResults(data);
                createCharts(data);
            } else {
                showError('Error: Could not analyze the code.');
            }
        })
        .catch(error => {
            document.getElementById('spinner').style.display = 'none';
            showError('Error: An error occurred while analyzing the code.');
        });
    });

    function displayAnalysisResults(data) {
        document.getElementById('analysisOutput').innerHTML = `
            <strong class="text-gray-800">Time Complexity:</strong><br>
            <span class="text-gray-600">Best Case: ${data.timeComplexity.bestCase}</span><br>
            <span class="text-gray-600">Average Case: ${data.timeComplexity.averageCase}</span><br>
            <span class="text-gray-600">Worst Case: ${data.timeComplexity.worstCase}</span><br>
            <strong class="text-gray-800">Space Complexity:</strong><br>
            <span class="text-gray-600">Best Case: ${data.spaceComplexity.bestCase}</span><br>
            <span class="text-gray-600">Average Case: ${data.spaceComplexity.averageCase}</span><br>
            <span class="text-gray-600">Worst Case: ${data.spaceComplexity.worstCase}</span><br>
            <strong class="text-gray-800">Summary:</strong> <span class="text-gray-600">${data.summary || "No summary provided."}</span>
        `;
        document.getElementById('optimizedCode').innerHTML = `
            <pre><code class="language-js">${data.optimizedCode || "No optimized code provided."}</code></pre>
        `;
        Prism.highlightAll();
        document.getElementById('analysisResult').classList.remove('hidden');
    }

    function createCharts(data) {
        const timeLabels = Array.from({ length: 100 }, (_, i) => i + 1);
        createTimeComplexityChart(timeLabels, data.timeComplexity);
        createSpaceComplexityChart(timeLabels, data.spaceComplexity);
    }

    function createTimeComplexityChart(labels, complexity) {
        const bestCase = generateTrendlineData(complexity.bestCase);
        const averageCase = generateTrendlineData(complexity.averageCase);
        const worstCase = generateTrendlineData(complexity.worstCase);

        if (timeComplexityChart) {
            timeComplexityChart.destroy();
        }

        const ctx = document.getElementById('timeComplexityChart').getContext('2d');
        timeComplexityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    { label: 'Best Case', data: bestCase, borderColor: 'green', borderWidth: 2, pointRadius: 3, fill: false },
                    { label: 'Average Case', data: averageCase, borderColor: 'blue', borderWidth: 2, pointRadius: 3, fill: false },
                    { label: 'Worst Case', data: worstCase, borderColor: 'red', borderWidth: 2, pointRadius: 3, fill: false }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Input Size (n)',
                            font: { size: window.innerWidth < 640 ? 12 : 14 }
                        },
                        ticks: { font: { size: window.innerWidth < 640 ? 10 : 12 } }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Time Complexity',
                            font: { size: window.innerWidth < 640 ? 12 : 14 }
                        },
                        ticks: { font: { size: window.innerWidth < 640 ? 10 : 12 } }
                    },
                },
                plugins: {
                    legend: {
                        labels: { font: { size: window.innerWidth < 640 ? 10 : 12 } }
                    },
                },
            }
        });
    }

    function createSpaceComplexityChart(labels, complexity) {
        const bestCase = generateSpaceTrendlineData(complexity.bestCase);
        const averageCase = generateSpaceTrendlineData(complexity.averageCase);
        const worstCase = generateSpaceTrendlineData(complexity.worstCase);

        if (spaceComplexityChart) {
            spaceComplexityChart.destroy();
        }

        const ctx = document.getElementById('spaceComplexityChart').getContext('2d');
        spaceComplexityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    { label: 'Best Case', data: bestCase, borderColor: 'green', borderWidth: 2, pointRadius: 3, fill: false },
                    { label: 'Average Case', data: averageCase, borderColor: 'blue', borderWidth: 2, pointRadius: 3, fill: false },
                    { label: 'Worst Case', data: worstCase, borderColor: 'red', borderWidth: 2, pointRadius: 3, fill: false }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Input Size (n)',
                            font: { size: window.innerWidth < 640 ? 12 : 14 }
                        },
                        ticks: { font: { size: window.innerWidth < 640 ? 10 : 12 } }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Space Complexity',
                            font: { size: window.innerWidth < 640 ? 12 : 14 }
                        },
                        ticks: { font: { size: window.innerWidth < 640 ? 10 : 12 } }
                    },
                },
                plugins: {
                    legend: {
                        labels: { font: { size: window.innerWidth < 640 ? 10 : 12 } }
                    },
                },
            }
        });
    }

    function generateTrendlineData(complexity) {
        const data = [];
        for (let n = 1; n <= 100; n++) {
            let value = 0;
            if (complexity === 'O(1)') {
                value = 1;
            } else if (complexity === 'O(n)') {
                value = n;
            } else if (complexity === 'O(n^2)') {
                value = n * n;
            }
            data.push(value);
        }
        return data;
    }

    function generateSpaceTrendlineData(complexity) {
        return generateTrendlineData(complexity);
    }

    function showError(message) {
        const feedback = document.getElementById('feedbackMessage');
        feedback.innerHTML = `<div class="text-red-600">${message}</div>`;
    }

    window.addEventListener('resize', function() {
        if (timeComplexityChart) {
            timeComplexityChart.resize();
        }
        if (spaceComplexityChart) {
            spaceComplexityChart.resize();
        }
    });
});
