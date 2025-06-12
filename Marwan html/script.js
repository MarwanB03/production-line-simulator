// Données du quiz
const quizData = [
    {
        image: "images/memory1.jpg",
        question: "Où avons-nous eu notre premier rendez-vous ?",
        answers: [
            "Au cinéma",
            "Au restaurant",
            "Dans un parc",
            "À la plage"
        ],
        correct: 1
    },
    {
        image: "images/memory2.jpg",
        question: "Quel est mon plat préféré ?",
        answers: [
            "Pizza",
            "Sushi",
            "Pâtes",
            "Burger"
        ],
        correct: 2
    },
    {
        image: "images/memory3.jpg",
        question: "Quelle est notre chanson ?",
        answers: [
            "Perfect - Ed Sheeran",
            "All of Me - John Legend",
            "Thinking Out Loud - Ed Sheeran",
            "A Thousand Years - Christina Perri"
        ],
        correct: 0
    },
    {
        image: "images/memory4.jpg",
        question: "Quel est mon film préféré ?",
        answers: [
            "Titanic",
            "Notebook",
            "La La Land",
            "Before Sunrise"
        ],
        correct: 1
    },
    {
        image: "images/memory5.jpg",
        question: "Quelle est ma couleur préférée ?",
        answers: [
            "Bleu",
            "Rose",
            "Vert",
            "Rouge"
        ],
        correct: 1
    },
    {
        image: "images/memory6.jpg",
        question: "Quel est mon rêve ?",
        answers: [
            "Voyager autour du monde",
            "Avoir une grande maison",
            "Devenir célèbre",
            "Avoir une famille"
        ],
        correct: 0
    }
];

// Variables globales
let currentQuestion = 0;
let score = 0;
let heartsFound = 0;
let gameTimer;
let timeLeft = 30;

// Fonctions de navigation
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

// Fonctions du quiz
function startQuiz() {
    currentQuestion = 0;
    score = 0;
    showPage('quiz-page');
    loadQuestion();
}

function loadQuestion() {
    const question = quizData[currentQuestion];
    const img = document.getElementById('question-image');
    img.src = question.image;
    // Ajouter un gestionnaire d'erreur pour l'image
    img.onerror = function() {
        // Si l'image .jpg ne charge pas, essayer .png
        if (this.src.endsWith('.jpg')) {
            this.src = this.src.replace('.jpg', '.png');
        }
    };
    document.getElementById('question-text').textContent = question.question;
    document.getElementById('current-question').textContent = currentQuestion + 1;
    
    const answerButtons = document.querySelectorAll('.answer-btn');
    answerButtons.forEach((button, index) => {
        button.textContent = question.answers[index];
        button.classList.remove('correct', 'wrong');
        button.disabled = false;
        button.onclick = () => checkAnswer(index);
    });
    
    document.getElementById('next-btn').style.display = 'none';
}

function checkAnswer(selectedIndex) {
    const question = quizData[currentQuestion];
    const answerButtons = document.querySelectorAll('.answer-btn');
    
    answerButtons.forEach(button => {
        button.disabled = true;
    });
    
    if (selectedIndex === question.correct) {
        answerButtons[selectedIndex].classList.add('correct');
        score++;
    } else {
        answerButtons[selectedIndex].classList.add('wrong');
        answerButtons[question.correct].classList.add('correct');
    }
    
    document.getElementById('next-btn').style.display = 'block';
}

function nextQuestion() {
    currentQuestion++;
    
    if (currentQuestion < quizData.length) {
        loadQuestion();
    } else {
        if (score >= 4) {
            startGame();
        } else {
            showPage('fail-page');
        }
    }
}

function restartQuiz() {
    startQuiz();
}

// Fonctions du mini-jeu
function startGame() {
    showPage('game-page');
    heartsFound = 0;
    timeLeft = 30;
    updateGameInfo();
    createHearts();
    startTimer();
}

function createHearts() {
    const gameArea = document.getElementById('game-area');
    gameArea.innerHTML = '';
    
    for (let i = 0; i < 5; i++) {
        const heart = document.createElement('div');
        heart.className = 'heart';
        heart.innerHTML = '❤️';
        heart.style.left = Math.random() * (gameArea.offsetWidth - 40) + 'px';
        heart.style.top = Math.random() * (gameArea.offsetHeight - 40) + 'px';
        
        // Ajouter des propriétés de mouvement aléatoires
        heart.dataset.speedX = (Math.random() - 0.5) * 2; // Vitesse horizontale
        heart.dataset.speedY = (Math.random() - 0.5) * 2; // Vitesse verticale
        
        heart.onclick = () => collectHeart(heart);
        gameArea.appendChild(heart);
    }
    
    // Démarrer l'animation des cœurs
    animateHearts();
}

function animateHearts() {
    const hearts = document.querySelectorAll('.heart:not(.collected)');
    const gameArea = document.getElementById('game-area');
    
    hearts.forEach(heart => {
        let currentX = parseFloat(heart.style.left);
        let currentY = parseFloat(heart.style.top);
        let speedX = parseFloat(heart.dataset.speedX);
        let speedY = parseFloat(heart.dataset.speedY);
        
        // Mettre à jour la position
        currentX += speedX;
        currentY += speedY;
        
        // Rebondir sur les bords
        if (currentX <= 0 || currentX >= gameArea.offsetWidth - 40) {
            speedX *= -1;
            heart.dataset.speedX = speedX;
        }
        if (currentY <= 0 || currentY >= gameArea.offsetHeight - 40) {
            speedY *= -1;
            heart.dataset.speedY = speedY;
        }
        
        // Appliquer les nouvelles positions
        heart.style.left = currentX + 'px';
        heart.style.top = currentY + 'px';
    });
    
    // Continuer l'animation
    requestAnimationFrame(animateHearts);
}

function collectHeart(heart) {
    if (!heart.classList.contains('collected')) {
        heart.classList.add('collected');
        heart.style.opacity = '0.5';
        heart.style.pointerEvents = 'none';
        heartsFound++;
        updateGameInfo();
        
        if (heartsFound === 5) {
            clearInterval(gameTimer);
            showVictory();
        }
    }
}

function updateGameInfo() {
    document.getElementById('hearts-found').textContent = `Cœurs trouvés : ${heartsFound}/5`;
    document.getElementById('timer').textContent = `${timeLeft}s`;
}

function startTimer() {
    gameTimer = setInterval(() => {
        timeLeft--;
        updateGameInfo();
        
        if (timeLeft <= 0) {
            clearInterval(gameTimer);
            showPage('fail-page');
        }
    }, 1000);
}

// Fonction de victoire
function showVictory() {
    showPage('final-page');
    createConfetti();
}

function createConfetti() {
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.animationDelay = Math.random() * 3 + 's';
        document.body.appendChild(confetti);
        
        setTimeout(() => {
            confetti.remove();
        }, 3000);
    }
}

function restartGame() {
    showPage('intro-page');
    document.querySelectorAll('.confetti').forEach(confetti => confetti.remove());
} 