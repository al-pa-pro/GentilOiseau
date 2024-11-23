$(document).ready(function () {
    // Fonction pour charger les oiseaux en fonction de la région ou de la liste sélectionnée
    function loadBirds(region = "") {
        // Si une région est sélectionnée, on charge les oiseaux par région, sinon par liste
        $.get('/quiz-data', { region: region }, function (data) {
            $('#bird-list').empty(); // Vide la liste actuelle
            data.forEach(oiseau => {
                $('#bird-list').append(
                    `<li>
                        <input type="checkbox" value="${oiseau.id_oiseau}">
                        ${oiseau.nom_français} (${oiseau.nom_scientifique})
                        <button class="play-chants" data-oiseau-id="${oiseau.id_oiseau}">Écouter</button>
                    </li>`
                );
            });
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

    // Délégation d'événements : écouteur de clic pour les boutons "Écouter un chant"
    $('#bird-list').on('click', '.play-chants', function () {
        const button = $(this);
        const oiseauId = button.data('oiseau-id');
        playChants(oiseauId, button);
    });

    // Charger les oiseaux initialement (sans filtre)
    loadBirds();

    // Réagir au changement de région
    $('#region-select').on('change', function () {
        const selectedRegion = $(this).val();
        loadBirds(selectedRegion);
    });




    // Générer une liste aléatoire
    $('#generate-random').click(function () {
        const selectedRegion = $('#region-select').val();
        $.get('/quiz-random', { region: selectedRegion }, function (data) {
            $('#bird-list').empty();
            data.forEach(oiseau => {
                $('#bird-list').append(
                    `<li>
                        <input type="checkbox" value="${oiseau.id_oiseau}" checked>
                        ${oiseau.nom_français} (${oiseau.nom_scientifique})
                        <button class="play-chants" data-oiseau-id="${oiseau.id_oiseau}">Écouter</button>
                    </li>`
                );
            });
        });
    });

    // Lancer le quiz
    $('#start-quiz').click(function () {
        const selected = $('#bird-list input:checked').map(function () {
            return $(this).val();
        }).get();

        $.ajax({
            url: '/start-quiz',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ selected_ids: selected }),
            success: function (data) {
                $('#quiz-section').empty();
                data.forEach((question, index) => {
                    if (question.audio) {
                        const audioUrl = `${question.audio}`;  // Lien vers le fichier audio
                        
                        $('#quiz-section').append(
                            `<div class="question">
                                <audio controls src="${audioUrl}"></audio>
                                <div>
                                    ${question.options.map(option => `
                                        <button class="answer" data-id="${option.id_oiseau}" data-correct="${option.correct}" data-correct-name="${question.correct_name}">
                                            ${option.nom_français}
                                        </button>
                                    `).join('')}
                                </div>
                                <p id="result-${index}" class="result-message"></p>
                            </div>`
                        );
                    } else {
                        console.error('Le fichier audio est manquant pour cette question.');
                    }
                });

                // Ajouter l'événement de clic sur les réponses
                $('.answer').click(function () {
                    const isCorrect = $(this).data('correct');
                    const correctName = $(this).data('correct-name');
                    const questionIndex = $(this).closest('.question').index();
                    const resultMessage = $('#result-' + questionIndex);

                    if (isCorrect) {
                        resultMessage.text('Juste !').css('color', 'green');
                    } else {
                        resultMessage.text(`Faux ! La bonne réponse était : ${correctName}.`).css('color', 'red');
                    }

                });

            },
            error: function (xhr, status, error) {
                console.error('Erreur lors de l\'envoi de la requête : ', error);
            }
        });
    });


});
