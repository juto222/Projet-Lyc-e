// Gestion des clics sur les boutons de modules
document.addEventListener('DOMContentLoaded', function() {
    const moduleButtons = document.querySelectorAll('.module-btn');
    
    moduleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const moduleCard = this.closest('.module-card');
            const moduleTitle = moduleCard.querySelector('.module-title').textContent;
            
            alert(`Ouverture du module : ${moduleTitle}\n\nCette fonctionnalité sera disponible prochainement.`);
        });
    });
    
    // Animation des cartes au survol
    const cards = document.querySelectorAll('.module-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
    
    // Gestion du menu de navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (!this.classList.contains('active')) {
                e.preventDefault();
                navItems.forEach(nav => nav.classList.remove('active'));
                this.classList.add('active');
                
                const section = this.textContent.trim();
                console.log(`Navigation vers : ${section}`);
            }
        });
    });
    
    // Bouton d'aide
    const helpSection = document.querySelector('.help-section');
    if (helpSection) {
        helpSection.addEventListener('click', function() {
            alert('Section d\'aide\n\nPour toute question, contactez : secnumacademie@ssi.gouv.fr');
        });
    }
});

// Fonction pour mettre à jour les statistiques (simulé)
function updateModuleStats(moduleId, time, score) {
    const modules = document.querySelectorAll('.module-card');
    if (modules[moduleId]) {
        const timeElement = modules[moduleId].querySelector('.stat:first-child span:last-child');
        const scoreElement = modules[moduleId].querySelector('.score-value');
        
        if (timeElement) {
            timeElement.textContent = `Temps passé : ${time}`;
        }
        if (scoreElement) {
            scoreElement.textContent = `${score}%`;
            scoreElement.classList.toggle('zero', score === 0);
        }
    }
}
