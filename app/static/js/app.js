// =========================================================
// REGISTER FORM
// =========================================================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", function (event) {

        const password =
            document.getElementById("password").value;

        const confirmPassword =
            document.getElementById("confirm_password").value;

        const passwordError =
            document.getElementById("passwordError");


        if (password !== confirmPassword) {

            event.preventDefault();

            passwordError.textContent =
                "Passwords do not match.";

            return;
        }


        passwordError.textContent = "";
    });
}


// =========================================================
// TOGGLE TASK COMPLETION
// =========================================================

async function toggleTask(taskId) {

    try {

        const response = await fetch(
            `/tasks/${taskId}/complete`,
            {
                method: "PATCH"
            }
        );


        if (!response.ok) {

            if (response.status === 401) {
                window.location.href = "/login";
                return;
            }

            alert("Unable to update task.");
            return;
        }


        window.location.reload();

    } catch (error) {

        console.error(
            "Error completing task:",
            error
        );

        alert(
            "Something went wrong. Please try again."
        );
    }
}


// =========================================================
// DELETE TASK
// =========================================================

async function deleteTask(taskId) {

    const confirmed = confirm(
        "Are you sure you want to delete this task?"
    );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `/tasks/${taskId}`,
            {
                method: "DELETE"
            }
        );


        if (!response.ok) {

            if (response.status === 401) {
                window.location.href = "/login";
                return;
            }

            alert("Unable to delete task.");
            return;
        }


        window.location.reload();

    } catch (error) {

        console.error(
            "Error deleting task:",
            error
        );

        alert(
            "Something went wrong. Please try again."
        );
    }
}


// =========================================================
// EDIT TASK
// =========================================================

async function editTask(taskId) {

    try {

        const response = await fetch(
            `/tasks/${taskId}`
        );


        if (!response.ok) {

            if (response.status === 401) {
                window.location.href = "/login";
                return;
            }

            alert("Unable to load task.");
            return;
        }


        const task = await response.json();


        const newTitle = prompt(
            "Edit task title:",
            task.title
        );


        if (newTitle === null) {
            return;
        }


        const trimmedTitle = newTitle.trim();


        if (!trimmedTitle) {

            alert(
                "Task title cannot be empty."
            );

            return;
        }


        const newDescription = prompt(
            "Edit task description:",
            task.description || ""
        );


        if (newDescription === null) {
            return;
        }


        const updatedTask = {

            title: trimmedTitle,

            description:
                newDescription.trim() || null,

            completed: task.completed,

            due_time: task.due_time,

            reminder_time: task.reminder_time
        };


        const updateResponse = await fetch(
            `/tasks/${taskId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(updatedTask)
            }
        );


        if (!updateResponse.ok) {

            if (updateResponse.status === 401) {
                window.location.href = "/login";
                return;
            }

            alert("Unable to update task.");
            return;
        }


        window.location.reload();

    } catch (error) {

        console.error(
            "Error editing task:",
            error
        );

        alert(
            "Something went wrong. Please try again."
        );
    }
}


// =========================================================
// TASK BUTTON EVENT HANDLERS
// =========================================================

document.addEventListener(
    "click",
    function (event) {

        const button =
            event.target.closest(
                "[data-action]"
            );


        if (!button) {
            return;
        }


        const action =
            button.dataset.action;

        const taskId =
            button.dataset.taskId;


        if (!taskId) {
            return;
        }


        if (action === "complete") {

            toggleTask(taskId);

        }


        else if (action === "delete") {

            deleteTask(taskId);

        }


        else if (action === "edit") {

            editTask(taskId);

        }

    }
);


// =========================================================
// REMINDER CHECK
// =========================================================

function checkReminders() {

    const taskCards =
        document.querySelectorAll(
            ".task-card"
        );


    if (!taskCards.length) {
        return;
    }


    const now = new Date();


    taskCards.forEach(function (card) {

        const reminderElement =
            card.querySelector(
                ".task-reminder"
            );


        if (!reminderElement) {
            return;
        }


        const reminderTimeString =
            reminderElement.dataset.reminderTime;


        if (!reminderTimeString) {
            return;
        }


        const reminderTime =
            new Date(reminderTimeString);


        if (
            !Number.isNaN(reminderTime.getTime()) &&
            reminderTime <= now &&
            !card.dataset.reminded
        ) {

            card.dataset.reminded = "true";


            const titleElement =
                card.querySelector(
                    ".task-info h4"
                );


            const taskTitle =
                titleElement
                    ? titleElement.textContent.trim()
                    : "You have a task";


            if (
                "Notification" in window &&
                Notification.permission === "granted"
            ) {

                new Notification(
                    "TodoFlow Reminder",
                    {
                        body: taskTitle
                    }
                );

            } else {

                console.log(
                    "Task reminder:",
                    taskTitle
                );
            }
        }

    });
}


// =========================================================
// REQUEST NOTIFICATION PERMISSION
// =========================================================

async function requestNotificationPermission() {

    if (
        "Notification" in window &&
        Notification.permission === "default"
    ) {

        try {

            await Notification.requestPermission();

        } catch (error) {

            console.error(
                "Notification permission error:",
                error
            );
        }
    }
}


// =========================================================
// INITIALIZE
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        requestNotificationPermission();

        checkReminders();

        setInterval(
            checkReminders,
            30000
        );

    }
);