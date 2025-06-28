import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import PhotoImage
from sqlalchemy import create_engine, text

DATABASE_URL = 'postgresql+psycopg2://app_user:666@localhost:5432/project' #DATABASE_URL ='postgresql+psycopg2://app_user:666@localhost:5432/project' 'postgresql+psycopg2://postgres:777@localhost:5432/project'

#создаём объект engine, который управляет подключениями к бд
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Соединение с базой данных успешно!")
except Exception as e:
    print(f"Ошибка при подключении: {e}")


def open_edit_student_window(student_data):
    edit_window = tk.Toplevel()
    edit_window.title("Редактирование данных студента")
    edit_window.geometry("500x800")

    email = student_data[0]
    name = student_data[1]
    current_city = student_data[2]
    phone = student_data[3]
    student_class = student_data[4]

    tk.Label(edit_window, text=f"Email: {email}", font=("Palatino Linotype", 14)).pack(pady=5)
    tk.Label(edit_window, text=f"ФИО: {name}", font=("Palatino Linotype", 14)).pack(pady=5)
    tk.Label(edit_window, text=f"Город: {current_city}", font=("Palatino Linotype", 14)).pack(pady=5)
    tk.Label(edit_window, text=f"Телефон: {phone}", font=("Palatino Linotype", 14)).pack(pady=5)
    tk.Label(edit_window, text=f"Класс: {student_class}", font=("Palatino Linotype", 14)).pack(pady=5)

    change_options = ["Город", "Телефон", "ФИО", "Класс"]
    option_var = tk.StringVar(edit_window)
    option_var.set(change_options[0])

    tk.Label(edit_window, text="Выберите, что изменить:", font=("Palatino Linotype", 14)).pack(pady=10)
    dropdown = tk.OptionMenu(edit_window, option_var, *change_options)
    dropdown.pack(pady=10)

    def save_changes():
        selected_option = option_var.get()
        new_value = new_value_entry.get().strip()
        if not new_value:
            messagebox.showwarning("Ошибка", "Новое значение не может быть пустым!")
            return
        try:
            if selected_option == "ФИО":
                query = "SELECT update_student_name(:email, :new_value);"
            elif selected_option == "Город":
                query = "SELECT update_student_city(:email, :new_value);"
            elif selected_option == "Телефон":
                query = "SELECT update_student_phone_number(:email, :new_value);"
            elif selected_option == "Класс":
                query = "SELECT update_student_class(:email, :new_value);"

            with engine.connect() as connection:
                with connection.begin():
                    connection.execute(text(query), {"new_value": new_value, "email": email})
            messagebox.showinfo("Успех", f"{selected_option} успешно обновлен!")
            edit_window.destroy()
        except Exception as e:
            print(f"Ошибка при изменении данных: {e}")
            messagebox.showerror("Ошибка", "Произошла ошибка при изменении данных.")

    tk.Label(edit_window, text="Введите новое значение:", font=("Palatino Linotype", 14)).pack(pady=10)
    new_value_entry = tk.Entry(edit_window, font=("Palatino Linotype", 14), width=30)
    new_value_entry.pack(pady=10)

    tk.Button(edit_window, text="Сохранить изменения", font=("Palatino Linotype", 14), command=save_changes).pack(pady=10)
    tk.Button(edit_window, text="Закрыть", font=("Palatino Linotype", 14), command=edit_window.destroy).pack(pady=10)


def search_student_by_email_for_edit():
    search_window = tk.Toplevel()
    search_window.title("Поиск студента по email для редактирования")
    search_window.geometry("500x300")

    tk.Label(search_window, text="Введите email студента:", font=("Palatino Linotype", 14)).pack(pady=10)

    email_entry = tk.Entry(search_window, font=("Palatino Linotype", 14), width=30)
    email_entry.pack(pady=10)

    def find_student():
        email = email_entry.get().strip()

        query = "SELECT * FROM print_student_by_email(:email)"
        try:
            with engine.connect() as connect:
                result = connect.execute(text(query), {"email": email}).fetchone() #fetchone для получения только1  строки

                if result:
                    open_edit_student_window(result)
                    search_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Студент с таким email не найден!")
        except Exception as e:
            print(f"Ошибка при поиске студента: {e}")
            messagebox.showerror("Ошибка", "Произошла ошибка при поиске студента.")

    tk.Button(search_window, text="Найти", font=("Palatino Linotype", 14), command=find_student).pack(pady=10)
    tk.Button(search_window, text="Закрыть", font=("Palatino Linotype", 14), command=search_window.destroy).pack(pady=10)



