from __future__ import annotations

import tkinter as tk
from contextlib import suppress
from datetime import date, datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageOps, ImageTk

from .models import Product, User
from .repository import Repository
from .services import ImageService

WINDOW_TITLE = 'ООО «Обувь»'
CARD_BG = '#FFFFFF'
DISCOUNT_BG = '#2E8B57'
OUT_OF_STOCK_BG = '#87CEEB'
HEADER_BG = '#F2F2F2'


class ShoeStoreApp(tk.Tk):
    def __init__(self, repository: Repository, image_service: ImageService) -> None:
        super().__init__()
        self.repository = repository
        self.image_service = image_service
        self.current_user: User | None = None
        self.product_form_window: ProductForm | None = None
        self.order_form_window: OrderForm | None = None
        self.title(f'{WINDOW_TITLE} - Авторизация')
        self.geometry('1240x820')
        self.minsize(1080, 720)
        icon_path = image_service.resources_dir / 'images' / 'Icon.ico'
        with suppress(tk.TclError):
            self.iconbitmap(default=icon_path)
        self._images: list[ImageTk.PhotoImage] = []
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill='both', expand=True)
        self.show_login_screen()

    def clear_container(self) -> None:
        for child in self.main_container.winfo_children():
            child.destroy()
        self._images.clear()

    def show_login_screen(self) -> None:
        self.current_user = None
        self.clear_container()
        self.title(f'{WINDOW_TITLE} - Авторизация')
        LoginView(self.main_container, self).pack(fill='both', expand=True)

    def login_as_guest(self) -> None:
        self.current_user = User(0, 'Гость', '', '', 'Гость')
        self.show_products_screen()

    def login(self, login: str, password: str) -> None:
        user = self.repository.authenticate(login, password)
        if user is None:
            messagebox.showerror('Ошибка авторизации', 'Неверный логин или пароль. Проверьте данные и повторите попытку.')
            return
        self.current_user = user
        self.show_products_screen()

    def logout(self) -> None:
        self.show_login_screen()

    def show_products_screen(self) -> None:
        self.clear_container()
        self.title(f'{WINDOW_TITLE} - Список товаров')
        ProductListView(self.main_container, self).pack(fill='both', expand=True)

    def show_orders_screen(self) -> None:
        if self.current_user is None:
            return
        self.clear_container()
        self.title(f'{WINDOW_TITLE} - Заказы')
        OrdersView(self.main_container, self).pack(fill='both', expand=True)

    def open_product_form(self, product_id: int | None = None) -> None:
        if self.current_user is None or self.current_user.role != 'Администратор':
            messagebox.showwarning('Доступ запрещён', 'Добавлять и редактировать товары может только администратор.')
            return
        if self.product_form_window is not None and self.product_form_window.winfo_exists():
            self.product_form_window.focus_set()
            return
        self.product_form_window = ProductForm(self, self.repository, self.image_service, product_id)

    def open_order_form(self, order_id: int | None = None) -> None:
        if self.current_user is None or self.current_user.role != 'Администратор':
            messagebox.showwarning('Доступ запрещён', 'Добавлять и редактировать заказы может только администратор.')
            return
        if self.order_form_window is not None and self.order_form_window.winfo_exists():
            self.order_form_window.focus_set()
            return
        self.order_form_window = OrderForm(self, self.repository, order_id)


class Header(ttk.Frame):
    def __init__(self, master: tk.Widget, app: ShoeStoreApp, title_text: str) -> None:
        super().__init__(master, padding=12)
        self.app = app
        self.columnconfigure(1, weight=1)
        self.logo_label = ttk.Label(self)
        self.logo_label.grid(row=0, column=0, rowspan=2, sticky='w', padx=(0, 12))

        logo_path = app.image_service.resources_dir / 'images' / 'Icon.png'
        with Image.open(logo_path) as image:
            logo = ImageTk.PhotoImage(image.resize((64, 64)))
        app._images.append(logo)
        self.logo_label.configure(image=logo)

        ttk.Label(self, text=WINDOW_TITLE, font=('Segoe UI', 18, 'bold')).grid(row=0, column=1, sticky='w')
        ttk.Label(self, text=title_text, font=('Segoe UI', 11)).grid(row=1, column=1, sticky='w')
        user_text = app.current_user.full_name if app.current_user else 'Неизвестный пользователь'
        ttk.Label(self, text=user_text, font=('Segoe UI', 11, 'bold')).grid(row=0, column=2, sticky='e', padx=(8, 12))
        ttk.Button(self, text='Выход', command=app.logout).grid(row=1, column=2, sticky='e')


