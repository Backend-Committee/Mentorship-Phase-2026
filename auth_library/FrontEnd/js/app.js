// Ensure user is logged in
checkAuth();

// --- DOM Elements ---
const resultArea = document.getElementById('resultArea');
const bookTitle = document.getElementById('bookTitle');
const bookAuthor = document.getElementById('bookAuthor');
const bookDownloads = document.getElementById('bookDownloads');
const bookYear = document.getElementById('bookYear');
const bookImage = document.getElementById('bookImage');
const bookLink = document.getElementById('bookLink');
const messageBox = document.getElementById('messageBox');
const btnAddToFav = document.getElementById('btnAddToFav');
const favoritesGrid = document.getElementById('favoritesGrid');

// --- State Variables ---
let currentBookData = null; // To store the current book object for adding to favorites

// --- Helper Functions ---

// Show messages (Error in Red, Success in Green)
function showMessage(message, type = 'error') {
    messageBox.innerText = message;
    messageBox.classList.remove('hidden');
    messageBox.classList.add('visible');

    if (type === 'success') {
        messageBox.style.backgroundColor = '#d1e7dd';
        messageBox.style.color = '#0f5132';
        messageBox.style.borderColor = '#badbcc';
    } else {
        messageBox.style.backgroundColor = '#fee2e2';
        messageBox.style.color = '#dc2626';
        messageBox.style.borderColor = '#fca5a5';
    }

    // Hide after 3 seconds
    setTimeout(() => {
        messageBox.classList.remove('visible');
    }, 3000);
}

// Reset the main display area
function resetDisplay() {
    messageBox.classList.remove('visible');
    resultArea.classList.add('hidden');
    bookImage.classList.add('hidden');
    bookLink.classList.add('hidden');
    btnAddToFav.classList.add('hidden');
}

// --- Main Logic Functions ---

// 1. Fetch a book (Random, Highest, Oldest)
async function fetchBook(endpoint) {
    resetDisplay();
    
    bookTitle.innerText = "Loading..."; 
    resultArea.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/books/${endpoint}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${getToken()}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            showMessage("Session expired. Please login again.");
            setTimeout(logout, 2000);
            return;
        }

        if (!response.ok) {
            throw new Error('Failed to fetch book');
        }

        const book = await response.json();
        
        // Save current book data to state
        currentBookData = book;
        
        displayBook(book);

    } catch (error) {
        console.error("Error fetching book:", error);
        bookTitle.innerText = "";
        showMessage("Error fetching data. Please try again.");
    }
}

// 2. Display book details on screen
function displayBook(book) {
    // Basic Info
    bookTitle.innerText = book.title || "Unknown Title";
    
    const authorName = book.authors && book.authors.length > 0 
        ? book.authors[0].name 
        : "Unknown Author";
        
    const birthYear = book.authors && book.authors.length > 0 
        ? book.authors[0].birth_year 
        : "N/A";

    bookAuthor.innerText = authorName;
    bookDownloads.innerText = book.download_count || 0;
    bookYear.innerText = birthYear;

    // Image Handling
    const imageUrl = book.formats['image/jpeg'];
    if (imageUrl) {
        bookImage.src = imageUrl;
        bookImage.classList.remove('hidden');
    } else {
        bookImage.classList.add('hidden');
    }

    // Read Link Handling
    const readUrl = book.formats['text/html'] || book.formats['text/plain; charset=utf-8'];
    if (readUrl) {
        bookLink.href = readUrl;
        bookLink.classList.remove('hidden');
    } else {
        bookLink.classList.add('hidden');
    }

    // Show Favorite Button
    btnAddToFav.classList.remove('hidden');
}

// 3. Add to Favorites
btnAddToFav.addEventListener('click', async () => {
    if (!currentBookData) return;

    try {
        const response = await fetch(`${API_BASE_URL}/books/favorite`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify(currentBookData)
        });

        const data = await response.json();
        
        if (response.ok) {
            showMessage("Book added to your favorites!", "success");
            loadFavorites(); // Refresh the list
        } else {
            showMessage(data.message || "Could not add to favorites");
        }
    } catch (error) {
        console.error(error);
        showMessage("Error connecting to server");
    }
});

// 4. Load Favorites List
async function loadFavorites() {
    try {
        const response = await fetch(`${API_BASE_URL}/books/favorites`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${getToken()}` }
        });
        
        if (response.ok) {
            const books = await response.json();
            renderFavorites(books);
        } else {
            favoritesGrid.innerHTML = '<p style="color: red;">Failed to load favorites.</p>';
        }
    } catch (error) {
        console.error("Failed to load favorites", error);
    }
}

// 5. Render Favorites Grid
function renderFavorites(books) {
    favoritesGrid.innerHTML = ''; // Clear current list

    if (!books || books.length === 0) {
        favoritesGrid.innerHTML = '<p style="color: #888;">No favorites yet.</p>';
        return;
    }

    books.forEach(book => {
        // Fallback image if not found
        const imgUrl = book.formats['image/jpeg'] || 'https://via.placeholder.com/150x200?text=No+Cover';
        const readUrl = book.formats['text/html'] || book.formats['text/plain; charset=utf-8'] || '#';

        const card = document.createElement('div');
        card.className = 'fav-card';
        card.innerHTML = `
            <img src="${imgUrl}" alt="Cover">
            <h4>${book.title}</h4>
            <a href="${readUrl}" target="_blank" class="btn-read" style="padding: 5px 10px; font-size: 0.8rem;">Read</a>
        `;
        favoritesGrid.appendChild(card);
    });
}

// --- Event Listeners ---
document.getElementById('btnRandom').addEventListener('click', () => fetchBook('random'));
document.getElementById('btnHighest').addEventListener('click', () => fetchBook('highest'));
document.getElementById('btnOldest').addEventListener('click', () => fetchBook('oldest'));

// --- Initial Load ---
loadFavorites();