def insert_student(email, name, city, phone_number, student_class):
    query = """
    SELECT public.insert_into_students(:email, :name, :city, :phone_number, :student_class);
    """

    try:
        with engine.connect() as connection:
            with connection.begin():
                result = connection.execute(text(query), {
                    "email": email,
                    "name": name,
                    "city": city,
                    "phone_number": phone_number,
                    "student_class": student_class
                })


                connection.commit()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")



def print_students(user_window):
    query_call_func = "SELECT * FROM print_students()"
    try:
        with engine.connect() as connect:
            result = connect.execute(text(query_call_func))
            tk.Label(user_window, text=f'EMAIL - ФИО - ГОРОД - ТЕЛЕФОН - КЛАСС',
                     font=("Palatino Linotype", 15)).pack(pady=5)
            for row in result:
                tk.Label(user_window, text=f'{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}',
                         font=("Palatino Linotype", 15)).pack(pady=5)
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        tk.Label(user_window, text="Ошибка при загрузке данных", font=("Palatino Linotype", 15)).pack(pady=5)


def print_courses(courses_window):
    query_call_func = "SELECT * FROM print_courses()"
    try:
        with engine.connect() as connect:
            result = connect.execute(text(query_call_func))
            tk.Label(courses_window, text =f'КОДИРОВКА - ПРЕДМЕТ - ДЛИТЕЛЬНОСТЬ - КЛАСС - ЦЕНА', font=("Palatino Linotype", 8)).pack(pady=5)
            for row in result:
                tk.Label(courses_window, text=f'{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}',
                         font=("Palatino Linotype", 8)).pack(pady=5)
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        tk.Label(courses_window, text="Ошибка при загрузке данных", font=("Palatino Linotype", 15)).pack(pady=5)


def verify_code():
    code = code_entry.get()
    email = email_entry.get()

    if not code.isdigit() or len(code) != 6:
        messagebox.showerror("Ошибка", "Неверный код. Введите 6-значный код с почты.")
        return

    #чек админа
    if email == "админ":
        if code == "666666":
            login_window.withdraw()
            open_admin_panel()
        else:
            messagebox.showerror("Ошибка", "Неверный код. Доступ запрещен.")
            code_window.destroy()
        return

    try:
        query_check_email = "SELECT public.check_email(:email);"
        with engine.connect() as connection:
            email_exists = connection.execute(text(query_check_email), {"email": email}).scalar()

        if email_exists:
            login_window.withdraw()
            open_personal_account(email)
        else:
            login_window.withdraw()
            registration_form(email)
    except Exception as e:
        messagebox.showerror("Ошибка", "Произошла ошибка при обработке запроса.")
    code_window.destroy()


def print_teachers(teachers_window):
    query_call_func = "SELECT * FROM print_teachers()"
    try:
        with engine.connect() as connect:
            result = connect.execute(text(query_call_func))
            tk.Label(teachers_window, text=f'ИНН - ФИО - СТАЖ ',
                     font=("Palatino Linotype", 15)).pack(pady=5)
            for row in result:
                tk.Label(teachers_window, text=f'{row[0]} - {row[1]} - {row[2]}',
                         font=("Palatino Linotype", 15)).pack(pady=5)
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        tk.Label(teachers_window, text="Ошибка при загрузке данных", font=("Palatino Linotype", 15)).pack(pady=5)


def show_teachers():
    teachers_window = tk.Toplevel()
    teachers_window.title("Список преподов")
    teachers_window.geometry("600x800")


    tk.Label(teachers_window, text="Список преподов:", font=("Palatino Linotype", 20)).pack(pady=10)

    print_teachers(teachers_window)

    tk.Button(teachers_window, text="Закрыть", command=teachers_window.destroy).pack(pady=10)

def print_bookings(bookings_window):
    query_call_func = "SELECT * FROM print_bookings()"
    try:
        with engine.connect() as connect:
            result = connect.execute(text(query_call_func))
            tk.Label(bookings_window, text=f'ID - КОД - EMAIL - ДАТА ',
                     font=("Palatino Linotype", 15)).pack(pady=5)
            for row in result:
                tk.Label(bookings_window, text=f'{row[0]} - {row[1]} - {row[2]} - {row[3]}',
                         font=("Palatino Linotype", 15)).pack(pady=5)
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        tk.Label(bookings_window, text="Ошибка при загрузке данных", font=("Palatino Linotype", 15)).pack(pady=5)

