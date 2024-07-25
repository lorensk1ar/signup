document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;

    fetch('http://127.0.0.1:5000/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ first_name: firstName, last_name: lastName, email: email }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').innerText = data.message;
        if (data.success) {
            document.getElementById('signupForm').reset();
        }
    })
    .catch(error => {
        document.getElementById('message').innerText = 'An error occurred.';
        console.error('Error:', error);
    });
});