from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / 'docs'

rcParams['font.family'] = 'DejaVu Sans'
rcParams['axes.unicode_minus'] = False


# ---------- Flowchart helpers ----------

def add_text(ax, x, y, text, *, fontsize=10, weight='normal', ha='center', va='center'):
    ax.text(x, y, text, fontsize=fontsize, weight=weight, ha=ha, va=va, color='#111111', wrap=True)


def draw_terminator(ax, x, y, w, h, text):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.01,rounding_size=0.08',
        linewidth=1.4,
        edgecolor='#2b2b2b',
        facecolor='#eef3f8',
    )
    ax.add_patch(patch)
    add_text(ax, x + w / 2, y + h / 2, text, fontsize=10.5, weight='bold')


def draw_process(ax, x, y, w, h, text):
    patch = Rectangle((x, y), w, h, linewidth=1.4, edgecolor='#2b2b2b', facecolor='white')
    ax.add_patch(patch)
    add_text(ax, x + w / 2, y + h / 2, text, fontsize=10)


def draw_data(ax, x, y, w, h, text):
    skew = w * 0.08
    patch = Polygon(
        [(x + skew, y), (x + w, y), (x + w - skew, y + h), (x, y + h)],
        closed=True,
        linewidth=1.4,
        edgecolor='#2b2b2b',
        facecolor='#fbfcfe',
    )
    ax.add_patch(patch)
    add_text(ax, x + w / 2, y + h / 2, text, fontsize=10)


def draw_decision(ax, x, y, w, h, text):
    patch = Polygon(
        [(x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y), (x, y + h / 2)],
        closed=True,
        linewidth=1.4,
        edgecolor='#2b2b2b',
        facecolor='white',
    )
    ax.add_patch(patch)
    add_text(ax, x + w / 2, y + h / 2, text, fontsize=9.6)


def draw_document(ax, x, y, w, h, text):
    xs = [x, x + w, x + w, x + w * 0.72, x + w * 0.45, x + w * 0.20, x]
    ys = [y + h, y + h, y + h * 0.15, y, y + h * 0.10, y, y + h * 0.15]
    patch = Polygon(list(zip(xs, ys, strict=False)), closed=True, linewidth=1.4, edgecolor='#2b2b2b', facecolor='white')
    ax.add_patch(patch)
    add_text(ax, x + w / 2, y + h * 0.60, text, fontsize=9.8)


def arrow(ax, x1, y1, x2, y2, label=None, label_dx=0, label_dy=0):
    ax.annotate(
        '',
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle='->', linewidth=1.3, color='#2b2b2b', shrinkA=2, shrinkB=2),
    )
    if label:
        mx = (x1 + x2) / 2 + label_dx
        my = (y1 + y2) / 2 + label_dy
        add_text(ax, mx, my, label, fontsize=9.3, weight='bold')


def elbow(ax, points, label=None, label_pos=None):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        style = dict(color='#2b2b2b', linewidth=1.3)
        if i == len(points) - 2:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', **style))
        else:
            ax.add_line(Line2D([x1, x2], [y1, y2], **style))
    if label and label_pos:
        add_text(ax, label_pos[0], label_pos[1], label, fontsize=9.3, weight='bold')