def show_bookings():
    bookings_window = tk.Toplevel()
    bookings_window.title("Список Покупок")
    bookings_window.geometry("600x800")
    tk.Label(bookings_window, text="Список Покупок:", font=("Palatino Linotype", 20)).pack(pady=10)
    print_bookings(bookings_window)
    tk.Button(bookings_window, text="Закрыть", command=bookings_window.destroy).pack(pady=10)

def open_delete_by_subject():
    def delete_subject():
        subject = subject_entry.get().strip()
        if not subject:
            messagebox.showwarning("Ошибка", "Введите название предмета!")
            return
        try:
            query = "SELECT public.delete_courses_by_subject(:subject);"
            with engine.connect() as connection:
                connection.execute(text(query), {"subject": subject})
                connection.commit()
            messagebox.showinfo("Топчик", f"Курсы по предмету \"{subject}\" успешно удалены!")
            delete_window.destroy()
        except Exception as e:
            print(f"Ошибка при удалении курсов: {e}")
            messagebox.showerror("Ошибка", "Не удалось удалить курсы.")


    delete_window = tk.Toplevel()
    delete_window.title("Удалить курсы по предмету")
    delete_window.geometry("600x400")

    tk.Label(delete_window, text="Введите предмет для удаления курсов(GEO/INF/PE):", font=("Palatino Linotype", 16)).pack(pady=10)
    subject_entry = tk.Entry(delete_window, width=30, font=("Palatino Linotype", 14))
    subject_entry.pack(pady=10)

    tk.Button(delete_window, text="Удалить", font=("Palatino Linotype", 14), command=delete_subject).pack(pady=20)

def open_delete_by_term():
    def delete_term():
        term = term_entry.get().strip()
        if not term.isdigit():
            messagebox.showwarning("Ошибка", "Введите число корректно")
            return
        try:
            query = "SELECT public.delete_courses_with_term(:term);"
            with engine.connect() as connection:
                connection.execute(text(query), {"term": int(term)})
                connection.commit()
            messagebox.showinfo("Топчик", f"Курсы с длительностью \"{term}\" успешно удалены!")
            delete_window.destroy()
        except Exception as e:
            print(f"Ошибка при удалении курсов: {e}")
            messagebox.showerror("Эррор", "Не удалось удалить курсы.")
    delete_window = tk.Toplevel()
    delete_window.title("Удалить курсы по длительности")
    delete_window.geometry("600x400")
    tk.Label(delete_window, text="Введите длительность курса для удаления (3/6/9):", font=("Palatino Linotype", 16)).pack(pady=10)
    term_entry = tk.Entry(delete_window, width=30, font=("Palatino Linotype", 14))
    term_entry.pack(pady=10)
    tk.Button(delete_window, text="Удалить", font=("Palatino Linotype", 14), command=delete_term).pack(pady=20)



def open_admin_panel():
    admin_window = tk.Toplevel()
    admin_window.title("Панель админа")
    admin_window.geometry("1024x1000")

    main_back_img = PhotoImage(file="main_back.png")
    main_back = tk.Label(admin_window, image=main_back_img)
    main_back.place(relwidth=1, relheight=1)
    admin_window.image = main_back_img

    query_revenue = "SELECT * FROM print_total_revenue();"

    try:
        with engine.connect() as connection:
            revenue = connection.execute(text(query_revenue)).fetchone()
            total_revenue = revenue[0]

    except Exception as e:
        total_revenue = "Ошибка"
        print(f"Ошибка при получении дохода: {e}")

    revenue_label = tk.Label(admin_window, text=f"Общий доход: {total_revenue} руб",
                             font=("Palatino Linotype", 18), bg="red", fg="black")
    revenue_label.place(relx=0.33, rely=0.73, anchor="ne")


    tk.Label(admin_window, text="Добро пожаловать, БОСС!", font=("Palatino Linotype", 25), bg="white").pack(pady=20)

    tk.Button(admin_window, text="Добавить студента", font=("Palatino Linotype", 20),
              command=lambda: open_add_student_form(admin_window)).pack(pady=10)
    # Добавляем кнопки для админа
    tk.Button(admin_window, text="Список учеников", font=("Palatino Linotype", 20),
              command=show_users).pack(pady=10)
    tk.Button(admin_window, text="Список Преподов", font=("Palatino Linotype", 20),
              command=show_teachers).pack(pady=10)
    tk.Button(admin_window, text="Список курсов", font=("Palatino Linotype", 20),
              command=show_courses).pack(pady=10)
    tk.Button(admin_window, text="Покупки", font=("Palatino Linotype", 20),
              command=show_bookings).pack(pady=10)
    tk.Button(admin_window, text="Изменить данные", font=("Palatino Linotype", 20),
              command=search_student_by_email_for_edit).pack(pady=10)
    tk.Button(admin_window, text="Удалить по предмету", font=("Palatino Linotype", 20),
              command=open_delete_by_subject).pack(pady=10)
    tk.Button(admin_window, text="Удалить по длительности", font=("Palatino Linotype", 20),
              command=open_delete_by_term).pack(pady=10)
    tk.Button(admin_window, text="Выход", font=("Palatino Linotype", 20), command=admin_window.destroy).pack(pady=10)

