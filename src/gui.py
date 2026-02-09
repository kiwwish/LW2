# gui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tritimus import TrithemusCipher
from polyTritimus import PolyalphabeticTrithemus


class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифр Тритемуса")
        self.root.geometry("900x850")

        # Создаём вкладки
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Вкладка 1: Простой шифр Тритемуса
        self.frame_simple = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_simple, text='Простой шифр Тритемуса')
        self.setup_simple_tab()

        # Вкладка 2: Полиалфавитный шифр Тритемуса
        self.frame_poly = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_poly, text='Полиалфавитный шифр Тритемуса')
        self.setup_poly_tab()

    def setup_simple_tab(self):
        """Настройка вкладки простого шифра Тритемуса"""
        # Область для таблицы
        frame_table = ttk.LabelFrame(self.frame_simple, text="Таблица замены", padding=10)
        frame_table.pack(fill='x', padx=10, pady=(10, 5))

        ttk.Label(frame_table, text="Ключ для таблицы:").grid(row=0, column=0, sticky='w', pady=5)
        self.key_entry = ttk.Entry(frame_table, width=50)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_table, text="Построить таблицу", command=self.show_table).grid(row=0, column=2, padx=5)

        ttk.Label(frame_table, text="Таблица:").grid(row=1, column=0, sticky='w', pady=5)
        self.table_text = tk.Text(frame_table, height=2, width=70, state='disabled', bg='#f0f0f0')
        self.table_text.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='w')

        # Область шифрования
        frame_encrypt = ttk.LabelFrame(self.frame_simple, text="Шифрование", padding=10)
        frame_encrypt.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_encrypt, text="Текст для шифрования:").grid(row=0, column=0, sticky='w', pady=5)
        self.text_encrypt = scrolledtext.ScrolledText(frame_encrypt, height=5, width=70)
        self.text_encrypt.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_encrypt, text="Зашифровать", command=self.encrypt_text).grid(row=1, column=1, pady=10,
                                                                                      sticky='w')

        ttk.Label(frame_encrypt, text="Результат:").grid(row=2, column=0, sticky='w', pady=5)
        self.result_encrypt = scrolledtext.ScrolledText(frame_encrypt, height=5, width=70)
        self.result_encrypt.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_encrypt, text="Копировать шифр", command=self.copy_cipher).grid(row=3, column=1, pady=5,
                                                                                         sticky='w')

        # Область дешифрования
        frame_decrypt = ttk.LabelFrame(self.frame_simple, text="Дешифрование", padding=10)
        frame_decrypt.pack(fill='x', padx=10, pady=(5, 10))

        ttk.Label(frame_decrypt, text="Шифр для расшифровки:").grid(row=0, column=0, sticky='w', pady=5)
        self.text_decrypt = scrolledtext.ScrolledText(frame_decrypt, height=5, width=70)
        self.text_decrypt.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_decrypt, text="Вставить из буфера", command=self.paste_cipher).grid(row=1, column=1, pady=5,
                                                                                             sticky='w')
        ttk.Button(frame_decrypt, text="Расшифровать", command=self.decrypt_text).grid(row=2, column=1, pady=10,
                                                                                       sticky='w')

        ttk.Label(frame_decrypt, text="Результат:").grid(row=3, column=0, sticky='w', pady=5)
        self.result_decrypt = scrolledtext.ScrolledText(frame_decrypt, height=5, width=70)
        self.result_decrypt.grid(row=3, column=1, padx=5, pady=5)

    def setup_poly_tab(self):
        """Настройка вкладки полиалфавитного шифра Тритемуса"""
        # Область для ключа
        frame_key = ttk.LabelFrame(self.frame_poly, text="Ключ", padding=10)
        frame_key.pack(fill='x', padx=10, pady=(10, 5))

        ttk.Label(frame_key, text="Ключ (текст):").grid(row=0, column=0, sticky='w', pady=5)
        self.poly_key_entry = ttk.Entry(frame_key, width=60)
        self.poly_key_entry.grid(row=0, column=1, padx=5, pady=5)

        # Область шифрования
        frame_encrypt = ttk.LabelFrame(self.frame_poly, text="Шифрование", padding=10)
        frame_encrypt.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_encrypt, text="Текст для шифрования:").grid(row=0, column=0, sticky='w', pady=5)
        self.poly_text_encrypt = scrolledtext.ScrolledText(frame_encrypt, height=5, width=70)
        self.poly_text_encrypt.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_encrypt, text="Зашифровать", command=self.poly_encrypt_text).grid(row=1, column=1, pady=10,
                                                                                           sticky='w')

        ttk.Label(frame_encrypt, text="Результат:").grid(row=2, column=0, sticky='w', pady=5)
        self.poly_result_encrypt = scrolledtext.ScrolledText(frame_encrypt, height=5, width=70)
        self.poly_result_encrypt.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_encrypt, text="Копировать шифр", command=self.poly_copy_cipher).grid(row=3, column=1, pady=5,
                                                                                              sticky='w')

        # Область дешифрования
        frame_decrypt = ttk.LabelFrame(self.frame_poly, text="Дешифрование", padding=10)
        frame_decrypt.pack(fill='x', padx=10, pady=(5, 10))

        ttk.Label(frame_decrypt, text="Шифр для расшифровки:").grid(row=0, column=0, sticky='w', pady=5)
        self.poly_text_decrypt = scrolledtext.ScrolledText(frame_decrypt, height=5, width=70)
        self.poly_text_decrypt.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_decrypt, text="Вставить из буфера", command=self.poly_paste_cipher).grid(row=1, column=1,
                                                                                                  pady=5, sticky='w')
        ttk.Button(frame_decrypt, text="Расшифровать", command=self.poly_decrypt_text).grid(row=2, column=1, pady=10,
                                                                                            sticky='w')

        ttk.Label(frame_decrypt, text="Результат:").grid(row=3, column=0, sticky='w', pady=5)
        self.poly_result_decrypt = scrolledtext.ScrolledText(frame_decrypt, height=5, width=70)
        self.poly_result_decrypt.grid(row=3, column=1, padx=5, pady=5)

    # ========== МЕТОДЫ ДЛЯ ПРОСТОГО ШИФРА ==========

    def show_table(self):
        """Показать таблицу замены для введённого ключа"""
        key = self.key_entry.get().strip().upper()
        if not key:
            messagebox.showerror("Ошибка", "Введите ключ")
            return

        cipher = TrithemusCipher(key)
        table = cipher.get_table()

        self.table_text.config(state='normal')
        self.table_text.delete(1.0, tk.END)
        self.table_text.insert(1.0, table)
        self.table_text.config(state='disabled')

        # Также покажем стандартный алфавит для сравнения
        standard = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_"
        messagebox.showinfo("Таблица замены",
                            f"Стандартный алфавит:\n{standard}\n\n"
                            f"Таблица по ключу '{key}':\n{table}")

    def encrypt_text(self):
        """Зашифровать текст простым шифром"""
        key = self.key_entry.get().strip().upper()
        text = self.text_encrypt.get("1.0", tk.END).strip().upper()

        if not key:
            messagebox.showerror("Ошибка", "Введите ключ")
            return
        if not text:
            messagebox.showerror("Ошибка", "Введите текст для шифрования")
            return

        cipher = TrithemusCipher(key)
        encrypted = cipher.encrypt(text)

        self.result_encrypt.delete("1.0", tk.END)
        self.result_encrypt.insert("1.0", encrypted)

    def decrypt_text(self):
        """Расшифровать текст простым шифром"""
        key = self.key_entry.get().strip().upper()
        cipher_text = self.text_decrypt.get("1.0", tk.END).strip().upper()

        if not key:
            messagebox.showerror("Ошибка", "Введите ключ")
            return
        if not cipher_text:
            messagebox.showerror("Ошибка", "Введите шифр для расшифровки")
            return

        cipher = TrithemusCipher(key)
        decrypted = cipher.decrypt(cipher_text)

        self.result_decrypt.delete("1.0", tk.END)
        self.result_decrypt.insert("1.0", decrypted)

    def copy_cipher(self):
        """Копировать результат шифрования в буфер"""
        cipher = self.result_encrypt.get("1.0", tk.END).strip()
        if cipher:
            self.root.clipboard_clear()
            self.root.clipboard_append(cipher)
            messagebox.showinfo("Скопировано", "Шифр скопирован в буфер обмена")

    def paste_cipher(self):
        """Вставить текст из буфера в поле дешифрования"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.text_decrypt.delete("1.0", tk.END)
            self.text_decrypt.insert("1.0", clipboard_text)
        except:
            messagebox.showwarning("Ошибка", "Не удалось получить текст из буфера")

    # ========== МЕТОДЫ ДЛЯ ПОЛИАЛФАВИТНОГО ШИФРА ==========

    def poly_encrypt_text(self):
        """Зашифровать текст полиалфавитным шифром"""
        key = self.poly_key_entry.get().strip().upper()
        text = self.poly_text_encrypt.get("1.0", tk.END).strip().upper()

        if not key:
            messagebox.showerror("Ошибка", "Введите ключ")
            return
        if not text:
            messagebox.showerror("Ошибка", "Введите текст для шифрования")
            return

        try:
            cipher = PolyalphabeticTrithemus(key)
            encrypted = cipher.encrypt(text)

            self.poly_result_encrypt.delete("1.0", tk.END)
            self.poly_result_encrypt.insert("1.0", encrypted)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка шифрования: {str(e)}")

    def poly_decrypt_text(self):
        """Расшифровать текст полиалфавитным шифром"""
        key = self.poly_key_entry.get().strip().upper()
        cipher_text = self.poly_text_decrypt.get("1.0", tk.END).strip().upper()

        if not key:
            messagebox.showerror("Ошибка", "Введите ключ")
            return
        if not cipher_text:
            messagebox.showerror("Ошибка", "Введите шифр для расшифровки")
            return

        try:
            cipher = PolyalphabeticTrithemus(key)
            decrypted = cipher.decrypt(cipher_text)

            self.poly_result_decrypt.delete("1.0", tk.END)
            self.poly_result_decrypt.insert("1.0", decrypted)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка дешифрования: {str(e)}")

    def poly_copy_cipher(self):
        """Копировать результат полиалфавитного шифрования"""
        cipher = self.poly_result_encrypt.get("1.0", tk.END).strip()
        if cipher:
            self.root.clipboard_clear()
            self.root.clipboard_append(cipher)
            messagebox.showinfo("Скопировано", "Шифр скопирован в буфер обмена")

    def poly_paste_cipher(self):
        """Вставить текст из буфера в поле дешифрования"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.poly_text_decrypt.delete("1.0", tk.END)
            self.poly_text_decrypt.insert("1.0", clipboard_text)
        except:
            messagebox.showwarning("Ошибка", "Не удалось получить текст из буфера")


def main():
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()