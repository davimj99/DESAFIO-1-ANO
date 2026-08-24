const image = document.getElementById("baby-image");

const timerElement =
    document.getElementById("timer");

const options =
    document.querySelectorAll(".option");

const result =
    document.getElementById("result");

const resultIcon =
    document.getElementById("result-icon");

const resultTitle =
    document.getElementById("result-title");

const resultMessage =
    document.getElementById("result-message");

const nextButton =
    document.getElementById("next-button");


let time = 10;

let answered = false;


/*
    CONTADOR
*/

const countdown = setInterval(() => {

    if (answered) {
        return;
    }


    time--;


    timerElement.textContent =
        time;


    if (time <= 0) {

        clearInterval(countdown);

        revealImage();

        finishGame(false);

    }

}, 1000);


/*
    DEIXA A FOTO NÍTIDA
*/

function revealImage() {

    image.classList.add("reveal");

}


/*
    CLIQUE NAS RESPOSTAS
*/

options.forEach(option => {

    option.addEventListener(
        "click",
        () => {

            if (answered) {
                return;
            }


            answered = true;


            clearInterval(countdown);


            revealImage();


            const answer =
                option.dataset.answer;


            if (answer === "correto") {

                option.classList.add(
                    "correct"
                );

                finishGame(true);

            } else {

                option.classList.add(
                    "wrong"
                );

                /*
                    Mostra a resposta correta
                */

                options.forEach(item => {

                    if (
                        item.dataset.answer ===
                        "correto"
                    ) {

                        item.classList.add(
                            "correct"
                        );

                    }

                });


                finishGame(false);

            }

        }
    );

});


/*
    RESULTADO
*/

function finishGame(correct) {

    result.classList.remove(
        "hidden"
    );


    if (correct) {

        resultIcon.textContent =
            "🎉";

        resultTitle.textContent =
            "ACERTOU!";

        resultMessage.textContent =
            "Você conhece muito bem o aniversariante! +100 pontos";

    } else {

        resultIcon.textContent =
            "😂";

        resultTitle.textContent =
            "QUASE!";

        resultMessage.textContent =
            "Não foi dessa vez! Mas ainda dá para ganhar pontos.";

    }


    /*
        Desabilita os botões
    */

    options.forEach(option => {

        option.disabled = true;

    });

}


/*
    PRÓXIMO JOGO
*/

nextButton.addEventListener(
    "click",
    () => {

        window.location.href =
            "/quiz/";

    }
);