class LoginView(ttk.Frame):
    def __init__(self, master: tk.Widget, app: ShoeStoreApp) -> None:
        super().__init__(master, padding=20)
        self.app = app
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        box = ttk.Frame(self, padding=30)
        box.grid(row=0, column=0)
        ttk.Label(box, text=WINDOW_TITLE, font=('Segoe UI', 24, 'bold')).pack(pady=(0, 10))
        ttk.Label(box, text='Вход в систему', font=('Segoe UI', 14)).pack(pady=(0, 24))

        self.login_var = tk.StringVar()
        self.password_var = tk.StringVar()
        ttk.Label(box, text='Логин').pack(anchor='w')
        ttk.Entry(box, textvariable=self.login_var, width=40).pack(pady=(0, 12))
        ttk.Label(box, text='Пароль').pack(anchor='w')
        ttk.Entry(box, textvariable=self.password_var, width=40, show='*').pack(pady=(0, 20))
        ttk.Button(box, text='Войти', command=self._login).pack(fill='x', pady=(0, 10))
        ttk.Button(box, text='Продолжить как гость', command=app.login_as_guest).pack(fill='x')

    def _login(self) -> None:
        self.app.login(self.login_var.get(), self.password_var.get())


class ProductListView(ttk.Frame):
    def __init__(self, master: tk.Widget, app: ShoeStoreApp) -> None:
        super().__init__(master)
        self.app = app
        self.search_var = tk.StringVar()
        self.supplier_var = tk.StringVar(value='Все поставщики')
        self.sort_var = tk.StringVar(value='Без сортировки')
        self.products: list[Product] = []

        Header(self, app, 'Список товаров').pack(fill='x')
        self._build_toolbar()
        self._build_canvas()
        self.refresh_products()

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self, padding=(12, 0, 12, 12))
        toolbar.pack(fill='x')
        role = self.app.current_user.role if self.app.current_user else 'Гость'
        if role in {'Менеджер', 'Администратор'}:
            ttk.Label(toolbar, text='Поиск:').pack(side='left')
            search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=28)
            search_entry.pack(side='left', padx=(6, 12))
            search_entry.bind('<KeyRelease>', lambda _event: self.refresh_products())

            ttk.Label(toolbar, text='Поставщик:').pack(side='left')
            suppliers = ['Все поставщики'] + self.app.repository.get_suppliers()
            supplier_box = ttk.Combobox(toolbar, textvariable=self.supplier_var, values=suppliers, state='readonly', width=24)
            supplier_box.pack(side='left', padx=(6, 12))
            supplier_box.bind('<<ComboboxSelected>>', lambda _event: self.refresh_products())

            ttk.Label(toolbar, text='Сортировка:').pack(side='left')
            sort_box = ttk.Combobox(
                toolbar,
                textvariable=self.sort_var,
                values=['Без сортировки', 'По количеству: возрастание', 'По количеству: убывание'],
                state='readonly',
                width=28,
            )
            sort_box.pack(side='left', padx=(6, 12))
            sort_box.bind('<<ComboboxSelected>>', lambda _event: self.refresh_products())

        if role in {'Менеджер', 'Администратор'}:
            ttk.Button(toolbar, text='Заказы', command=self.app.show_orders_screen).pack(side='right', padx=(8, 0))
        if role == 'Администратор':
            ttk.Button(toolbar, text='Добавить товар', command=lambda: self.app.open_product_form()).pack(side='right')

    def _build_canvas(self) -> None:
        self.canvas = tk.Canvas(self, bg='#EDEDED', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.cards_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.cards_frame, anchor='nw')
        self.cards_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)

    def _on_frame_configure(self, _event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self.canvas_window, width=event.width)

    def refresh_products(self) -> None:
        for child in self.cards_frame.winfo_children():
            child.destroy()
        self.products = self.app.repository.get_products(
            search_text=self.search_var.get(),
            supplier_name=self.supplier_var.get(),
            sort_order=self.sort_var.get(),
        )
        ttk.Label(self.cards_frame, text=f'Найдено товаров: {len(self.products)}', padding=(12, 6), font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        for product in self.products:
            self._add_product_card(product)

    def _add_product_card(self, product: Product) -> None:
        background = CARD_BG
        if product.stock_quantity == 0:
            background = OUT_OF_STOCK_BG
        elif product.discount_percent > 15:
            background = DISCOUNT_BG

        card = tk.Frame(self.cards_frame, bg=background, bd=1, relief='solid', padx=12, pady=10)
        card.pack(fill='x', padx=12, pady=6)
        card.columnconfigure(1, weight=1)
        image_path = self.app.image_service.resolve_image(product.image_path)
        with Image.open(image_path) as image:
            preview = ImageOps.contain(image.convert('RGB'), (160, 100))
            tk_image = ImageTk.PhotoImage(preview)
        self.app._images.append(tk_image)
        tk.Label(card, image=tk_image, bg=background).grid(row=0, column=0, rowspan=6, sticky='nw', padx=(0, 12))

        text_color = 'white' if background == DISCOUNT_BG else 'black'
        tk.Label(card, text=f'{product.article} - {product.name}', bg=background, fg=text_color, font=('Segoe UI', 12, 'bold')).grid(row=0, column=1, sticky='w')
        tk.Label(card, text=f'Категория: {product.category_name}', bg=background, fg=text_color, font=('Segoe UI', 10)).grid(row=1, column=1, sticky='w')
        tk.Label(card, text=f'Производитель: {product.manufacturer_name}', bg=background, fg=text_color, font=('Segoe UI', 10)).grid(row=2, column=1, sticky='w')
        tk.Label(card, text=f'Поставщик: {product.supplier_name}', bg=background, fg=text_color, font=('Segoe UI', 10)).grid(row=3, column=1, sticky='w')
        tk.Label(card, text=f'Единица измерения: {product.unit} | На складе: {product.stock_quantity}', bg=background, fg=text_color, font=('Segoe UI', 10)).grid(row=4, column=1, sticky='w')
        tk.Label(card, text=f'Описание: {product.description}', bg=background, fg=text_color, font=('Segoe UI', 10), wraplength=750, justify='left').grid(row=5, column=1, sticky='w')

        price_frame = tk.Frame(card, bg=background)
        price_frame.grid(row=0, column=2, sticky='ne')
        if product.discount_percent > 0:
            tk.Label(price_frame, text=f'{product.price:,.2f} ₽'.replace(',', ' '), bg=background, fg='red', font=('Segoe UI', 10, 'overstrike')).pack(anchor='e')
            tk.Label(price_frame, text=f'{product.discounted_price:,.2f} ₽'.replace(',', ' '), bg=background, fg='black', font=('Segoe UI', 11, 'bold')).pack(anchor='e')
        else:
            tk.Label(price_frame, text=f'{product.price:,.2f} ₽'.replace(',', ' '), bg=background, fg=text_color, font=('Segoe UI', 11, 'bold')).pack(anchor='e')
        tk.Label(card, text=f'Скидка: {product.discount_percent}%', bg=background, fg=text_color, font=('Segoe UI', 10)).grid(row=1, column=2, sticky='ne')

        if self.app.current_user and self.app.current_user.role == 'Администратор':
            actions = ttk.Frame(card)
            actions.grid(row=5, column=2, sticky='se')
            ttk.Button(actions, text='Редактировать', command=lambda value=product.id: self.app.open_product_form(value)).pack(side='left', padx=(0, 8))
            ttk.Button(actions, text='Удалить', command=lambda value=product: self._delete_product(value)).pack(side='left')
            for widget in actions.winfo_children():
                widget.configure(cursor='hand2')

    def _delete_product(self, product: Product) -> None:
        if not self.app.repository.can_delete_product(product.id):
            messagebox.showwarning('Удаление невозможно', 'Нельзя удалить товар, который присутствует в заказе.')
            return
        confirmed = messagebox.askyesno('Подтверждение удаления', f'Удалить товар {product.article} - {product.name}?')
        if not confirmed:
            return
        self.app.image_service.delete_if_managed(product.image_path)
        self.app.repository.delete_product(product.id)
        self.refresh_products()
        messagebox.showinfo('Удаление выполнено', 'Товар успешно удалён.')


class ProductForm(tk.Toplevel):
    def __init__(self, app: ShoeStoreApp, repository: Repository, image_service: ImageService, product_id: int | None) -> None:
        super().__init__(app)
        self.app = app
        self.repository = repository
        self.image_service = image_service
        self.product_id = product_id
        self.selected_image_source: Path | None = None
        self.saved_image_path: str | None = None
        self.original_image_path: str | None = None
        self.title(f'{WINDOW_TITLE} - {"Редактирование товара" if product_id else "Добавление товара"}')
        self.geometry('760x680')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)

        self.vars = {
            'article': tk.StringVar(),
            'name': tk.StringVar(),
            'category_name': tk.StringVar(),
            'manufacturer_name': tk.StringVar(),
            'supplier_name': tk.StringVar(),
            'price': tk.StringVar(),
            'unit': tk.StringVar(value='шт.'),
            'stock_quantity': tk.StringVar(),
            'discount_percent': tk.StringVar(value='0'),
            'description': tk.StringVar(),
        }
        self._build_form()
        self._load_product()
        self.transient(app)
        self.grab_set()

    def _build_form(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill='both', expand=True)
        frame.columnconfigure(1, weight=1)
        next_id = self.repository.get_next_product_id() if self.product_id is None else self.product_id
        ttk.Label(frame, text='ID товара').grid(row=0, column=0, sticky='w', pady=6)
        self.id_entry = ttk.Entry(frame, state='readonly')
        self.id_entry.grid(row=0, column=1, sticky='ew', pady=6)
        self.id_entry.configure(state='normal')
        self.id_entry.insert(0, str(next_id))
        self.id_entry.configure(state='readonly')

        row = 1
        for label_text, name, values in [
            ('Артикул', 'article', None),
            ('Наименование товара', 'name', None),
            ('Категория товара', 'category_name', self.repository.get_categories()),
            ('Производитель', 'manufacturer_name', self.repository.get_manufacturers()),
            ('Поставщик', 'supplier_name', self.repository.get_suppliers()),
            ('Цена', 'price', None),
            ('Единица измерения', 'unit', None),
            ('Количество на складе', 'stock_quantity', None),
            ('Действующая скидка', 'discount_percent', None),
        ]:
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky='w', pady=6)
            if values is None:
                widget = ttk.Entry(frame, textvariable=self.vars[name])
            else:
                widget = ttk.Combobox(frame, textvariable=self.vars[name], values=values, state='readonly')
            widget.grid(row=row, column=1, sticky='ew', pady=6)
            row += 1

        ttk.Label(frame, text='Описание товара').grid(row=row, column=0, sticky='nw', pady=6)
        self.description_text = tk.Text(frame, height=6, width=50)
        self.description_text.grid(row=row, column=1, sticky='ew', pady=6)
        row += 1

        image_row = ttk.Frame(frame)
        image_row.grid(row=row, column=1, sticky='w', pady=6)
        ttk.Button(image_row, text='Выбрать изображение', command=self._choose_image).pack(side='left')
        self.image_label = ttk.Label(image_row, text='Изображение не выбрано')
        self.image_label.pack(side='left', padx=10)
        row += 1

        actions = ttk.Frame(frame)
        actions.grid(row=row, column=1, sticky='e', pady=(18, 0))
        ttk.Button(actions, text='Сохранить', command=self._save).pack(side='left', padx=(0, 8))
        ttk.Button(actions, text='Отмена', command=self._close).pack(side='left')

    def _load_product(self) -> None:
        if self.product_id is None:
            return
        product = self.repository.get_product_by_id(self.product_id)
        if product is None:
            messagebox.showerror('Ошибка', 'Не удалось загрузить выбранный товар.')
            self._close()
            return
        self.vars['article'].set(product.article)
        self.vars['name'].set(product.name)
        self.vars['category_name'].set(product.category_name)
        self.vars['manufacturer_name'].set(product.manufacturer_name)
        self.vars['supplier_name'].set(product.supplier_name)
        self.vars['price'].set(str(product.price))
        self.vars['unit'].set(product.unit)
        self.vars['stock_quantity'].set(str(product.stock_quantity))
        self.vars['discount_percent'].set(str(product.discount_percent))
        self.description_text.delete('1.0', 'end')
        self.description_text.insert('1.0', product.description)
        self.original_image_path = product.image_path
        self.saved_image_path = product.image_path
        self.image_label.configure(text=Path(product.image_path).name if product.image_path else 'Используется заглушка')

    def _choose_image(self) -> None:
        file_name = filedialog.askopenfilename(
            title='Выберите изображение',
            filetypes=[('Изображения', '*.png *.jpg *.jpeg *.bmp')],
        )
        if not file_name:
            return
        self.selected_image_source = Path(file_name)
        self.image_label.configure(text=self.selected_image_source.name)

    def _save(self) -> None:
        try:
            article = self.vars['article'].get().strip()
            if not article:
                raise ValueError('Поле «Артикул» обязательно для заполнения.')
            name = self.vars['name'].get().strip()
            if not name:
                raise ValueError('Поле «Наименование товара» обязательно для заполнения.')
            category_name = self.vars['category_name'].get().strip()
            manufacturer_name = self.vars['manufacturer_name'].get().strip()
            supplier_name = self.vars['supplier_name'].get().strip()
            if not category_name or not manufacturer_name or not supplier_name:
                raise ValueError('Выберите категорию, производителя и поставщика товара.')
            price = float(self.vars['price'].get().replace(',', '.'))
            if price < 0:
                raise ValueError('Стоимость товара не может быть отрицательной.')
            stock_quantity = int(self.vars['stock_quantity'].get())
            if stock_quantity < 0:
                raise ValueError('Количество товара на складе не может быть отрицательным.')
            discount_percent = int(self.vars['discount_percent'].get())
            if not 0 <= discount_percent <= 100:
                raise ValueError('Размер скидки должен быть в диапазоне от 0 до 100%.')

            if self.selected_image_source is not None:
                new_image_path = self.image_service.save_product_image(self.selected_image_source)
                if self.original_image_path and self.original_image_path != new_image_path:
                    self.image_service.delete_if_managed(self.original_image_path)
                self.saved_image_path = new_image_path

            data = {
                'article': article,
                'name': name,
                'category_name': category_name,
                'manufacturer_name': manufacturer_name,
                'supplier_name': supplier_name,
                'price': price,
                'unit': self.vars['unit'].get().strip() or 'шт.',
                'stock_quantity': stock_quantity,
                'discount_percent': discount_percent,
                'description': self.description_text.get('1.0', 'end').strip(),
                'image_path': self.saved_image_path,
            }
            self.repository.save_product(data, self.product_id)
            self.app.show_products_screen()
            messagebox.showinfo('Сохранение выполнено', 'Данные о товаре успешно сохранены.')
            self._close()
        except ValueError as error:
            messagebox.showerror('Ошибка ввода', str(error))

    def _close(self) -> None:
        self.app.product_form_window = None
        self.destroy()


