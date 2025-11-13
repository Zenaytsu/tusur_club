from script.scenario.characters import CHARACTERS

para = {
    "para_begin": {
        
        "dialogue": [
            {
                "speaker": CHARACTERS["system"],
                "text": "Для переключения используйте ЛКМ",
            },
            {
                "speaker": CHARACTERS["system"],
                "text": "Для выхода из игры ESC",
            },
            {   "bg": "общага.png",
                "song":"фон.mp3",
                "speaker": CHARACTERS["system"],
                "text": "Обычный день студенческого городка Томска на Лыткина"
            },
            {   "bg": "общага.png",
                "speaker": CHARACTERS["system"],
                "text": "Студенты спешат на пары, а я неспешно двигаюсь в сторону богтейшего предприятия студгородка"
            },
            {   "bg": "безумно_входо.png",
                "speaker": CHARACTERS["system"],
                "text": "Безумно-шаурма"
            },
            {   "speaker": CHARACTERS["system"],
                "text": "Самое лучшее место, которое еще и работает круглосуточно"
            },
            {   "bg": "безумно_заход.png",
                "speaker": CHARACTERS["system"],
                "text": "Аккуратно спускаясь по лестнице, я захожу в темное подвальное помещение"
            },
            {   "bg": "Безумно_внутри.png",
                "song":"фон.mp3",
                "speaker": CHARACTERS["system"], 
                "text": "Здесь всегда многолюдно и играют молодежные песни 10х годов"
            },
            {   "speaker": CHARACTERS["system"],
                "text": "Я подхожу к кассе и начинаю выбирать шавуху"
            },
        ],
        "choices": [ 
            {
                "text": "Кавказкая", 
                "next": "uvazhenie"
            },
            {
                "text": "Арабская", 
                "next": "prodolshit"
            },
            {
                "text": "Вегетарианская", 
                "next": "izvrat"
            }
        ]
    },

    "izvrat": {
        "dialogue": [
            {
                "speaker": CHARACTERS["system"],
                "text": "Ебать ты извращенец",
                "effect":"изврат.mp3",
                "sound":"no_sound"
            }
        ]
        #Здесь конец
    },

    "uvazhenie": {
        "dialogue": [
            {
                "speaker": CHARACTERS["system"],
                "text": "Ебать ты извращенец",
                "effect":"изврат.mp3",
                "sound":"no_sound"
            }
        ]
    },

    "prodolshit": {
        "dialogue": [
            {
                "speaker": CHARACTERS["system"],
                "text": "Ебать ты извращенец",
                "effect":"изврат.mp3",
                "sound":"no_sound"
            }
        ]
    },
}