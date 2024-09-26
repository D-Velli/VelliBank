// Function to calculate total and update progress ring
function updateProgress(solde, credit) {
    const total = solde + credit;
    const percentage = (solde / total) * 100;

    // Update progress ring
    document
        .getElementById("progressRing")
        .style.setProperty("--percent", `${percentage}%`);

    // Update solde and credit text
    document.getElementById(
        "solde"
    ).textContent = `${solde.toLocaleString()} $`;
    document.getElementById(
        "credit"
    ).textContent = `${credit.toLocaleString()} $`;
}

// Sample data
const soldeDuJour = 2146.54;
const creditDisponible = 1853;

// Initialize progress ring with data
updateProgress(soldeDuJour, creditDisponible);

// Tab switching functionality
function showTab(event, tabId) {
    event.preventDefault();

    // Hide all tab contents
    var tabs = document.querySelectorAll(".tab-content");
    tabs.forEach(function (tab) {
        tab.classList.remove("active");
    });

    // Remove active class from all tab links
    var links = document.querySelectorAll(".tab-links a");
    links.forEach(function (link) {
        link.classList.remove("active");
    });

    // Show the selected tab and mark the link as active
    document.getElementById(tabId).classList.add("active");
    event.target.classList.add("active");
}