def open_add_student_form(admin_window):
    def submit_student_registration():
        email = email_entry.get()
        name = name_entry.get()
        student_class = class_entry.get()
        city = city_entry.get()
        phone = phone_entry.get()

        if all([email, name, student_class, city, phone]):
            try:
                insert_student(email, name, city, phone, student_class)
                add_student_window.destroy()
                messagebox.showinfo("Успешно", "Студент успешно добавлен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении студента: {e}")
        else:
            messagebox.showwarning("Ошибка", "Заполните все поля!")

    add_student_window = tk.Toplevel(admin_window)
    add_student_window.title("Добавить студента")
    add_student_window.geometry("800x600")

    tk.Label(add_student_window, text="Добавление студента", font=("Palatino Linotype", 16)).pack(pady=10)

    tk.Label(add_student_window, text="Email:", font=("Palatino Linotype", 16)).pack(anchor="w", padx=20)
    email_entry = tk.Entry(add_student_window, width=35)
    email_entry.pack(padx=10, pady=10)

    tk.Label(add_student_window, text="ФИО:", font=("Palatino Linotype", 16)).pack(anchor="w", padx=20)
    name_entry = tk.Entry(add_student_window, width=35)
    name_entry.pack(padx=10, pady=10)

    tk.Label(add_student_window, text="Класс:", font=("Palatino Linotype", 16)).pack(anchor="w", padx=20)
    class_entry = tk.Entry(add_student_window, width=35)
    class_entry.pack(padx=10, pady=10)

    tk.Label(add_student_window, text="Город:", font=("Palatino Linotype", 16)).pack(anchor="w", padx=20)
    city_entry = tk.Entry(add_student_window, width=35)
    city_entry.pack(padx=10, pady=10)

    tk.Label(add_student_window, text="Телефон:", font=("Palatino Linotype", 16)).pack(anchor="w", padx=20)
    phone_entry = tk.Entry(add_student_window, width=35)
    phone_entry.pack(padx=10, pady=10)

    tk.Button(add_student_window, text="Добавить студента", font=("Palatino Linotype", 12),
              command=submit_student_registration).pack(pady=10)

def show_users():
    user_window = tk.Toplevel()
    user_window.title("Список учеников")
    user_window.geometry("1200x900")


    tk.Label(user_window, text="Список учеников:", font=("Palatino Linotype", 20)).pack(pady=10)

    city_label = tk.Label(user_window, text="Введите город для поиска:", font=("Palatino Linotype", 14))
    city_label.pack(pady=5)

    city_entry = tk.Entry(user_window, font=("Palatino Linotype", 14), width=30)
    city_entry.pack(pady=5)

    frame = tk.Frame(user_window)
    frame.pack(fill="both", expand=True)


    def search_by_city():
        city = city_entry.get().strip()
        open_city_window(city)

    search_button = tk.Button(user_window, text="Поиск", font=("Palatino Linotype", 14), command=search_by_city)
    search_button.pack(pady=10)


    print_students(user_window)

    tk.Button(user_window, text="Закрыть", command=user_window.destroy).pack(pady=10)



