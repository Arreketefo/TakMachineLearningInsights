// Initialize statistics chart
const ctx = document.getElementById('eventStats').getContext('2d');
const eventStats = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Events Processed',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Function to update recent events table
function updateRecentEvents(events) {
    const tbody = document.getElementById('recentEvents');
    tbody.innerHTML = events.map(event => `
        <tr>
            <td>${event.event_id}</td>
            <td>${new Date(event.time).toLocaleString()}</td>
            <td>${event.type}</td>
            <td>
                <span class="badge ${event.is_anomaly ? 'bg-danger' : 'bg-success'}">
                    ${event.is_anomaly ? 'Yes' : 'No'}
                </span>
            </td>
        </tr>
    `).join('');
}

// Mock data update (replace with actual API calls)
setInterval(() => {
    // Update chart
    const now = new Date();
    eventStats.data.labels.push(now.toLocaleTimeString());
    eventStats.data.datasets[0].data.push(Math.floor(Math.random() * 100));
    
    if (eventStats.data.labels.length > 10) {
        eventStats.data.labels.shift();
        eventStats.data.datasets[0].data.shift();
    }
    eventStats.update();
    
    // Update recent events
    updateRecentEvents([
        {
            event_id: `EVT-${Math.random().toString(36).substr(2, 9)}`,
            time: now.toISOString(),
            type: 'a-f-G-U-C',
            is_anomaly: Math.random() > 0.8
        }
    ]);
}, 5000);
