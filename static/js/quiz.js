$(document).ready(function () {
    // Fonction pour charger les oiseaux en fonction de la liste publique et de la région
    function loadBirds(listeId = "", region = "") {
        const params = {};
        if (listeId) params.liste_id = listeId;
        if (region) params.region = region;

        $.get('/quiz-data', params, function (data) {
            $('#bird-list').empty(); // Vide la liste actuelle

            // Créer une liste des ID des oiseaux à présélectionner
            const preselectedIds = data.map(oiseau => oiseau.id_oiseau);

            // Ajouter chaque oiseau à la liste HTML
            data.forEach(oiseau => {
                $('#bird-list').append(
                    `<li>
                        <input type="checkbox" value="${oiseau.id_oiseau}" 
                            class="oiseau-checkbox" 
                            ${preselectedIds.includes(oiseau.id_oiseau) ? 'checked' : ''}>
                        ${oiseau.nom_français} (${oiseau.nom_scientifique})
                        <button class="play-chants" data-oiseau-id="${oiseau.id_oiseau}">Écouter</button>
                    </li>`
                );
            });
        }).fail(function () {
            alert("Une erreur s'est produite lors du chargement des oiseaux.");
        });
    }

    // Fonction pour jouer ou arrêter les chants associés à un oiseau
    function playChants(oiseauId, button) {
        const audioPlayer = $('#audio-player')[0]; // Accéder à l'élément audio
        const isPlaying = button.attr('data-playing') === 'true';

        if (isPlaying) {
            // Arrêter le lecteur si un chant est en cours de lecture
            audioPlayer.pause();
            audioPlayer.currentTime = 0; // Remettre à zéro
            button.text('Écouter');
            button.attr('data-playing', 'false');
        } else {
            // Charger et jouer un chant
            $.get(`/get-chants/${oiseauId}`, function (data) {
                if (data.length > 0) {
                    // Choisir un chant aléatoire parmi ceux récupérés
                    const chant = data[Math.floor(Math.random() * data.length)];
                    audioPlayer.src = chant.chemin_chant;
                    audioPlayer.play();

                    // Mettre à jour l'état du bouton
                    button.text('Arrêter');
                    button.attr('data-playing', 'true');

                    // Arrêter le chant lorsque la lecture se termine
                    audioPlayer.onended = function () {
                        button.text('Écouter');
                        button.attr('data-playing', 'false');
                    };
                } else {
                    alert("Aucun chant trouvé pour cet oiseau.");
                }
            });
        }
    }

    // Ajouter un gestionnaire pour le bouton "Sélectionner tous les oiseaux"
    $('#select-all-birds').on('click', function () {
        const checkboxes = $('#bird-list .oiseau-checkbox');
        const allChecked = checkboxes.length === checkboxes.filter(':checked').length;

        // Si tous les oiseaux sont déjà sélectionnés, les désélectionner, sinon les sélectionner
        checkboxes.prop('checked', !allChecked);
    });

    // Écouteur pour les boutons "Écouter"
    $('#bird-list').on('click', '.play-chants', function () {
        const button = $(this);
        const oiseauId = button.data('oiseau-id');
        playChants(oiseauId, button);
    });

    // Réagir au changement de la liste publique
    $('#public-list-select').on('change', function () {
        const selectedListId = $(this).val();
        const selectedRegion = $('#region-select').val(); // Récupérer la région sélectionnée
        loadBirds(selectedListId, selectedRegion);
    });

    // Réagir au changement de liste
    $('#private-list-select').on('change', function () {
        const selectedListId = $(this).val();
        const selectedRegion = $('#region-select').val(); // Récupérer la région sélectionnée
        loadBirds(selectedListId, selectedRegion);
    });

    // Réagir au changement de région
    $('#region-select').on('change', function () {
        const selectedRegion = $(this).val();
        const selectedListId = $('#public-list-select').val(); // Récupérer la liste sélectionnée
        loadBirds(selectedListId, selectedRegion);
    });

    // Charger les oiseaux initiaux si une région ou une liste est déjà sélectionnée (optionnel)
    const initialListId = $('#public-list-select').val();
    const initialRegion = $('#region-select').val();
    loadBirds(initialListId, initialRegion);

    // Générer une liste aléatoire
    $('#generate-random').click(function () {
        const selectedRegion = $('#region-select').val();
        $.get('/quiz-random', { region: selectedRegion }, function (data) {
            $('#bird-list').empty();

            // Créer une liste des ID des oiseaux à présélectionner
            const preselectedIds = data.map(oiseau => oiseau.id_oiseau);

            data.forEach(oiseau => {
                $('#bird-list').append(
                    `<li>
                        <input type="checkbox" value="${oiseau.id_oiseau}" 
                            class="oiseau-checkbox" 
                            ${preselectedIds.includes(oiseau.id_oiseau) ? 'checked' : ''}>
                        ${oiseau.nom_français} (${oiseau.nom_scientifique})
                        <button class="play-chants" data-oiseau-id="${oiseau.id_oiseau}">Écouter</button>
                    </li>`
                );
            });
        }).fail(function () {
            alert("Une erreur s'est produite lors du chargement des oiseaux.");
        });
    });


    // Afficher / cacher la section des paramètres au clic du bouton "Paramètres"
    $('#settings-button').click(function () {
        $('#settings-section').toggle(); // Affiche ou masque la section des paramètres
    });

    // Sauvegarder les paramètres au clic du bouton "Sauvegarder"
    $('#save-settings').click(function () {
        const numQuestions = $('#num-questions').val();
        const numOptions = $('#num-options').val();

        // Sauvegarde dans localStorage
        localStorage.setItem('numQuestions', numQuestions);
        localStorage.setItem('numOptions', numOptions);

        // Masquer la section des paramètres après la sauvegarde
        $('#settings-section').hide();
    });


    // Précharger les valeurs depuis localStorage si elles existent
    if (localStorage.getItem('numQuestions') && localStorage.getItem('numOptions')) {
        $('#num-questions').val(localStorage.getItem('numQuestions'));
        $('#num-options').val(localStorage.getItem('numOptions'));
    }

    // Lancer le quiz
    $('#start-quiz').click(function () {
        const selected = $('#bird-list input:checked').map(function () {
            return $(this).val();
        }).get();

        // Récupérer les paramètres depuis localStorage
        const numQuestions = localStorage.getItem('numQuestions') || 5;  // Valeur par défaut 5
        const numOptions = localStorage.getItem('numOptions') || 3;  // Valeur par défaut 3


        $.ajax({
            url: '/start-quiz',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                selected_ids: selected,
                num_questions: numQuestions,
                num_options: numOptions
            }),
            success: function (data) {
                $('#quiz-section').empty(); // Vide la section du quiz avant de la remplir
                let currentQuestionIndex = 0; // Commencer avec la première question

                function showQuestion(index) {
                    const question = data[index];
                    if (question.audio) {
                        const audioUrl = `${question.audio}`;  // Lien vers le fichier audio

                        $('#quiz-section').html(
                            `<div class="question">
                                <p class="question-text">Question ${index + 1}: </p>
                                <audio controls src="${audioUrl}"></audio>
                                <div class="options">
                                    ${question.options.map(option => `
                                        <button class="answer" data-id="${option.id_oiseau}" data-correct="${option.correct}" data-correct-name="${question.correct_name}">
                                            ${option.nom_français}
                                        </button>
                                    `).join('')}
                                </div>
                                <p id="result-${index}" class="result-message"></p>
                                <button id="next-button" class="next-button" style="display:none;">Question suivante</button>
                            </div>`
                        );

                        // Ajouter l'événement de clic sur les réponses
                        $('.answer').click(function () {
                            const isCorrect = $(this).data('correct');
                            const correctName = $(this).data('correct-name');
                            const resultMessage = $('#result-' + index);

                            // Afficher le message de résultat
                            if (isCorrect) {
                                resultMessage.text('Juste !').css('color', 'green');
                            } else {
                                resultMessage.text(`Faux ! Essaie les autres réponses !`).css('color', 'red');
                            }

                            // Afficher le bouton "Question suivante"
                            $('#next-button').show();
                        });

                        // Ajouter l'événement pour le bouton "Question suivante"
                        $('#next-button').click(function () {
                            // Cacher le bouton pour la question suivante
                            $(this).hide();

                            // Passer à la question suivante
                            if (index + 1 < data.length) {
                                showQuestion(index + 1);
                            } else {
                                $('#quiz-section').append('<p>Le quiz est terminé !</p>');
                            }
                        });
                    } else {
                        console.error('Le fichier audio est manquant pour cette question.');
                    }
                }

                // Commencer avec la première question
                showQuestion(currentQuestionIndex);
            },
            error: function (xhr, status, error) {
                console.error('Erreur lors de l\'envoi de la requête : ', error);
            }
        });
    });
});