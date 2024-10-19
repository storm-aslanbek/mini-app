document.getElementById("generate-task-btn").addEventListener("click", function() {
    fetch("/generate-task/")
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                document.getElementById("task-container").innerText = data.task;
            } else
