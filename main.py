import typer
import secrets
import string
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
import os

from art import text2art

app = typer.Typer()
console = Console()

def generate_password(length: int = 16, character_set: str = None) -> str:
    """
    Генерирует случайный пароль заданной длины.

    Args:
        length: Длина пароля (по умолчанию 16)
        character_set: Набор символов для генерации пароля (по умолчанию string.ascii_letters + string.punctuation без проблемных символов)

    Returns:
        Сгенерированный пароль
    """
    if character_set is None:
        # Используем только английские буквы (верхний и нижний регистр) и специальные символы
        characters = string.ascii_letters + string.punctuation
        # Исключаем потенциально проблемные символы, такие как пробелы
        exclude_chars = " '`\"\\\t\n\r"
        filtered_characters = ''.join(c for c in characters if c not in exclude_chars)
    else:
        filtered_characters = character_set

    password = ''.join(secrets.choice(filtered_characters) for _ in range(length))
    return password

def show_menu():
    """Отображает главное меню приложения."""
    
    
    while True:
        # Очищаем терминал перед отображением меню
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Генерируем ASCII-арт для слова "TEST"
        ascii_art = text2art("PassWDGenerator", font="small")
        
        # Создаем текстовый объект для ASCII-арта
        ascii_text = Text(ascii_art, justify="left")
        ascii_text.stylize("bold magenta", 0, len(ascii_text))
        
        # Отображаем ASCII-арт слева
        console.print(ascii_text)
        
        # Отображаем меню
        menu_text = Text()
        menu_text.append("1. Сделать пароль\n", style="bold")
        menu_text.append("0. Выйти\n", style="bold")
        
        menu_panel = Panel(
            menu_text,
            title="[bold magenta]Меню[/bold magenta]",
            border_style="magenta",
            width=50  # Устанавливаем фиксированную ширину для предотвращения проблем с изменением размера окна
        )
        console.print(menu_panel)
        
        # Получаем выбор пользователя
        choice = Prompt.ask(
            "[bold magenta]Выберите действие[/bold magenta]",
            choices=["1", "0"],
            default="1"
        )
        
        if choice == "1":
            # Предлагаем пользователю выбрать: один пароль или несколько
            sub_choice = Prompt.ask(
                "[bold magenta]Выберите: 1 - один пароль, много - несколько паролей, 0 - назад[/bold magenta]",
                choices=["1", "много", "0"],
                default="1",
                show_choices=False
            )
            
            if sub_choice == "1":
                # Генерируем и отображаем один пароль
                password = generate_password()
                console.print(Panel(
                    password,
                    title="[bold magenta]Сгенерированный пароль[/bold magenta]",
                    border_style="magenta",
                    padding=(1, 2),
                    width=50  # Устанавливаем фиксированную ширину для предотвращения проблем с изменением размера окна
                ))
                
                # Ждем, пока пользователь нажмет Enter, чтобы вернуться в меню
                console.input("\n[bold magenta]Нажмите Enter, чтобы вернуться в меню...[/bold magenta]")
                
            elif sub_choice == "много":
                # Спрашиваем, сколько паролей сгенерировать
                # Создаем список допустимых значений
                valid_choices = [str(i) for i in range(1, 11)]
                
                while True:
                    try:
                        count_input = Prompt.ask(
                            "[bold magenta]Сколько паролей сгенерировать? (1-10)[/bold magenta]",
                            default="3",
                            choices=valid_choices
                        )
                        
                        count = int(count_input.strip())
                        break  # Выходим из цикла, если ввод корректен
                    except ValueError:
                        console.print("[bold red]Пожалуйста, введите число от 1 до 10.[/bold red]")
                        continue
                
                # Генерируем и отображаем несколько паролей
                passwords = []
                for i in range(count):
                    password = generate_password()
                    passwords.append(password)
                
                # Отображаем пароли компактно
                for i, password in enumerate(passwords, 1):
                    console.print(Panel(
                        f"[bold]{password}[/bold]", 
                        title=f"[bold magenta]Пароль #{i}[/bold magenta]", 
                        border_style="magenta",
                        padding=(0, 1),
                        width=50  # Устанавливаем фиксированную ширину для предотвращения проблем с изменением размера окна
                    ))
                
                # Ждем, пока пользователь нажмет Enter, чтобы вернуться в меню
                console.input("\n[bold magenta]Нажмите Enter, чтобы вернуться в меню...[/bold magenta]")
                
            elif sub_choice == "0":
                continue  # Возвращаемся в главное меню
                
        elif choice == "0":
            console.print("[bold magenta]До свидания![/bold magenta]")
            break

