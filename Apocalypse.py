# version: 1.0.2
# language: русский


import sys
from win32api import GetSystemMetrics
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QInputDialog, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from MainWindowForm import Ui_MainWindowForm
from SettingsForm import Ui_FormSettings
from random import randint, choice


class GameExample(QMainWindow, Ui_MainWindowForm):
    '''
    Главный класс и окно игры
    '''

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''Инициализация игры'''

        # Инициализация оформления меню
        self.setupUi(self)

        # Определение допустимых размеров окна в переменную free_resolutions
        resolutions = ['1920x1080', '1680x900', '1280x720', '960x540', '800x600']
        free_resolutions = []
        for resolution in resolutions:
            size = [int(elem) for elem in resolution.split('x')]
            if size[0] <= GetSystemMetrics(0) and size[1] <= GetSystemMetrics(1):
                free_resolutions.append(resolution)

        # Установка первоночального размера окна игры
        size, okBtnPressed = QInputDialog.getItem(self, "Настройки",
                                                  "Выберите размер экрана игры",
                                                  free_resolutions,
                                                  0, False)
        if okBtnPressed:  # Если было нажатие, то установка выбранного размера окна
            size = [int(elem) for elem in size.split('x')]
        else:  # Иначе установка максимального размера экрана
            size = [GetSystemMetrics(0), GetSystemMetrics(1)]
        self.setFixedSize(*size)

        self.move(0, 0)  # Перемещение окна в левый верний угол

        self.game_activity = False  # Активность игры
        self.pos_objects = []  # Все позиции объектов
        self.activity_bonuses = {}  # Данные об активных бонусах

        # Инициализация данных поля игры
        self.indent_x, self.indent_y = 250, 20  # Отступ
        self.step = 60  # Размер стороны клетки
        self.n_x = self.NX_MAX = ((size[0] - self.indent_x) //
                                  self.step)  # Кол-во клеток по X
        self.n_y = self.NY_MAX = ((size[1] - self.indent_y) //
                                  self.step)  # Кол-во клеток по Y

        # Инициализация фона игрового поля
        self.label_background = QLabel(self)
        self.label_background.move(self.indent_x, self.indent_y)

        # Загрузка резервных виджетов
        self.reserve_labels = [QLabel(self) for _ in range(self.NX_MAX * self.NY_MAX)]

        # Инициализация переменных игрока и клетки выхода
        self.player = None  # Игрок
        self.exit = None  # Выход

        # Инициализация переменных данных о врагах
        self.type_enemies = {}  # Установленные виды врагов
        self.enemies = []  # Враги

        # Инициализация данных о опасных клетках
        self.type_dangerous_cells = {}  # Установленные виды опасных клеток
        self.dangerous_cells = []  # "Опасные клетки"

        # Инициализация данных о бонусах игры
        self.type_bonuses = {EnergyBomb: 0.05}  # Установленные виды бонусов
        self.bonuses = []  # Бонусы

        # Инициализация данных других объектов
        self.other_game_objects = []

        # Инициализация окна настроек
        self.window_settings = SettingsGameWindow(self)

        # Подключение кнопок к функциям
        self.btn_start_game.clicked.connect(self.prepare_and_start)  # Старт игры
        self.btn_settings.clicked.connect(self.window_settings.show)  # Настройки
        self.btn_guide.clicked.connect(self.print_guide)  # Правила
        self.btn_info.clicked.connect(self.print_info)  # О программе
        self.btn_close.clicked.connect(self.close)  # Выйти

        self.show()  # Показ окна

    def keyPressEvent(self, event):
        '''Считывание нажатий клавишь и вызов движений у врага и игрока'''

        if event.key() == Qt.Key_Escape:
            # Если была нажата кнопка Esc, то игра закрывается
            return self.close()
        elif event.key() == Qt.Key_N:
            # Если была нажата кнопка N, то игра перезагружается
            return self.prepare_and_start()
        elif not self.game_activity:
            return  # Если игра не активна, то дальше ничего не делать
        elif event.key() == Qt.Key_W:
            # Если была нажата кнопка W, то игрок перемещается вверх
            self.move_wrap(self.player, (0, -self.step))
        elif event.key() == Qt.Key_S:
            # Если была нажата кнопка W, то игрок перемещается вверх
            self.move_wrap(self.player, (0, self.step))
        elif event.key() == Qt.Key_A:
            # Если была нажата кнопка W, то игрок перемещается вверх
            self.move_wrap(self.player, (-self.step, 0))
        elif event.key() == Qt.Key_D:
            # Если была нажата кнопка W, то игрок перемещается вверх
            self.move_wrap(self.player, (self.step, 0))
        elif event.key() == Qt.Key_V:
            # Если была нажата кнопка W, то игрок перемещается вверх
            self.move_wrap(self.player, (0, 0))
        else:
            return  # Иначе дальше ничего не делать
        self.check_move()  # Проверка событий
        if not self.game_activity:
            return  # Если игра не активна, то ничего дальше не делать
        if self.activity_bonuses.get('EnergyBomb', 0) > 0:
            # Если активен бонус 'EnergyBomb', то уменьшить его время действия
            self.activity_bonuses['EnergyBomb'] -= 1
        else:
            # Иначе вызвать ход врагов
            for enemy in self.enemies:
                direction = enemy.get_direction_move()  # Получение направления
                self.move_wrap(enemy, direction)  # Вызов перемещения
        self.check_move()  # Проверка событий

    def prepare_and_start(self):
        '''Старт и перезагруска игры'''

        # Очистка данных объектов игры
        self.clear_objects()

        # Запуск генерации объектов
        self.generation_objects()

        # Обновление текущих бонусов
        self.label_info.setText('>>>')

        # Запуск игры
        self.game_activity = True

    def clear_objects(self):
        '''Очистка данных объектов игры'''

        # Очистка поля игры
        self.label_background.clear()

        # Очистка активных бонусов
        self.activity_bonuses.clear()

        # Удаление игрока
        if self.player is not None:
            self.player.remove()
            self.player = None

        # Удаление выхода
        if self.exit is not None:
            self.exit.remove()
            self.exit = None

        # Удаление остальных объектов
        for listen_obj in [self.enemies, self.dangerous_cells, self.bonuses, self.other_game_objects]:
            for obj in listen_obj:
                obj.remove()
            listen_obj.clear()

        self.reserve_labels = sorted(self.reserve_labels, key=lambda x: -id(x))
        # Обновление данных позиций объектов
        self.up_data_pos()

    def generation_objects(self):
        '''Генерация объектов игры'''

        self.player = MainHero(self)  # Генерация игрока
        self.exit = Exit(self)  # Генерация выхода

        for enemy, k in self.type_enemies.items():  # Генерация врагов
            for _ in range(int(self.n_x * self.n_y * k)):
                self.enemies.append(enemy(self))

        for cell, k in self.type_dangerous_cells.items():  # Генерация опасных клеток
            for _ in range(int(self.n_x * self.n_y * k)):
                self.dangerous_cells.append(cell(self))

        for bonus, k in self.type_bonuses.items():  # Генерация бонусов
            for _ in range(int(self.n_x * self.n_y * k)):
                self.bonuses.append(bonus(self))

        # Генерация фона
        self.label_background.setPixmap(self.load_pic('background.png',
                                                      self.step * self.n_x,
                                                      self.step * self.n_y))
        self.label_background.resize(self.step * self.n_x, self.step * self.n_y)

    def up_data_pos(self):
        '''Обновление данных позиций объектов игры'''
        # Очистка старых позиций
        self.pos_objects.clear()
        # Добавление новых позиций
        objects = ([self.player, self.exit] + self.enemies +
                   self.dangerous_cells + self.bonuses)
        for obj in objects:
            if obj is not None:
                self.pos_objects.append(obj.get_coords())

    def check_move(self):
        '''Проверка событий в игре'''

        if self.player.get_coords() == self.exit.get_coords():
            # Если координаты игрока и выхода равны, то *** Победа *** и
            # установка неактивности игры
            self.label_info.setText('*** ПОБЕДА!! ***')
            # Скрытие изображение игрока
            self.player.label.clear()
            self.game_activity = False

        if self.game_activity:
            # Если активна игра, то проверка на условия
            # поражения и получения бонуса
            for enemy in self.enemies:
                if self.player.get_coords() == enemy.get_coords():
                    # Если координаты игрока и врага равны,
                    # то *** Поражение *** и
                    # Установка неактивности игры
                    self.label_info.setText('*** ПОРАЖЕНИЕ!! ***')
                    self.game_activity = False
            for danger_cell in self.dangerous_cells:
                if self.player.get_coords() == danger_cell.get_coords():
                    self.label_info.setText('*** ПОРАЖЕНИЕ!! ***')
                    self.game_activity = False
            for bonus in self.bonuses:
                if self.player.get_coords() == bonus.get_coords() and not bonus.isact():
                    bonus.activate()

        info = '\n'.join(
            [f'{key}- {val} х.'
             for (key, val) in self.activity_bonuses.items()
             if val > 0])  # Получение инфор-ии об активных бонусах 

        if self.game_activity:
            info = self.get_info_act_bonuses()  # Получение информации об активных бонусах
            if info:
                self.label_info.setText('>>> Бонусы:\n' + info)
            else:
                self.label_info.setText('>>>')
        self.label_info.resize(self.label_info.sizeHint())

    def move_wrap(self, obj, move):
        """Вызов движения"""

        # Вызов движения obj
        pos = obj.get_coords()
        obj.move(pos[0] + move[0], pos[1] + move[1])

        # Если obj вышел за край карты по X, то перемещает его на другую сторону
        pos = obj.get_coords()
        if pos[0] < self.indent_x:
            obj.move(self.indent_x + self.step * (self.n_x - 1), pos[1])
        elif pos[0] > self.indent_x + self.step * (self.n_x - 1):
            obj.move(self.indent_x, pos[1])

        # Если obj вышел за край карты по Y, то перемещает его на другую сторону
        pos = obj.get_coords()
        if pos[1] < self.indent_y:
            obj.move(pos[0], self.indent_y + self.step * (self.n_y - 1))
        elif pos[1] > self.indent_y + self.step * (self.n_y - 1):
            obj.move(pos[0], self.indent_y)

        self.up_data_pos()

    def load_pic(self, name, scale_x=None, scale_y=None):
        '''Возвращает картинку с именем name отмасштабированную по
        scale_x и scale_y в виде объекта QPixmap'''

        scale_x = scale_x if scale_x is not None else self.step
        scale_y = scale_y if scale_y is not None else self.step
        return QPixmap(f'images/{name}').scaled(scale_x, scale_y)

    def get_pos_objects(self):
        '''Получение данных о позициях объектов'''

        return self.pos_objects

    def print_info(self):
        '''Вывод информации о программе'''
        with open('About the program.txt') as info:
            data = info.read()
            self.label_info.setText(data)
            self.label_info.resize(self.label_info.sizeHint())

    def print_guide(self):
        '''Вывод информации о правилах игры'''
        with open('guide_game.txt') as rules:
            data = rules.read()
            self.label_info.setText(data)
            self.label_info.resize(self.label_info.sizeHint())

    def get_info_act_bonuses(self):
        '''Получение информации об активных бонусах'''

        return '\n'.join([f'{key}- {val} х.'
                          for (key, val) in self.activity_bonuses.items() if val > 0])

    def is_cell_free(self, *pos):
        '''Возвращает True если на клетке нет объектов (игнорирует MainHero)
           и клетка не за краем карты'''

        # Враги не умеют выходить за край карты
        if not self.indent_x <= pos[0] < self.indent_x + self.n_x * self.step:
            return False
        if not self.indent_y <= pos[1] < self.indent_y + self.n_y * self.step:
            return False

        # Враги не могут вступать на те клетки
        # где есть другой объект (кроме MainHero и Bonus)
        for obj in [self.exit] + self.enemies + self.dangerous_cells + self.bonuses:
            if pos == obj.get_coords():
                return False

        return True


class SettingsGameWindow(QWidget, Ui_FormSettings):
    '''
    Окно настроек игры
    '''

    def __init__(self, game):
        super().__init__()
        self.initUI(game)

    def initUI(self, game):
        '''Инициализация настроек игры'''
        # Инициализация оформления и меню
        self.setupUi(self)
        # Связка настроек с игрой
        self.game = game
        # Установка максимального и текущего размера карты
        self.editer_size_x.setMaximum(self.game.NX_MAX)
        self.editer_size_x.setValue(self.game.n_x)
        self.editer_size_y.setMaximum(self.game.NY_MAX)
        self.editer_size_y.setValue(self.game.n_y)
        # Связка кнопок с функциями
        self.btn_ok.clicked.connect(self.save)  # ОК
        # Первичное применение настроек
        self.save()

    def save(self):
        '''Сохранение настроек игры'''
        self.game.n_x = self.editer_size_x.value()  # Размер карты по X
        self.game.n_y = self.editer_size_y.value()  # Размер карты по Y
        # Очистка старых устоновок о типах врагов и опасных клеток
        self.game.type_enemies.clear()
        self.game.type_dangerous_cells.clear()
        if self.checkBoxStraightForwardEnemy.isChecked():
            self.game.type_enemies[StraightForwardEnemy] = float(
                '0.' + str(self.countStraightForwardEnemies.value()).rjust(2, '0'))
        if self.checkBoxStupidEnemy.isChecked():
            self.game.type_enemies[StupidEnemy] = float('0.' + str(self.countStupidEnemies.value()
                                                                   ).rjust(2, '0'))
        if self.checkBoxSmartEnemy.isChecked():
            self.game.type_enemies[SmartEnemy] = float('0.' + str(self.countSmartEnemies.value()
                                                                  ).rjust(2, '0'))
        if self.checkBoxSecretiveEnemy.isChecked():
            self.game.type_enemies[SecretiveEnemy] = float('0.' + str(self.countSecretiveEnemies.value()
                                                                      ).rjust(2, '0'))
        if self.checkBoxTraps.isChecked():
            self.game.type_dangerous_cells[Trap] = float('0.' + str(self.countTraps.value()
                                                                    ).rjust(2, '0'))
        self.hide()


class BaseObject:
    '''
    Базовый класс всех игровых объектов
    '''

    def __init__(self, game):
        '''Инициализация объекта'''

        # Связка игры с объектом
        self.game = game
        # Взятие из резерва игры объект QLabel
        self.label = self.game.reserve_labels.pop()
        self.label.resize(self.game.step, self.game.step)  # Изменение размера игры
        while True:  # Генерация случайной не накладывающаяся позиции объекта
            pos = (randint(0, self.game.n_x - 1) * self.game.step + self.game.indent_x,
                   randint(0, self.game.n_y - 1) * self.game.step + self.game.indent_y)
            if pos not in self.game.get_pos_objects():
                break
        # Перемещение объекта на эту позицию
        self.move(*pos)
        # Добаление этой позиции в список всех позиций игры
        self.game.pos_objects.append(pos)
        # Установка имени объекта в label (для отладки)
        self.label.setText(str(randint(0, 1000)))

        # Далее в каждом объекте у наследованного от этого
        # устанавливается картинка
        # self.label.setPixmap(self.game.load_pic(<Имя картинки>))

    def __repr__(self):
        return 'BaseObject()'

    def get_coords(self):
        '''Получить координаты объекта'''
        if self.label is None:
            return None, None
        return self.label.pos().x(), self.label.pos().y()

    def move(self, x, y):
        '''Вызов перемещения'''

        self.label.move(x, y)

    def untie_label(self):
        '''Отвязка labela'''

    def remove(self):
        '''Удаление объекта'''
        # Отвязка Label-а
        self.untie_label()
        # Очистка label-a объекта
        self.label.clear()
        # Передвижение label-а объекта
        self.label.move(0, 0)
        # Возврат label-а в резерв игры
        self.game.reserve_labels.append(self.label)
        # Отвязка label от объекта
        self.label = None
        # Удаление объекта
        del self


class MainHero(BaseObject):
    '''
    "Главный герой" - герой, за которого будет
    упрявлять человек во время игры
    '''

    def __init__(self, game):
        super().__init__(game)
        self.label.setPixmap(self.game.load_pic('MainHero.png'))

    def __repr__(self):
        return 'MainHero()'


class Exit(BaseObject):
    '''
    "Выход" - клетка, которая завершает игру победой
    при попадании игрока на неё
    '''

    def __init__(self, game):
        super().__init__(game)
        self.label.setPixmap(self.game.load_pic('Exit.png'))

    def __repr__(self):
        return 'Exit()'


class Trap(BaseObject):
    '''
    "Ловушки" - опасные клетки, которые убивают игрока
    при попадании на них
    '''

    def __init__(self, game):
        super().__init__(game)
        self.label.setPixmap(self.game.load_pic('Trap.png'))

    def __repr__(self):
        return 'Trap()'


class Enemy(BaseObject):
    '''
     Класс "врагов" игры
    '''

    def __init__(self, game):
        super().__init__(game)

    def __repr__(self):
        return 'Enemy()'

    def get_direction_move(self):
        '''Получить место перемещения'''
        # Возвращает изменения координат
        # для дальнейшего перемещения
        return 0, 0


class StraightForwardEnemy(Enemy):
    '''
    "Прямоходящий враг" - враг, за которого будет
    управлять ИИ во время игры. Ходит в одну сторону (или стоит на месте)
    пока не наткнётся на препятствие. После меняет направление
    (или останавливается) и повторяет всё заново.
    '''

    def __init__(self, game):
        super().__init__(game)
        self.label.setPixmap(self.game.load_pic('StraightForwardEnemy.png'))
        self.dir = (choice([-self.game.step, 0, self.game.step]),
                    choice([-self.game.step, 0, self.game.step]))

    def __repr__(self):
        return 'StraightForwardEnemy()'

    def get_direction_move(self):
        pos_e = self.get_coords()
        if self.game.is_cell_free(pos_e[0] + self.dir[0], pos_e[1] + self.dir[1]):
            return self.dir[0], self.dir[1]
        self.dir = (choice([-self.game.step, 0, self.game.step]),
                    choice([-self.game.step, 0, self.game.step]))
        return 0, 0


class StupidEnemy(Enemy):
    '''
    "Глупый враг" - враг, который будет управляться ИИ
    во время игры. Ходит случайным образом.
    '''

    def __init__(self, game):
        super().__init__(game)
        self.label.setPixmap(self.game.load_pic('StupidEnemy.png'))

    def __repr__(self):
        return 'StupidEnemy()'

    def get_direction_move(self):
        pos = self.get_coords()
        move = (choice([-self.game.step, 0, self.game.step]),
                choice([-self.game.step, 0, self.game.step]))
        if self.game.is_cell_free(pos[0] + move[0], pos[1] + move[1]):
            return move
        return 0, 0


class SmartEnemy(Enemy):
    '''
    "Умный враг" - враг, который будет управляться ИИ
    во время игры. Ходит всегда на главного героя.
    '''

    def __init__(self, game):
        super().__init__(game)
        self.label.setPixmap(self.game.load_pic('SmartEnemy.png'))

    def __repr__(self):
        return 'SmartEnemy()'

    def get_direction_move(self):
        pos_p = self.game.player.get_coords()
        pos_e = self.get_coords()

        if pos_p[0] < pos_e[0] and pos_p[1] < pos_e[1]:
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] - self.game.step):
                return -self.game.step, -self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1]):
                return -self.game.step, 0
            if self.game.is_cell_free(pos_e[0], pos_e[1] - self.game.step):
                return 0, -self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] + self.game.step):
                return -self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] - self.game.step):
                return self.game.step, -self.game.step
        if pos_p[0] > pos_e[0] and pos_p[1] > pos_e[1]:
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] + self.game.step):
                return self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1]):
                return self.game.step, 0
            if self.game.is_cell_free(pos_e[0], pos_e[1] + self.game.step):
                return 0, self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] + self.game.step):
                return -self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] - self.game.step):
                return self.game.step, -self.game.step
        if pos_p[1] < pos_e[1] and pos_p[0] > pos_e[0]:
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] - self.game.step):
                return self.game.step, -self.game.step
            if self.game.is_cell_free(pos_e[0], pos_e[1] - self.game.step):
                return 0, -self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1]):
                return self.game.step, 0
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] + self.game.step):
                return self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] - self.game.step):
                return -self.game.step, -self.game.step
        if pos_p[1] > pos_e[1] and pos_p[0] < pos_e[0]:
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] + self.game.step):
                return -self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0], pos_e[1] + self.game.step):
                return 0, self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1]):
                return -self.game.step, 0
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] + self.game.step):
                return self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] - self.game.step):
                return -self.game.step, -self.game.step
        if pos_p[0] < pos_e[0]:
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1]):
                return -self.game.step, 0
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] + self.game.step):
                return -self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] - self.game.step):
                return -self.game.step, -self.game.step
            if self.game.is_cell_free(pos_e[0], pos_e[1] + self.game.step):
                return 0, self.game.step
            if self.game.is_cell_free(pos_e[0], pos_e[1] - self.game.step):
                return 0, -self.game.step
        if pos_p[0] > pos_e[0]:
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1]):
                return self.game.step, 0
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] + self.game.step):
                return self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] - self.game.step):
                return self.game.step, -self.game.step
            if self.game.is_cell_free(pos_e[0], pos_e[1] + self.game.step):
                return 0, self.game.step
            if self.game.is_cell_free(pos_e[0], pos_e[1] - self.game.step):
                return 0, -self.game.step
        if pos_p[1] < pos_e[1]:
            if self.game.is_cell_free(pos_e[0], pos_e[1] - self.game.step):
                return 0, -self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] - self.game.step):
                return self.game.step, -self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] - self.game.step):
                return -self.game.step, -self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1]):
                return self.game.step, 0
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1]):
                return -self.game.step, 0
        if pos_p[1] > pos_e[1]:
            if self.game.is_cell_free(pos_e[0], pos_e[1] + self.game.step):
                return 0, self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1] + self.game.step):
                return self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1] + self.game.step):
                return -self.game.step, self.game.step
            if self.game.is_cell_free(pos_e[0] + self.game.step, pos_e[1]):
                return self.game.step, 0
            if self.game.is_cell_free(pos_e[0] - self.game.step, pos_e[1]):
                return -self.game.step, 0
        return 0, 0


class SecretiveEnemy(Enemy):
    '''
    "Скрытный враг" - враг, который будет управляться ИИ
    во время игры. Стоит всю игру на месте не двигаясь,
    но когда главный герой подходит к нему очень близко
    атакует.
    '''

    def __init__(self, game):
        super().__init__(game)
        self.label.setPixmap(self.game.load_pic('SecretiveEnemy2.png'))

    def __repr__(self):
        return 'SecretiveEnemy()'

    def get_direction_move(self):
        pos_p = self.game.player.get_coords()
        pos_e = self.get_coords()
        if (abs(pos_p[0] - pos_e[0]) <= self.game.step and
                abs(pos_p[1] - pos_e[1]) <= self.game.step):
            if self.game.is_cell_free(pos_p[0], pos_p[1]):
                self.label.setPixmap(self.game.load_pic('SecretiveEnemy.png'))
                return pos_p[0] - pos_e[0], pos_p[1] - pos_e[1]
        return 0, 0


class Bonus(BaseObject):
    '''
    Класс "бонусов" игры
    '''

    def __init__(self, game):
        super().__init__(game)
        self.name = 'Bonus'  # Установка имени бонуса
        self.label.setText('B' + str(randint(0, 100)))
        self.act = False

    def __repr__(self):
        return 'Bonus()'

    def isact(self):
        '''Возвращает True если бонус был активирован'''
        return self.act

    def activate(self):
        '''Активирует бонус и делает его недействительным'''
        # Складывает действие бонуса если
        # уже раннее такой бонус активировался
        bonus_old = self.game.activity_bonuses.get(self.name, 0)
        self.game.activity_bonuses[self.name] = bonus_old + randint(2, 6)
        # Устанавливает бонус активным
        self.act = True
        # Очистка и сдвиг label-а в левый верхний угол
        self.label.clear()
        self.label.move(0, 0)


class EnergyBomb(Bonus):
    '''
    "Энергетическая бомба" - бонус, который останавливает
    врагов на случайное кол-во ходов
    '''

    def __init__(self, game):
        super().__init__(game)
        self.name = 'EnergyBomb'
        self.label.setText('[B-1]')
        self.label.setPixmap(self.game.load_pic('EnergyBomb.png'))

    def __repr__(self):
        return 'EnergyBomb()'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameExample()
    sys.exit(app.exec_())