def open_course_signup(email):
    def enroll_course():
        course_code = course_code_entry.get().strip()
        if not course_code:
            messagebox.showwarning("Ошибка", "Введите код курса!")
            return

        try:
            query = "SELECT public.insert_into_bookings(:course_code, :email);"
            with engine.connect() as connection:
                with connection.begin():
                    result = connection.execute(text(query), {"course_code": course_code, "email": email})
                    connection.commit()


            messagebox.showinfo("Успех", "Вы успешно записались на курс!")
            signup_window.destroy()
        except Exception as e:
            print(f"Ошибка при записи на курс: {e}")
            messagebox.showerror("Ошибка", "Не удалось записаться на курс.")

    signup_window = tk.Toplevel()
    signup_window.title("Записаться на курс")
    signup_window.geometry("600x400")

    tk.Label(signup_window, text="Введите код курса для записи:", font=("Palatino Linotype", 16)).pack(pady=10)
    course_code_entry = tk.Entry(signup_window, width=30, font=("Palatino Linotype", 14))
    course_code_entry.pack(pady=10)

    tk.Button(signup_window, text="Записаться", font=("Palatino Linotype", 14), command=enroll_course).pack(pady=20)

def open_city_window(city):
    city_window = tk.Toplevel()
    city_window.title(f"Ученики из города {city}")
    city_window.geometry("600x400")

    tk.Label(city_window, text=f"Ученики из города {city}:", font=("Palatino Linotype", 20)).pack(pady=10)

    query_call_func = "SELECT * FROM print_students_from(:city)"

    try:
        with engine.connect() as connect:
            result = connect.execute(text(query_call_func), {"city": city})

            if result.rowcount == 0:
                tk.Label(city_window, text="Нет студентов из этого города.", font=("Palatino Linotype", 15)).pack(
                    pady=5)
            else:
                tk.Label(city_window, text=f'EMAIL - ФИО - ГОРОД - ТЕЛЕФОН - КЛАСС',
                         font=("Palatino Linotype", 15)).pack(pady=5)
                for row in result:
                    tk.Label(city_window, text=f'{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}',
                             font=("Palatino Linotype", 15)).pack(pady=5)
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        tk.Label(city_window, text="Ошибка при загрузке данных", font=("Palatino Linotype", 15)).pack(pady=5)

    tk.Button(city_window, text="Закрыть", command=city_window.destroy).pack(pady=10)

def show_courses():
    courses_window = tk.Toplevel()
    courses_window.title("Список курсов")
    courses_window.geometry("600x900")

    tk.Label(courses_window, text="Список курсов:", font=("Palatino Linotype", 20)).pack(pady=10)

    print_courses(courses_window)

    tk.Button(courses_window, text="Закрыть", command=courses_window.destroy).pack(pady=10)


def registration_form(email):
    def submit_registration():
        name = name_entry.get()
        user_class = class_entry.get()
        city = city_entry.get()
        phone = phone_entry.get()

        if not user_class.isdigit() or not phone.isdigit():
            messagebox.showwarning("Ошибка", "класс и телефон числа")
            return
        if all([name, user_class, city, phone]):
            try:
                insert_student(email, name, city, phone, user_class)
                reg_window.destroy()
                messagebox.showinfo("Успешно", "Регистрация завершена!")
                open_personal_account(email)
            except Exception as e:
                print(f"Ошибка регистрации: {e}")
                messagebox.showerror("Ошибка", "Произошла ошибка при регистрации.")
        else:
            messagebox.showwarning("Ошибка", "Заполните все поля!")

    reg_window = tk.Toplevel()
    reg_window.title("Регистрация")
    reg_window.geometry("800x600")


    tk.Label(reg_window, text='Регистрация', font=("Palatino Linotype", 16)).pack(pady=10)

    tk.Label(reg_window, text='ФИО:', font=("Palatino Linotype", 16)).pack(anchor="w", padx=20)
    name_entry = tk.Entry(reg_window, width=35)
    name_entry.pack(padx=10, pady=10)

    tk.Label(reg_window, text='Класс:', font=("Palatino Linotype", 16)).pack(anchor="w", padx=10)
    class_entry = tk.Entry(reg_window, width=35)
    class_entry.pack(padx=10, pady=10)

    tk.Label(reg_window, text='Город:', font=("Palatino Linotype", 16)).pack(anchor="w", padx=10)
    city_entry = tk.Entry(reg_window, width=35)
    city_entry.pack(padx=10, pady=10)

    tk.Label(reg_window, text='Телефон:', font=("Palatino Linotype", 16)).pack(anchor="w", padx=10)
    phone_entry = tk.Entry(reg_window, width=35)
    phone_entry.pack(padx=10, pady=10)

    tk.Button(reg_window, text='Зарегистрироваться', font=("Palatino Linotype", 12),
              command=submit_registration).pack(pady=10)