class OrdersView(ttk.Frame):
    def __init__(self, master: tk.Widget, app: ShoeStoreApp) -> None:
        super().__init__(master)
        self.app = app
        Header(self, app, 'Список заказов').pack(fill='x')
        self._build_toolbar()
        self._build_table()
        self.refresh_orders()

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self, padding=(12, 0, 12, 12))
        toolbar.pack(fill='x')
        ttk.Button(toolbar, text='Назад к товарам', command=self.app.show_products_screen).pack(side='left')
        if self.app.current_user and self.app.current_user.role == 'Администратор':
            ttk.Button(toolbar, text='Добавить заказ', command=lambda: self.app.open_order_form()).pack(side='right')

    def _build_table(self) -> None:
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill='both', expand=True)
        columns = ('number', 'articles', 'status', 'address', 'order_date', 'delivery_date', 'customer', 'code')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        headings = {
            'number': 'Номер',
            'articles': 'Артикул заказа',
            'status': 'Статус',
            'address': 'Пункт выдачи',
            'order_date': 'Дата заказа',
            'delivery_date': 'Дата выдачи',
            'customer': 'Клиент',
            'code': 'Код',
        }
        widths = {'number': 70, 'articles': 220, 'status': 120, 'address': 260, 'order_date': 110, 'delivery_date': 110, 'customer': 220, 'code': 70}
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor='center')
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        if self.app.current_user and self.app.current_user.role == 'Администратор':
            self.tree.bind('<Double-1>', self._open_selected_order)
            button_row = ttk.Frame(self)
            button_row.pack(fill='x', padx=12, pady=(0, 12))
            ttk.Button(button_row, text='Редактировать выбранный заказ', command=self._edit_selected).pack(side='left')
            ttk.Button(button_row, text='Удалить выбранный заказ', command=self._delete_selected).pack(side='left', padx=8)

    def refresh_orders(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for order in self.app.repository.get_orders():
            self.tree.insert(
                '',
                'end',
                iid=str(order.id),
                values=(
                    order.order_number,
                    order.article_summary,
                    order.status_name,
                    order.pickup_address,
                    order.order_date.isoformat() if order.order_date else '',
                    order.delivery_date.isoformat() if order.delivery_date else '',
                    order.customer_name,
                    order.pickup_code,
                ),
            )

    def _get_selected_order_id(self) -> int | None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning('Заказ не выбран', 'Сначала выберите заказ из списка.')
            return None
        return int(selection[0])

    def _open_selected_order(self, _event: tk.Event) -> None:
        self._edit_selected()

    def _edit_selected(self) -> None:
        order_id = self._get_selected_order_id()
        if order_id is not None:
            self.app.open_order_form(order_id)

    def _delete_selected(self) -> None:
        order_id = self._get_selected_order_id()
        if order_id is None:
            return
        if not messagebox.askyesno('Подтверждение удаления', 'Удалить выбранный заказ?'):
            return
        self.app.repository.delete_order(order_id)
        self.refresh_orders()
        messagebox.showinfo('Удаление выполнено', 'Заказ успешно удалён.')


class OrderForm(tk.Toplevel):
    def __init__(self, app: ShoeStoreApp, repository: Repository, order_id: int | None) -> None:
        super().__init__(app)
        self.app = app
        self.repository = repository
        self.order_id = order_id
        self.title(f'{WINDOW_TITLE} - {"Редактирование заказа" if order_id else "Добавление заказа"}')
        self.geometry('760x480')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self._close)
        self.vars = {
            'order_number': tk.StringVar(value=str(self.repository.get_next_order_number())),
            'article_summary': tk.StringVar(),
            'status_name': tk.StringVar(),
            'pickup_address': tk.StringVar(),
            'order_date': tk.StringVar(value=date.today().isoformat()),
            'delivery_date': tk.StringVar(value=date.today().isoformat()),
            'customer_name': tk.StringVar(value='Не указан'),
            'pickup_code': tk.StringVar(),
        }
        self._build_form()
        self._load_order()
        self.transient(app)
        self.grab_set()

    def _build_form(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill='both', expand=True)
        frame.columnconfigure(1, weight=1)
        specs = [
            ('Номер заказа', 'order_number', None),
            ('Артикул заказа', 'article_summary', None),
            ('Статус заказа', 'status_name', self.repository.get_statuses()),
            ('Адрес пункта выдачи', 'pickup_address', self.repository.get_pickup_points()),
            ('Дата заказа (ГГГГ-ММ-ДД)', 'order_date', None),
            ('Дата выдачи (ГГГГ-ММ-ДД)', 'delivery_date', None),
            ('ФИО клиента', 'customer_name', None),
            ('Код для получения', 'pickup_code', None),
        ]
        for row, (label_text, name, values) in enumerate(specs):
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky='w', pady=6)
            if values is None:
                widget = ttk.Entry(frame, textvariable=self.vars[name])
            else:
                widget = ttk.Combobox(frame, textvariable=self.vars[name], values=values, state='readonly')
            widget.grid(row=row, column=1, sticky='ew', pady=6)

        buttons = ttk.Frame(frame)
        buttons.grid(row=len(specs), column=1, sticky='e', pady=(18, 0))
        ttk.Button(buttons, text='Сохранить', command=self._save).pack(side='left', padx=(0, 8))
        ttk.Button(buttons, text='Отмена', command=self._close).pack(side='left')

    def _load_order(self) -> None:
        if self.order_id is None:
            statuses = self.repository.get_statuses()
            if statuses:
                self.vars['status_name'].set(statuses[0])
            pickup_points = self.repository.get_pickup_points()
            if pickup_points:
                self.vars['pickup_address'].set(pickup_points[0])
            return
        order = self.repository.get_order_by_id(self.order_id)
        if order is None:
            messagebox.showerror('Ошибка', 'Не удалось загрузить заказ.')
            self._close()
            return
        self.vars['order_number'].set(str(order.order_number))
        self.vars['article_summary'].set(order.article_summary)
        self.vars['status_name'].set(order.status_name)
        self.vars['pickup_address'].set(order.pickup_address)
        self.vars['order_date'].set(order.order_date.isoformat() if order.order_date else '')
        self.vars['delivery_date'].set(order.delivery_date.isoformat() if order.delivery_date else '')
        self.vars['customer_name'].set(order.customer_name)
        self.vars['pickup_code'].set(order.pickup_code)

    def _save(self) -> None:
        try:
            order_number = int(self.vars['order_number'].get())
            article_summary = self.vars['article_summary'].get().strip()
            if not article_summary:
                raise ValueError('Поле «Артикул заказа» обязательно для заполнения.')
            status_name = self.vars['status_name'].get().strip()
            pickup_address = self.vars['pickup_address'].get().strip()
            if not status_name or not pickup_address:
                raise ValueError('Необходимо выбрать статус заказа и пункт выдачи.')
            for key in ('order_date', 'delivery_date'):
                value = self.vars[key].get().strip()
                if value:
                    datetime.strptime(value, '%Y-%m-%d')
            payload = {
                'order_number': order_number,
                'article_summary': article_summary,
                'status_name': status_name,
                'pickup_address': pickup_address,
                'order_date': self.vars['order_date'].get().strip(),
                'delivery_date': self.vars['delivery_date'].get().strip(),
                'customer_name': self.vars['customer_name'].get().strip() or 'Не указан',
                'pickup_code': self.vars['pickup_code'].get().strip(),
            }
            self.repository.save_order(payload, self.order_id)
            self.app.show_orders_screen()
            messagebox.showinfo('Сохранение выполнено', 'Данные о заказе успешно сохранены.')
            self._close()
        except ValueError as error:
            messagebox.showerror('Ошибка ввода', f'Проверьте введённые данные.\n{error}')

    def _close(self) -> None:
        self.app.order_form_window = None
        self.destroy()
