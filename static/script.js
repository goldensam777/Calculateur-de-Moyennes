// Données globales
let matieres = [];

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    chargerMatieres();
    attacherEvenements();
});

// Charger les matières
function chargerMatieres() {
    fetch('/api/matieres')
        .then(response => response.json())
        .then(data => {
            matieres = data;
            afficherMatieres();
        })
        .catch(error => console.error('Erreur:', error));
}

// Afficher les matières
function afficherMatieres() {
    const liste = document.getElementById('matieres-list');
    liste.innerHTML = '';

    matieres.forEach(m => {
        const div = document.createElement('div');
        div.className = 'matiere-item';
        div.innerHTML = `
            <input type="checkbox" id="check-${m.nom}" checked>
            <div class="matiere-info">
                <div class="matiere-nom">${m.nom}</div>
                <div class="matiere-coeff">Coefficient: ${m.coefficient}</div>
            </div>
            <input type="number" 
                   class="matiere-input" 
                   min="0" 
                   max="20" 
                   step="0.5" 
                   value="0"
                   id="note-${m.nom}"
                   placeholder="0">
            <span>/20</span>
        `;
        liste.appendChild(div);
    });
}

// Attacher les événements
function attacherEvenements() {
    document.getElementById('btn-calculer').addEventListener('click', calculer);
    document.getElementById('btn-reset').addEventListener('click', reinitialiser);
    document.getElementById('btn-ajouter').addEventListener('click', ouvrirModal);
    document.getElementById('btn-annuler').addEventListener('click', fermerModal);
    document.querySelector('.close').addEventListener('click', fermerModal);
    document.getElementById('form-matiere').addEventListener('submit', ajouterMatiere);

    // Fermer le modal en cliquant en dehors
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('modal-ajouter');
        if (e.target === modal) {
            fermerModal();
        }
    });
}

// Calculer la moyenne
function calculer() {
    const donnees = {
        matieres: matieres.map(m => ({
            nom: m.nom,
            coefficient: m.coefficient,
            note: document.getElementById(`note-${m.nom}`).value,
            selectionnee: document.getElementById(`check-${m.nom}`).checked
        }))
    };

    fetch('/api/calculer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(donnees)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            afficherErreur(data.error);
        } else {
            afficherResultats(data);
        }
    })
    .catch(error => {
        afficherErreur('Erreur serveur: ' + error);
    });
}

// Afficher les résultats
function afficherResultats(data) {
    const section = document.getElementById('resultats');
    const content = document.getElementById('resultats-content');

    let html = `
        <div class="resultat-moyenne">
            <h3>Votre moyenne pondérée</h3>
            <div class="resultat-score">${data.moyenne}/20</div>
            <div class="resultat-appreciation" style="background-color: ${data.couleur}; color: white;">
                ${data.appreciation}
            </div>
        </div>
        <h3 style="margin-top: 20px; margin-bottom: 15px;">Matières sélectionnées</h3>
    `;

    data.matieres.forEach(m => {
        html += `
            <div class="resultat-item">
                <div class="resultat-nom">${m.nom}</div>
                <div class="resultat-details">
                    Note: <strong>${m.note.toFixed(2)}</strong> | 
                    Coefficient: <strong>${m.coefficient}</strong>
                </div>
            </div>
        `;
    });

    content.innerHTML = html;
    section.style.display = 'block';
    section.scrollIntoView({ behavior: 'smooth' });
}

// Afficher une erreur
function afficherErreur(message) {
    const section = document.getElementById('resultats');
    const content = document.getElementById('resultats-content');
    content.innerHTML = `<div class="error-message">${message}</div>`;
    section.style.display = 'block';
    section.scrollIntoView({ behavior: 'smooth' });
}

// Réinitialiser
function reinitialiser() {
    matieres.forEach(m => {
        document.getElementById(`note-${m.nom}`).value = '0';
    });
    document.getElementById('resultats').style.display = 'none';
}

// Modal - Ouvrir
function ouvrirModal() {
    document.getElementById('modal-ajouter').style.display = 'flex';
    document.getElementById('nom-matiere').focus();
}

// Modal - Fermer
function fermerModal() {
    document.getElementById('modal-ajouter').style.display = 'none';
    document.getElementById('form-matiere').reset();
}

// Ajouter une matière
function ajouterMatiere(e) {
    e.preventDefault();

    const nom = document.getElementById('nom-matiere').value.trim();
    const coefficient = parseFloat(document.getElementById('coeff-matiere').value);

    if (!nom) {
        alert('Veuillez entrer un nom de matière');
        return;
    }

    if (coefficient <= 0) {
        alert('Le coefficient doit être supérieur à 0');
        return;
    }

    fetch('/api/ajouter-matiere', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nom, coefficient })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Erreur: ' + data.error);
        } else {
            chargerMatieres();
            fermerModal();
            afficherSucces(`La matière "${nom}" a été ajoutée avec succès`);
        }
    })
    .catch(error => {
        alert('Erreur: ' + error);
    });
}

// Afficher un message de succès
function afficherSucces(message) {
    const section = document.getElementById('resultats');
    const content = document.getElementById('resultats-content');
    content.innerHTML = `<div class="success-message">${message}</div>`;
    section.style.display = 'block';
    setTimeout(() => {
        section.style.display = 'none';
    }, 3000);
}