def generate_flowchart(output: Path) -> None:
    fig = plt.figure(figsize=(16.54, 11.69))  # A3 landscape
    ax = plt.axes([0.03, 0.04, 0.94, 0.92])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # frame and title block
    ax.add_patch(Rectangle((0.01, 0.01), 0.98, 0.98, fill=False, linewidth=1.2, edgecolor='#2b2b2b'))
    ax.add_patch(Rectangle((0.01, 0.92), 0.98, 0.07, fill=False, linewidth=1.0, edgecolor='#2b2b2b'))
    ax.add_line(Line2D([0.70, 0.70], [0.92, 0.99], color='#2b2b2b', linewidth=1.0))
    ax.add_line(Line2D([0.85, 0.85], [0.92, 0.99], color='#2b2b2b', linewidth=1.0))

    add_text(ax, 0.355, 0.965, 'БЛОК-СХЕМА АЛГОРИТМА РАБОТЫ ПРИЛОЖЕНИЯ «МАГАЗИН ОБУВИ»', fontsize=16, weight='bold')
    add_text(ax, 0.355, 0.936, 'Модуль 2. Разработка алгоритма и создание приложения. Оформлено по ГОСТ 19.701-90.', fontsize=10.5)
    add_text(ax, 0.775, 0.965, 'Документ', fontsize=9, weight='bold')
    add_text(ax, 0.775, 0.938, 'Блок-схема', fontsize=9)
    add_text(ax, 0.92, 0.965, 'Лист', fontsize=9, weight='bold')
    add_text(ax, 0.92, 0.938, '1 / 1', fontsize=9)

    # section labels
    for x, title in [(0.08, 'Инициализация'), (0.31, 'Авторизация и роль'), (0.56, 'Работа с товарами'), (0.83, 'Работа с заказами / завершение')]:
        ax.add_patch(Rectangle((x - 0.10, 0.865), 0.20, 0.032, facecolor='#eef3f8', edgecolor='#2b2b2b', linewidth=1.0))
        add_text(ax, x, 0.881, title, fontsize=9.8, weight='bold')

    # y levels
    y_top = 0.81
    gap = 0.085

    # Column 1
    draw_terminator(ax, 0.04, y_top, 0.12, 0.045, 'Начало')
    draw_process(ax, 0.025, y_top - gap, 0.15, 0.055, 'Запуск приложения\nmain.py')
    draw_process(ax, 0.02, y_top - 2 * gap, 0.16, 0.06, 'Инициализация ресурсов:\nиконка, логотип, настройки UI')
    draw_data(ax, 0.02, y_top - 3 * gap, 0.16, 0.06, 'Подключение к SQLite\nи чтение справочников')
    draw_decision(ax, 0.045, y_top - 4.22 * gap, 0.11, 0.075, 'Подключение\nуспешно?')
    draw_process(ax, 0.02, y_top - 5.28 * gap, 0.16, 0.06, 'Вывод сообщения об ошибке\nи запись в журнал')
    draw_terminator(ax, 0.04, y_top - 6.22 * gap, 0.12, 0.045, 'Завершение')

    arrow(ax, 0.10, y_top, 0.10, y_top - gap + 0.055)
    arrow(ax, 0.10, y_top - gap, 0.10, y_top - 2 * gap + 0.06)
    arrow(ax, 0.10, y_top - 2 * gap, 0.10, y_top - 3 * gap + 0.06)
    arrow(ax, 0.10, y_top - 3 * gap, 0.10, y_top - 4.22 * gap + 0.075)
    arrow(ax, 0.10, y_top - 4.22 * gap, 0.10, y_top - 5.28 * gap + 0.06, label='Нет', label_dx=-0.03)
    arrow(ax, 0.10, y_top - 5.28 * gap, 0.10, y_top - 6.22 * gap + 0.045)

    # Column 2
    draw_document(ax, 0.24, y_top - 0.01, 0.15, 0.055, 'Форма входа')
    draw_decision(ax, 0.255, y_top - gap, 0.12, 0.08, 'Вход как\nгость?')
    draw_process(ax, 0.225, y_top - 2 * gap, 0.18, 0.06, 'Открыть каталог товаров\nв режиме гостя')
    draw_process(ax, 0.225, y_top - 3 * gap, 0.18, 0.06, 'Проверка логина и пароля\nпо базе данных')
    draw_decision(ax, 0.255, y_top - 4.10 * gap, 0.12, 0.08, 'Авторизация\nуспешна?')
    draw_process(ax, 0.225, y_top - 5.22 * gap, 0.18, 0.06, 'Определение роли:\nклиент / менеджер / администратор')
    draw_process(ax, 0.225, y_top - 6.20 * gap, 0.18, 0.06, 'Открытие главного окна\nс правами роли')
    draw_process(ax, 0.225, y_top - 7.20 * gap, 0.18, 0.06, 'Сообщение: неверный логин\nили пароль')

    elbow(ax, [(0.155, y_top - 4.22 * gap + 0.04), (0.205, y_top - 4.22 * gap + 0.04), (0.205, y_top - gap + 0.04), (0.255, y_top - gap + 0.04)], label='Да', label_pos=(0.205, y_top - gap + 0.065))
    arrow(ax, 0.315, y_top - 0.01, 0.315, y_top - gap + 0.08)
    arrow(ax, 0.315, y_top - gap, 0.315, y_top - 2 * gap + 0.06, label='Да', label_dx=-0.045)
    arrow(ax, 0.315, y_top - 2 * gap, 0.315, y_top - 3 * gap + 0.06)
    arrow(ax, 0.315, y_top - 3 * gap, 0.315, y_top - 4.10 * gap + 0.08)
    arrow(ax, 0.315, y_top - 4.10 * gap, 0.315, y_top - 5.22 * gap + 0.06, label='Да', label_dx=-0.045)
    arrow(ax, 0.315, y_top - 5.22 * gap, 0.315, y_top - 6.20 * gap + 0.06)
    arrow(ax, 0.375, y_top - 4.10 * gap + 0.04, 0.405, y_top - 4.10 * gap + 0.04, label='Нет', label_dy=0.025)
    elbow(ax, [(0.405, y_top - 4.10 * gap + 0.04), (0.405, y_top - 7.20 * gap + 0.03), (0.405, y_top - 7.20 * gap + 0.03)],)
    arrow(ax, 0.315, y_top - 7.20 * gap + 0.06, 0.315, y_top - gap + 0.005)

    # Column 3
    draw_data(ax, 0.49, y_top - 0.01, 0.16, 0.055, 'Запрос списка товаров\nиз БД')
    draw_process(ax, 0.485, y_top - gap, 0.17, 0.06, 'Вывод каталога:\nфото, цена, скидка, остаток')
    draw_decision(ax, 0.515, y_top - 2.07 * gap, 0.11, 0.08, 'Роль =\nменеджер\nили админ?')
    draw_process(ax, 0.48, y_top - 3.15 * gap, 0.18, 0.06, 'Поиск, фильтрация,\nсортировка товаров')
    draw_decision(ax, 0.515, y_top - 4.20 * gap, 0.11, 0.08, 'Роль =\nадминистратор?')
    draw_process(ax, 0.47, y_top - 5.28 * gap, 0.20, 0.06, 'Добавление / редактирование /\nудаление товара')
    draw_decision(ax, 0.515, y_top - 6.35 * gap, 0.11, 0.08, 'Данные товара\nкорректны?')
    draw_process(ax, 0.475, y_top - 7.42 * gap, 0.19, 0.06, 'Сохранение изменений:\nБД + путь к изображению')
    draw_process(ax, 0.475, y_top - 8.42 * gap, 0.19, 0.06, 'Обновление списка товаров\nи уведомление пользователя')

    elbow(ax, [(0.405, y_top - 6.20 * gap + 0.03), (0.445, y_top - 6.20 * gap + 0.03), (0.445, y_top - 0.02 + 0.027), (0.49, y_top - 0.02 + 0.027)])
    elbow(ax, [(0.405, y_top - 2 * gap + 0.03), (0.445, y_top - 2 * gap + 0.03), (0.445, y_top - 0.02 + 0.027), (0.49, y_top - 0.02 + 0.027)])
    arrow(ax, 0.57, y_top - 0.01, 0.57, y_top - gap + 0.06)
    arrow(ax, 0.57, y_top - gap, 0.57, y_top - 2.07 * gap + 0.08)
    arrow(ax, 0.57, y_top - 2.07 * gap, 0.57, y_top - 3.15 * gap + 0.06, label='Да', label_dx=-0.045)
    elbow(ax, [(0.625, y_top - 2.07 * gap + 0.04), (0.67, y_top - 2.07 * gap + 0.04), (0.67, y_top - 8.42 * gap + 0.03), (0.665, y_top - 8.42 * gap + 0.03)], label='Нет', label_pos=(0.66, y_top - 2.07 * gap + 0.07))
    arrow(ax, 0.57, y_top - 3.15 * gap, 0.57, y_top - 4.20 * gap + 0.08)
    arrow(ax, 0.57, y_top - 4.20 * gap, 0.57, y_top - 5.28 * gap + 0.06, label='Да', label_dx=-0.045)
    elbow(ax, [(0.625, y_top - 4.20 * gap + 0.04), (0.69, y_top - 4.20 * gap + 0.04), (0.69, y_top - 8.42 * gap + 0.03), (0.665, y_top - 8.42 * gap + 0.03)], label='Нет', label_pos=(0.685, y_top - 4.20 * gap + 0.07))
    arrow(ax, 0.57, y_top - 5.28 * gap, 0.57, y_top - 6.35 * gap + 0.08)
    arrow(ax, 0.57, y_top - 6.35 * gap, 0.57, y_top - 7.42 * gap + 0.06, label='Да', label_dx=-0.045)
    elbow(ax, [(0.625, y_top - 6.35 * gap + 0.04), (0.68, y_top - 6.35 * gap + 0.04), (0.68, y_top - 7.20 * gap + 0.03), (0.405, y_top - 7.20 * gap + 0.03)], label='Нет', label_pos=(0.665, y_top - 6.35 * gap + 0.07))
    arrow(ax, 0.57, y_top - 7.42 * gap, 0.57, y_top - 8.42 * gap + 0.06)

    # Column 4
    draw_decision(ax, 0.77, y_top - 0.02, 0.11, 0.08, 'Нужен модуль\nзаказов?')
    draw_data(ax, 0.735, y_top - gap - 0.01, 0.18, 0.055, 'Получение заказов,\nстатусов и ПВЗ из БД')
    draw_process(ax, 0.735, y_top - 2.0 * gap, 0.18, 0.06, 'Просмотр заказов\nменеджером / админом')
    draw_decision(ax, 0.77, y_top - 3.05 * gap, 0.11, 0.08, 'Роль =\nадминистратор?')
    draw_process(ax, 0.73, y_top - 4.15 * gap, 0.19, 0.06, 'Добавление / редактирование\nзаказа')
    draw_decision(ax, 0.77, y_top - 5.22 * gap, 0.11, 0.08, 'Проверка данных\nзаказа пройдена?')
    draw_process(ax, 0.73, y_top - 6.30 * gap, 0.19, 0.06, 'Сохранение заказа\nи обновление списка')
    draw_decision(ax, 0.77, y_top - 7.38 * gap, 0.11, 0.08, 'Команда\n«Выход»?')
    draw_terminator(ax, 0.75, y_top - 8.38 * gap, 0.15, 0.045, 'Конец работы')

    elbow(ax, [(0.665, y_top - 8.42 * gap + 0.03), (0.705, y_top - 8.42 * gap + 0.03), (0.705, y_top - 0.02 + 0.04), (0.77, y_top - 0.02 + 0.04)])
    arrow(ax, 0.825, y_top - 0.02 + 0.04, 0.825, y_top - gap - 0.01 + 0.055, label='Да', label_dx=-0.04)
    elbow(ax, [(0.88, y_top - 0.02 + 0.04), (0.94, y_top - 0.02 + 0.04), (0.94, y_top - 7.38 * gap + 0.04), (0.88, y_top - 7.38 * gap + 0.04)], label='Нет', label_pos=(0.935, y_top - 0.02 + 0.07))
    arrow(ax, 0.825, y_top - gap - 0.01, 0.825, y_top - 2.0 * gap + 0.06)
    arrow(ax, 0.825, y_top - 2.0 * gap, 0.825, y_top - 3.05 * gap + 0.08)
    arrow(ax, 0.825, y_top - 3.05 * gap, 0.825, y_top - 4.15 * gap + 0.06, label='Да', label_dx=-0.045)
    elbow(ax, [(0.88, y_top - 3.05 * gap + 0.04), (0.93, y_top - 3.05 * gap + 0.04), (0.93, y_top - 7.38 * gap + 0.04), (0.88, y_top - 7.38 * gap + 0.04)], label='Нет', label_pos=(0.925, y_top - 3.05 * gap + 0.07))
    arrow(ax, 0.825, y_top - 4.15 * gap, 0.825, y_top - 5.22 * gap + 0.08)
    arrow(ax, 0.825, y_top - 5.22 * gap, 0.825, y_top - 6.30 * gap + 0.06, label='Да', label_dx=-0.045)
    elbow(ax, [(0.88, y_top - 5.22 * gap + 0.04), (0.93, y_top - 5.22 * gap + 0.04), (0.93, y_top - 7.38 * gap + 0.04), (0.88, y_top - 7.38 * gap + 0.04)], label='Нет', label_pos=(0.925, y_top - 5.22 * gap + 0.07))
    arrow(ax, 0.825, y_top - 6.30 * gap, 0.825, y_top - 7.38 * gap + 0.08)
    arrow(ax, 0.825, y_top - 7.38 * gap, 0.825, y_top - 8.38 * gap + 0.045, label='Да', label_dx=-0.04)

    # legend block
    ax.add_patch(Rectangle((0.02, 0.03), 0.43, 0.12, fill=False, linewidth=1.0, edgecolor='#2b2b2b'))
    add_text(ax, 0.035, 0.136, 'Условные обозначения:', fontsize=9.5, weight='bold', ha='left')
    draw_terminator(ax, 0.03, 0.055, 0.08, 0.03, 'Старт / стоп')
    draw_process(ax, 0.125, 0.055, 0.08, 0.03, 'Процесс')
    draw_decision(ax, 0.225, 0.048, 0.07, 0.045, 'Решение')
    draw_data(ax, 0.315, 0.055, 0.10, 0.03, 'Данные / БД')

    fig.savefig(output, format='pdf')
    plt.close(fig)


