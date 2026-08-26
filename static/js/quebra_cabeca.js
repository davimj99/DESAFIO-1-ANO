const puzzle = document.getElementById("puzzle");
const startButton = document.getElementById("startButton");

const timerElement = document.getElementById("timer");
const scoreElement = document.getElementById("score");

const resultModal = document.getElementById("resultModal");
const finalTime = document.getElementById("finalTime");
const finalScore = document.getElementById("finalScore");

const restartButton = document.getElementById("restartButton");

const TOTAL_PIECES = 9;

let pieces = [];
let draggedPiece = null;

let seconds = 0;
let timerInterval = null;

let gameStarted = false;


// =====================================
// CRIAR QUEBRA-CABEÇA
// =====================================

function createPuzzle() {

    puzzle.innerHTML = "";

    pieces = [];

    for (let i = 0; i < TOTAL_PIECES; i++) {

        const piece = document.createElement("div");

        piece.classList.add("puzzle-piece");

        piece.dataset.correctPosition = i;

        const row = Math.floor(i / 3);
        const column = i % 3;

        piece.style.backgroundImage =
            "url('/static/images/pascoa_dudu.jpeg')";

        piece.style.backgroundSize = "300% 300%";

        piece.style.backgroundPosition =
            `${column * 50}% ${row * 50}%`;

        // Desktop
        piece.draggable = true;

        piece.addEventListener("dragstart", () => {

            if (!gameStarted) return;

            draggedPiece = piece;

            piece.classList.add("dragging");

        });

        piece.addEventListener("dragend", () => {

            piece.classList.remove("dragging");

        });

        piece.addEventListener("dragover", (event) => {

            event.preventDefault();

        });

        piece.addEventListener("drop", (event) => {

            event.preventDefault();

            if (!gameStarted) return;

            const targetPiece = piece;

            if (
                draggedPiece &&
                draggedPiece !== targetPiece
            ) {

                swapPieces(
                    draggedPiece,
                    targetPiece
                );

                checkPuzzle();

            }

        });


        // Celular
        piece.addEventListener(
            "touchstart",
            handleTouchStart,
            { passive: true }
        );

        piece.addEventListener(
            "touchmove",
            handleTouchMove,
            { passive: false }
        );

        piece.addEventListener(
            "touchend",
            handleTouchEnd
        );


        pieces.push(piece);

    }

    shufflePieces();

    renderPuzzle();
}


// =====================================
// EMBARALHAR
// =====================================

function shufflePieces() {

    do {

        pieces.sort(() => Math.random() - 0.5);

    } while (isPuzzleSolved());

}


// =====================================
// RENDERIZAR
// =====================================

function renderPuzzle() {

    puzzle.innerHTML = "";

    pieces.forEach(piece => {

        puzzle.appendChild(piece);

    });

}


// =====================================
// TROCAR PEÇAS
// =====================================

function swapPieces(pieceA, pieceB) {

    const indexA = pieces.indexOf(pieceA);
    const indexB = pieces.indexOf(pieceB);

    if (indexA === -1 || indexB === -1) {
        return;
    }

    [
        pieces[indexA],
        pieces[indexB]
    ] = [
        pieces[indexB],
        pieces[indexA]
    ];

    renderPuzzle();

}


// =====================================
// TOUCH - CELULAR
// =====================================

let touchStartX = 0;
let touchStartY = 0;

let touchedPiece = null;


function handleTouchStart(event) {

    if (!gameStarted) return;

    touchedPiece = this;

    const touch = event.touches[0];

    touchStartX = touch.clientX;
    touchStartY = touch.clientY;

    this.classList.add("dragging");

}


function handleTouchMove(event) {

    if (!gameStarted || !touchedPiece) {
        return;
    }

    event.preventDefault();

}


function handleTouchEnd(event) {

    if (!gameStarted || !touchedPiece) {
        return;
    }

    const touch = event.changedTouches[0];

    const element = document.elementFromPoint(
        touch.clientX,
        touch.clientY
    );

    const targetPiece =
        element?.closest(".puzzle-piece");

    touchedPiece.classList.remove("dragging");

    if (
        targetPiece &&
        targetPiece !== touchedPiece
    ) {

        swapPieces(
            touchedPiece,
            targetPiece
        );

        checkPuzzle();

    }

    touchedPiece = null;

}


// =====================================
// VERIFICAR
// =====================================

function isPuzzleSolved() {

    return pieces.every(
        (piece, index) =>
            Number(piece.dataset.correctPosition) === index
    );

}


function checkPuzzle() {

    if (isPuzzleSolved()) {

        finishGame();

    }

}


// =====================================
// CRONÔMETRO
// =====================================

function startTimer() {

    clearInterval(timerInterval);

    seconds = 0;

    updateTimer();

    timerInterval = setInterval(() => {

        seconds++;

        updateTimer();

        updateScore();

    }, 1000);

}


function updateTimer() {

    const minutes =
        Math.floor(seconds / 60)
        .toString()
        .padStart(2, "0");

    const secs =
        (seconds % 60)
        .toString()
        .padStart(2, "0");

    timerElement.textContent =
        `${minutes}:${secs}`;

}


// =====================================
// PONTUAÇÃO
// =====================================

function calculateScore() {

    if (seconds <= 15) return 200;

    if (seconds <= 25) return 180;

    if (seconds <= 40) return 160;

    if (seconds <= 60) return 140;

    if (seconds <= 90) return 120;

    if (seconds <= 120) return 100;

    return 80;

}


function updateScore() {

    scoreElement.textContent =
        calculateScore();

}


// =====================================
// FINALIZAR
// =====================================
function finishGame() {

    clearInterval(timerInterval);

    gameStarted = false;

    const score = calculateScore();

    finalTime.textContent =
        timerElement.textContent;

    finalScore.textContent =
        score;

    document.getElementById(
        "pontosQuebraCabeca"
    ).value = score;

    resultModal.classList.add("active");
}


// =====================================
// COMEÇAR
// =====================================

startButton.addEventListener("click", () => {

    gameStarted = true;

    startButton.style.display = "none";

    createPuzzle();

    startTimer();

    updateScore();

});


// =====================================
// REINICIAR
// =====================================

restartButton.addEventListener("click", () => {

    resultModal.classList.remove("active");

    createPuzzle();

    gameStarted = true;

    startTimer();

    updateScore();

});