def open_code_window():
    global code_window, code_entry
    code_window = tk.Toplevel(login_window)
    code_window.title("Введите код")
    code_window.geometry("500x300")

    it_cats_img = PhotoImage(file="it_cats.png")
    back_verify = tk.Label(code_window, image=it_cats_img)
    back_verify.place(relwidth=1, relheight=1)

    tk.Label(code_window, text="Введите код, отправленный на почту:", font=("Palatino Linotype", 16)).pack(pady=10)
    code_entry = tk.Entry(code_window, width=20, font=("Palatino Linotype", 16))
    code_entry.pack(pady=10)
    tk.Button(code_window, text="Подтвердить", command=verify_code, font=("Palatino Linotype", 20)).pack(pady=10)

    code_window.image = it_cats_img


def open_user_info(name, email, user_class, city, phone):
    info_window = tk.Toplevel(personal_window)
    info_window.title("Информация о себе")
    info_window.geometry("600x1000")

    tk.Label(info_window, text="Информация о пользователе:", font=("Palatino Linotype", 20)).pack(pady=20)
    tk.Label(info_window, text=f"Имя: {name}\nEmail: {email}\nКласс: {user_class}\nГород: {city}\nТелефон: {phone}",
             font=("Palatino Linotype", 15)).pack(pady=20)
    tk.Button(info_window, text="Закрыть", command=info_window.destroy).pack(pady=10)





def open_my_courses(email):
    courses_window = tk.Toplevel(personal_window)
    courses_window.title("Мои курсы")
    courses_window.geometry("600x600")

    query = "SELECT * FROM public.print_bookings() WHERE email = :email;"
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), {"email": email})

            for row in result:
                tk.Label(courses_window, text=f"Курс: {row[1]} - Дата записи: {row[3]}",
                         font=("Palatino Linotype", 14)).pack(pady=5)
    except Exception as e:
        tk.Label(courses_window, text="Ошибка при загрузке курсов.", font=("Palatino Linotype", 14)).pack(pady=10)

    tk.Button(courses_window, text="Закрыть", command=courses_window.destroy).pack(pady=10)


def open_personal_account(email):
    global personal_window
    personal_window = tk.Toplevel()
    personal_window.title("Личный кабинет")
    personal_window.geometry("1024x680")

    query_get_student = "SELECT * FROM public.print_student_by_email(:email);"
    try:
        with engine.connect() as connection:
            student_data = connection.execute(text(query_get_student), {"email": email}).fetchone()

        if not student_data:
            messagebox.showerror("Ошибка", "Не удалось загрузить данные пользователя.")
            personal_window.destroy()
            return

        name, city, phone, user_class = student_data[1], student_data[2], student_data[3], student_data[4]

    except Exception as e:
        messagebox.showerror("Ошибка", "Произошла ошибка при загрузке данных.")
        personal_window.destroy()
        return


    main_back_img = PhotoImage(file="main_back.png")
    main_back = tk.Label(personal_window, image=main_back_img)
    main_back.place(relwidth=1, relheight=1)
    personal_window.image = main_back_img

    info_button = tk.Button(personal_window, text="Информация о себе", font=("Palatino Linotype", 15),
                            command=lambda: open_user_info(name, email, user_class, city, phone))
    info_button.place(x=700, y=20)

    signup_button = tk.Button(personal_window, text="Записаться на курс", font=("Palatino Linotype", 20),
                               command= lambda:open_course_signup(email))
    signup_button.place(relx=0.05, rely=0.5, anchor="w", width=250, height=50)

    avaiable_courses_button = tk.Button(personal_window, text="Доступные курсы", font=("Palatino Linotype", 20),
                               command= lambda:show_courses())

    avaiable_courses_button.place(relx=0.35, rely=0.5, anchor="w", width=250, height=50)

    courses_button = tk.Button(personal_window, text="Мои курсы", font=("Palatino Linotype", 20),
                                command=lambda :open_my_courses(email))
    courses_button.place(relx=0.95, rely=0.5, anchor="e", width=250, height=50)

login_window = tk.Tk()
login_window.title("Вход/Регистрация")
login_window.geometry("800x600")

back_img = PhotoImage(file="back.png")
background_login = tk.Label(login_window, image=back_img)
background_login.place(relwidth=1, relheight=1)

tk.Label(login_window, text="Введите email:", font=("Palatino Linotype", 20)).pack(pady=10)
email_entry = tk.Entry(login_window, width=30, font=("Palatino Linotype", 20))
email_entry.pack(pady=5)
tk.Button(login_window, text="Войти", font=("Palatino Linotype", 20), command=open_code_window).pack(pady=10)

login_window.mainloop()