# ---------- ER diagram helpers ----------

class Entity:
    def __init__(self, name: str, fields: list[str], x: float, y: float, w: float, h: float):
        self.name = name
        self.fields = fields
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def draw_entity(ax, entity: Entity):
    ax.add_patch(Rectangle((entity.x, entity.y), entity.w, entity.h, facecolor='white', edgecolor='#222', linewidth=1.2))
    ax.add_patch(Rectangle((entity.x, entity.y + entity.h - 0.05), entity.w, 0.05, facecolor='#2f5aa6', edgecolor='#2f5aa6'))
    ax.text(entity.x + 0.01, entity.y + entity.h - 0.025, entity.name, color='white', fontsize=11, weight='bold', va='center', ha='left')
    line_y = entity.y + entity.h - 0.05 - 0.008
    for field in entity.fields:
        ax.text(entity.x + 0.01, line_y, field, fontsize=9.5, va='top', ha='left', color='#111')
        line_y -= 0.028


def connect(ax, a: Entity, b: Entity, a_side='right', b_side='left', label='1 : M'):
    points = {
        'right': (a.x + a.w, a.y + a.h / 2),
        'left': (a.x, a.y + a.h / 2),
        'top': (a.x + a.w / 2, a.y + a.h),
        'bottom': (a.x + a.w / 2, a.y),
    }
    x1, y1 = points[a_side]
    x2, y2 = {
        'right': (b.x + b.w, b.y + b.h / 2),
        'left': (b.x, b.y + b.h / 2),
        'top': (b.x + b.w / 2, b.y + b.h),
        'bottom': (b.x + b.w / 2, b.y),
    }[b_side]
    ax.add_line(Line2D([x1, x2], [y1, y2], color='#555', linewidth=1.1))
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx, my + 0.015, label, fontsize=9, color='#222', ha='center', va='bottom', bbox=dict(facecolor='white', edgecolor='none', pad=0.2))


