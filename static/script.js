// Expand and Hide Navbar
function toggleNav() {
    var navbar = document.getElementById('navbar');
    if (navbar.style.display === 'none') {
        navbar.style.display = 'block'; // Show the navbar
    } else {
        navbar.style.display = 'none'; // Hide the navbar
    }
}