document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.status === 201) {
            // التعديل هنا: حفظ التوكن والدخول مباشرة
            saveToken(data.token); 
            alert('Registration Successful! Logging you in...');
            window.location.href = 'app.html'; // توجيه للتطبيق مباشرة
        } else {
            alert(data.message || 'Registration failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong.');
    }
});