from telegram import ReplyKeyboardMarkup

from howru_helpers.Flag import flag


def get_custom_keyboard(values, max_column=2):
    # row_size = len(options) / max_column
    schema = [[value] for value in values]
    return ReplyKeyboardMarkup(schema)


gender_keyboard = {
    'ES': ReplyKeyboardMarkup([['Masculino', 'Femenino', 'Otro']]),
    'EN': ReplyKeyboardMarkup([['Male', 'Female', 'Other']])
}
language_keyboard = ReplyKeyboardMarkup([[flag('es'), flag('gb')]])
delete_user_keyboard = {
    'ES': ReplyKeyboardMarkup([
        ['Sí, eliminar mi usuario']
    ]
    ),
    'EN': ReplyKeyboardMarkup(
        [
            ['Yes, delete my user']
        ]
    ),
}
start_keyboard = ReplyKeyboardMarkup([['/start']])
config_keyboard = {
    'ES': ReplyKeyboardMarkup([
        ['Cambiar imagen de perfil', 'Cambiar nombre'],
        ["Cambiar género", 'Cambiar idioma'],
        ['Cambiar horario', "Ver mi perfil"],
        ["Borrar usuario️"]
    ]
    ),
    'EN': ReplyKeyboardMarkup(
        [
            ['Change profile picture', 'Change name'],
            ["Change gender", 'Change language'],
            ['Change schedule', "View my profile"],
            ["Remove user️"]
        ]
    ),
}
