// ERP POC Manager JavaScript utilities

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// CSRF token utility for AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set up CSRF token for AJAX
const csrftoken = getCookie('csrftoken');

// Dashboard utilities
class Dashboard {
    static updateTaskStats() {
        // Refresh task statistics on dashboard
        fetch('/api/task-stats/')
            .then(response => response.json())
            .then(data => {
                document.querySelector('#total-tasks').textContent = data.total;
                document.querySelector('#completed-tasks').textContent = data.completed;
                document.querySelector('#inprogress-tasks').textContent = data.inprogress;
                document.querySelector('#todo-tasks').textContent = data.todo;
            })
            .catch(error => console.error('Error updating task stats:', error));
    }

    static createTaskChart(todoCount, inprogressCount, completedCount) {
        const ctx = document.getElementById('taskChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['To Do', 'In Progress', 'Done'],
                datasets: [{
                    data: [todoCount, inprogressCount, completedCount],
                    backgroundColor: ['#dc3545', '#ffc107', '#28a745'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Team selection utilities
class TeamSelection {
    static calculateScore(javaScore, sqlScore, teamFit) {
        return parseInt(javaScore) + parseInt(sqlScore) + parseInt(teamFit);
    }

    static selectTopCandidates(candidates, count = 4) {
        return candidates
            .sort((a, b) => b.totalScore - a.totalScore)
            .slice(0, count);
    }

    static highlightSelected(candidateIds) {
        candidateIds.forEach(id => {
            const card = document.querySelector(`[data-candidate-id="${id}"]`);
            if (card) {
                card.classList.add('selected');
            }
        });
    }
}

// Task management utilities
class TaskManager {
    static updateTaskStatus(taskId, newStatus) {
        fetch(`/api/tasks/${taskId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ status: newStatus })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Simple refresh for now
            }
        })
        .catch(error => console.error('Error updating task:', error));
    }

    static createGanttView(tasks) {
        // Simple Gantt-like visualization
        const container = document.getElementById('gantt-container');
        if (!container) return;

        tasks.forEach(task => {
            const taskBar = document.createElement('div');
            taskBar.className = `task-bar week-${task.week} status-${task.status}`;
            taskBar.innerHTML = `
                <span class="task-title">${task.title}</span>
                <span class="task-duration">${task.duration}d</span>
            `;
            container.appendChild(taskBar);
        });
    }
}

// Meeting utilities
class MeetingManager {
    static scheduleRecurringMeetings(type, startDate, endDate, frequency) {
        fetch('/api/meetings/schedule-recurring/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                type: type,
                start_date: startDate,
                end_date: endDate,
                frequency: frequency
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`${data.created_count} meetings scheduled successfully`);
                location.reload();
            }
        })
        .catch(error => console.error('Error scheduling meetings:', error));
    }
}

// Performance monitoring
class PerformanceMonitor {
    static trackUserActivity(activity, details = {}) {
        fetch('/api/track-activity/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                activity: activity,
                details: details,
                timestamp: new Date().toISOString()
            })
        })
        .catch(error => console.error('Error tracking activity:', error));
    }

    static generateWeeklyReport() {
        fetch('/api/reports/weekly/')
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'weekly-report.pdf';
                a.click();
            })
            .catch(error => console.error('Error generating report:', error));
    }
}

// External tool integration
class ExternalTools {
    static runGitAnalysis() {
        const button = document.querySelector('#git-analysis-btn');
        if (button) {
            button.disabled = true;
            button.textContent = 'Running...';
        }

        fetch('/run-monitoring/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Git analysis completed successfully!');
                console.log('Analysis results:', data.results);
            } else {
                alert('Error running git analysis: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error running git analysis');
        })
        .finally(() => {
            if (button) {
                button.disabled = false;
                button.textContent = 'Run Git Analysis';
            }
        });
    }

    static openExternalTool(toolName, url) {
        // Track usage
        PerformanceMonitor.trackUserActivity('external_tool_access', { tool: toolName });
        window.open(url, '_blank');
    }
}

// Form enhancements
class FormEnhancements {
    static setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    static setupDateTimePickers() {
        const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
        dateInputs.forEach(input => {
            // Set minimum date to today
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            input.min = `${year}-${month}-${day}T${hours}:${minutes}`;
        });
    }
}

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', function() {
    FormEnhancements.setupFormValidation();
    FormEnhancements.setupDateTimePickers();
    
    // Track page view
    PerformanceMonitor.trackUserActivity('page_view', { 
        page: window.location.pathname,
        title: document.title 
    });
});