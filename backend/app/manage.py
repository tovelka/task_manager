import sys
from pathlib import Path
from alembic.config import Config
from alembic import command
import uvicorn
from dotenv import load_dotenv


load_dotenv(Path(__file__).parent.parent / '.env')


def run_makemigration(message):
    alembic_ini = Path(__file__).parent / 'alembic.ini'
    if not alembic_ini.exists():
        print(f'Ошибка: {alembic_ini} не найден')
        sys.exit(1)
    alembic_cfg = Config(str(alembic_ini))
    command.revision(alembic_cfg, autogenerate=True, message=message)
    print(f"Миграция '{message}' создана")


def run_migrate():
    alembic_ini = Path(__file__).parent / 'alembic.ini'
    if not alembic_ini.exists():
        print(f'Ошибка: {alembic_ini} не найден')
        sys.exit(1)
    alembic_cfg = Config(str(alembic_ini))
    command.upgrade(alembic_cfg, 'head')
    print('Миграции применены')


def run_server():
    uvicorn.run(
        'app.main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        run_server()
    elif args[0] == '--makemigration':
        if len(args) < 2:
            print("Укажите сообщение: --makemigration 'описание'")
            sys.exit(1)
        run_makemigration(args[1])
    elif args[0] == '--migrate':
        run_migrate()
    else:
        print(
            'Неизвестная команда. Доступно: --makemigration, --migrate, (без аргументов - запуск сервера)'
        )
        sys.exit(1)
