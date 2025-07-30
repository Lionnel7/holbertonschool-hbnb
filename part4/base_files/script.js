document.addEventListener('DOMContentLoaded', () => {
    // Fonction pour mettre à jour l'affichage du header
    function updateHeaderVisibility() {
        const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
        const userEmail = localStorage.getItem('userEmail');

        const loginLink = document.getElementById('login-link');
        let logoutButton = document.getElementById('logout-button'); // Peut être null au début
        let welcomeMessage = document.getElementById('welcome-message'); // Peut être null au début

        if (isLoggedIn) {
            // Masquer le lien "Login"
            if (loginLink) {
                loginLink.style.display = 'none';
            }

            // Créer et afficher le bouton "Logout" s'il n'existe pas
            if (!logoutButton) {
                const navActions = document.querySelector('header .nav-actions');
                logoutButton = document.createElement('a');
                logoutButton.id = 'logout-button';
                logoutButton.className = 'login-button'; // Réutilise la classe de style du bouton login
                logoutButton.href = '#'; // Ou une URL de déconnexion si tu en avais une
                logoutButton.textContent = 'Logout';
                navActions.appendChild(logoutButton);
            } else {
                logoutButton.style.display = 'inline-block'; // S'assurer qu'il est visible
            }

            // Créer et afficher le message de bienvenue s'il n'existe pas
            if (!welcomeMessage) {
                const navActions = document.querySelector('header .nav-actions');
                welcomeMessage = document.createElement('span');
                welcomeMessage.id = 'welcome-message';
                welcomeMessage.className = 'welcome-message'; // Nouvelle classe pour le style
                navActions.insertBefore(welcomeMessage, loginLink || logoutButton); // Insérer avant le login/logout
            }
            if (userEmail) {
                welcomeMessage.textContent = `Welcome ${userEmail}`;
                welcomeMessage.style.display = 'inline-block'; // S'assurer qu'il est visible
            } else {
                welcomeMessage.style.display = 'none';
            }
            
            // Gérer le clic sur le bouton "Logout"
            if (logoutButton) {
                logoutButton.onclick = (event) => {
                    event.preventDefault(); // Empêche le rechargement de la page
                    localStorage.removeItem('isLoggedIn');
                    localStorage.removeItem('userEmail');
                    updateHeaderVisibility(); // Mettre à jour le header après déconnexion
                    window.location.href = 'index.html'; // Rediriger vers la page d'accueil
                };
            }

        } else {
            // Afficher le lien "Login"
            if (loginLink) {
                loginLink.style.display = 'inline-block';
            }
            // Masquer le bouton "Logout" s'il existe
            if (logoutButton) {
                logoutButton.style.display = 'none';
            }
            // Masquer le message de bienvenue s'il existe
            if (welcomeMessage) {
                welcomeMessage.style.display = 'none';
            }
        }
    }

    // Appeler la fonction au chargement de la page
    updateHeaderVisibility();

    // Gestion du formulaire de connexion sur login.html
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Empêche le comportement par défaut du formulaire

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Simuler une connexion réussie
            // Dans un vrai projet, tu enverrais ces données à un serveur
            if (email === 'test@example.com' && password === 'password123') {
                localStorage.setItem('isLoggedIn', 'true');
                localStorage.setItem('userEmail', email);
                alert('Connexion réussie !');
                window.location.href = 'index.html'; // Rediriger vers la page d'accueil
            } else {
                alert('Email ou mot de passe incorrect.');
            }
        });
    }

    // Placeholder pour d'autres fonctionnalités JavaScript futures (comme le filtre)
    // const priceFilter = document.getElementById('price-filter');
    // if (priceFilter) {
    //     priceFilter.addEventListener('change', (event) => {
    //         const maxPrice = event.target.value;
    //         console.log(`Filtrer par prix max: ${maxPrice}`);
    //         // Logique de filtrage des lieux ici
    //     });
    // }
});
