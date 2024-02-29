from aiogram.fsm.state import State, StatesGroup


class ChoicePlace(StatesGroup):
    """
    Класс, наследуемый от StatesGroup, для группы состояний FSM бота.
    Состояние ожидания ввода населенного пункта
    """
    any_location: State = State()


class ChoiceUserPlace(StatesGroup):
    """
    Класс, наследуемый от StatesGroup, для группы состояний FSM бота.
    Состояние ожидания ввода населенного пункта, который пользователь
    устанавливает по-умолчанию
    """
    user_location: State = State()
