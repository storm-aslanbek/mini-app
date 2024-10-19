document.addEventListener('DOMContentLoaded', function () {
    const generateTaskBtn = document.getElementById('generate-task-btn');
    const taskContainer = document.getElementById('task-container');

    generateTaskBtn.addEventListener('click', function () {
        fetch('/generate_task/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.task) {
                taskContainer.innerHTML = `<p>${data.task}</p>`;
            } else {
                taskContainer.innerHTML = `<p>Қате: тапсырманы алу мүмкін емес</p>`;
            }
        })
        .catch(error => {
            taskContainer.innerHTML = `<p>Қате: ${error}</p>`;
        });
    });
});