def generate_er(output: Path) -> None:
    fig = plt.figure(figsize=(16, 10))
    ax = plt.axes([0.02, 0.04, 0.96, 0.9])
    ax.set_xlim(0, 1.30)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.02, 0.97, 'ER-диаграмма БД ИС «Магазин обуви»', fontsize=22, weight='bold', ha='left', va='top')
    ax.text(0.02, 0.92, 'Диаграмма отражает роли пользователей, каталог товаров, заказы и связанные справочники.', fontsize=11.5, ha='left', va='top')

    entities = {
        'roles': Entity('roles', ['PK id', 'name'], 0.00, 0.70, 0.22, 0.11),
        'users': Entity('users', ['PK id', 'FK role_id', 'full_name', 'login', 'password'], 0.00, 0.41, 0.22, 0.18),
        'suppliers': Entity('suppliers', ['PK id', 'name'], 0.27, 0.70, 0.22, 0.11),
        'manufacturers': Entity('manufacturers', ['PK id', 'name'], 0.27, 0.49, 0.22, 0.11),
        'categories': Entity('categories', ['PK id', 'name'], 0.27, 0.28, 0.22, 0.11),
        'products': Entity('products', ['PK id', 'article', 'name', 'unit', 'price', 'FK supplier_id', 'FK manufacturer_id', 'FK category_id', 'discount_percent', 'stock_quantity', 'description', 'image_path'], 0.60, 0.22, 0.31, 0.44),
        'statuses': Entity('order_statuses', ['PK id', 'name'], 0.31, 0.06, 0.22, 0.10),
        'pickup': Entity('pickup_points', ['PK id', 'address'], 0.92, 0.54, 0.25, 0.10),
        'orders': Entity('orders', ['PK id', 'order_number', 'article_summary', 'FK status_id', 'FK pickup_point_id', 'order_date', 'delivery_date', 'customer_name', 'pickup_code'], 0.93, 0.18, 0.24, 0.32),
        'items': Entity('order_items', ['PK id', 'FK order_id', 'FK product_id', 'quantity'], 1.02, 0.02, 0.22, 0.16),
    }

    for ent in entities.values():
        draw_entity(ax, ent)

    connect(ax, entities['roles'], entities['users'], 'bottom', 'top')
    connect(ax, entities['suppliers'], entities['products'])
    connect(ax, entities['manufacturers'], entities['products'])
    connect(ax, entities['categories'], entities['products'])
    connect(ax, entities['statuses'], entities['orders'], 'right', 'left')
    connect(ax, entities['pickup'], entities['orders'], 'bottom', 'top')
    connect(ax, entities['orders'], entities['items'], 'bottom', 'top')
    connect(ax, entities['products'], entities['items'], 'right', 'left')

    fig.savefig(output, format='pdf')
    plt.close(fig)


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    generate_flowchart(DOCS_DIR / 'algorithm_flowchart.pdf')
    generate_er(DOCS_DIR / 'er_diagram.pdf')
    print('Диаграммы успешно пересозданы.')


if __name__ == '__main__':
    main()