@app.command()
def generate(
    length: int = typer.Option(16, "--length", "-l", min=4, max=128, help="Длина пароля (минимум 4, максимум 128)"),
    count: int = typer.Option(1, "--count", "-c", min=1, max=10, help="Количество паролей для генерации (минимум 1, максимум 10)"),
    include_digits: bool = typer.Option(True, "--include-digits/--no-digits", help="Включать цифры в пароль"),
    include_punctuation: bool = typer.Option(True, "--include-punct/--no-punct", help="Включать знаки препинания в пароль"),
    exclude_ambiguous: bool = typer.Option(False, "--exclude-ambiguous/--include-ambiguous", help="Исключить неоднозначные символы (l, 1, I, O, 0)")
):
    """
    Генерирует безопасный пароль.

    По умолчанию создает один пароль длиной 16 символов,
    состоящий из английских букв (верхний и нижний регистр) и специальных символов.
    """
    if length < 4:
        typer.echo("Длина пароля должна быть не менее 4 символов для обеспечения безопасности.")
        raise typer.Exit(code=1)

    if count < 1:
        typer.echo("Количество паролей должно быть не менее 1.")
        raise typer.Exit(code=1)

    # Формируем набор символов на основе параметров
    character_set = string.ascii_letters  # Всегда включаем буквы
    
    if include_digits:
        character_set += string.digits
        
    if include_punctuation:
        character_set += string.punctuation
        # Исключаем потенциально проблемные символы
        exclude_chars = " '`\"\\\t\n\r"
        character_set = ''.join(c for c in character_set if c not in exclude_chars)
    
    if exclude_ambiguous:
        # Исключаем неоднозначные символы
        ambiguous_chars = "l1IO0"
        character_set = ''.join(c for c in character_set if c not in ambiguous_chars)

    for i in range(count):
        password = generate_password(length, character_set)
        console.print(Panel(
            password,
            title=f"[bold magenta]Пароль #{i+1}[/bold magenta]",
            border_style="magenta",
            padding=(1, 2),
            width=50  # Устанавливаем фиксированную ширину для предотвращения проблем с изменением размера окна
        ))

@app.command()
def interactive():
    """
    Интерактивный режим генерации паролей.
    """
    length = typer.prompt(
        "Введите длину пароля",
        type=int,
        default=16,
        show_default=True
    )

    if length < 4:
        typer.echo("Длина пароля должна быть не менее 4 символов для обеспечения безопасности.")
        raise typer.Exit(code=1)

    count = typer.prompt(
        "Введите количество паролей",
        type=int,
        default=1,
        show_default=True
    )

    if count < 1 or count > 10:
        typer.echo("Количество паролей должно быть от 1 до 10.")
        raise typer.Exit(code=1)

    include_digits = typer.confirm("Включить цифры?", default=True)
    include_punctuation = typer.confirm("Включить знаки препинания?", default=True)
    exclude_ambiguous = typer.confirm("Исключить неоднозначные символы (l, 1, I, O, 0)?", default=False)

    # Формируем набор символов на основе параметров
    character_set = string.ascii_letters  # Всегда включаем буквы
    
    if include_digits:
        character_set += string.digits
        
    if include_punctuation:
        character_set += string.punctuation
        # Исключаем потенциально проблемные символы
        exclude_chars = " '`\"\\\t\n\r"
        character_set = ''.join(c for c in character_set if c not in exclude_chars)
    
    if exclude_ambiguous:
        # Исключаем неоднозначные символы
        ambiguous_chars = "l1IO0"
        character_set = ''.join(c for c in character_set if c not in ambiguous_chars)

    for i in range(count):
        password = generate_password(length, character_set)
        console.print(Panel(
            password,
            title=f"[bold magenta]Пароль #{i+1}[/bold magenta]",
            border_style="magenta",
            padding=(1, 2),
            width=50  # Устанавливаем фиксированную ширину для предотвращения проблем с изменением размера окна
        ))

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    TUI генератор паролей.
    
    Генерирует безопасные пароли из английских букв (верхний и нижний регистр) и специальных символов.
    """
    if ctx.invoked_subcommand is None:
        # Если команда не указана, показываем меню
        show_menu()

if __name__ == "__main__":
    app()