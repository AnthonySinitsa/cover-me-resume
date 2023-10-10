function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("deleteAccountBtn").addEventListener("click", function() {
        document.getElementById("deleteAccountModal").style.display = "block";
    });

    document.getElementById("confirmDeleteBtn").addEventListener("click", function() {
        fetch('/delete_account/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({confirm: true})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = '/';
            } else {
                alert("Error deleting account.");
            }
        });
    });

    document.getElementById("cancelDeleteBtn").addEventListener("click", function() {
        document.getElementById("deleteAccountModal").style.display = "none";
    });
});
