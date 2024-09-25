function showTab(event, tabId) {
            event.preventDefault();

            // Hide all tab contents
            var tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(function(tab) {
                tab.classList.remove('active');
            });

            // Remove active class from all tab links
            var links = document.querySelectorAll('.tab-links a');
            links.forEach(function(link) {
                link.classList.remove('active');
            });

            // Show the selected tab and mark the link as active
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }