function toggleSearchButton() {
    const searchInput = document.getElementById('query');
    const searchButton = document.getElementById('search-btn');

    if (searchInput.value.length > 0) {
        searchButton.style.display = 'block';
    } else {
        searchButton.style.display = 'none';
    }
}

							