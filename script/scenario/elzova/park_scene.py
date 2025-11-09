from script.scenario.characters import CHARACTERS

park_scene = {
    "park": {
        
        "dialogue": [
            {"bg": "school.png",
                "speaker": CHARACTERS["male_speak"],
                "icon": "красавица_стоит.png",
                "text": "Да, вопрос один: я как раз собирался перекусить. Может, присоединитесь? Обсудим интегралы на свежем воздухе? В парке, например..."
            },
            {
                "speaker": CHARACTERS["system"],
                "icon": "1.1.png",
                "text": "Преподаватель на секунду замерла, затем подняла на меня удивленный взгляд."
            },
            {
                "speaker": CHARACTERS["tamara_prepod"],
                "text": "В парк? Т/И, на улице уже вечер. Вы предлагаете мне есть сэндвичи на холодной скамейке под звездами?"
            },
            {
                "speaker": CHARACTERS["male_speak"],
                "text": "Ну, это... романтичнее! В смысле, атмосфернее для размышлений! И можно взять кофе с собой!"
            },
            {
                "speaker": CHARACTERS["tamara_prepod"],
                "icon": "1.1.png",
                "text": "Романтичнее... (вздыхает) Что ж, посмотрим на ваше понимание романтики. Ладно, ведите, звездный математик."
            },
            {
                "bg": "park.png",
                "sound":"park.mp3",
                "speaker": CHARACTERS["system"],
                "icon": "no icon",
                "text": "Мы шли до парка в немного неловком молчании, но в целом все было зашибись.",
                "icon": "park_icon.png"
            },
            {
                "bg": "park.png",
                "speaker": CHARACTERS["system"],
                "text": "Парк и правда был красивым. Мы нашли скамейку, купили кофе и булочки."
            },
            {
                "speaker": CHARACTERS["tamara_prepod"],
                "icon": "курточка.png",
                "text": "Ну что, ТИ, где же обещанная атмосфера для интегралов? Я жду."
            },
            {
                "speaker": CHARACTERS["male_speak"],
                "text": "Видите ту звезду? Она прямо над нами... Я бы назвал ее... интегралом вашей красоты, стремящимся к бесконечности!"
            },
            {
                "speaker": CHARACTERS["tamara_prepod"],
                "icon": "красопетка_1.png",
                "text": "Боже мой... (качает головой, но улыбается) Вы абсолютно безнадежны. И знаете, в этом есть какая-то дурацкая прелесть."
            },
            {
                "speaker": CHARACTERS["male"],
                "text": "Она улыбается! Это работает! Надо действовать дальше!"
            },
            {
                "speaker": CHARACTERS["male_speak"],
                "text": "Может, проводить Вас до дома? А то уже темнеет..."
            },
            {
                "speaker": CHARACTERS["tamara_prepod"],
                "icon": "курточка.png",
                "text": "Наконец-то здравая мысль. Да, проводи. Но без глупостей про звезды и интегралы по дороге."
            }
        ],
        "choices": [
            {
                "text": "Идти к ее дому", 
                "next": "dom_Elcovoi"
            }
        ]
    }
}