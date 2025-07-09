import os
import requests
import psutil
import GPUtil

# ASCII арт —
ASCII_ART = r"""
                _..._
              .'     '.      _
             /    .-""-\   _/ \   ||Open-Space Monitor||
           .-|   /:.   |  |   |   ||by 1nspect0r1     ||
           |  \  |:.   /.-'-./
           | .-'-;:__.'    =/
           .'=  *=|     _.='
          /   _.  |    ;
         ;-.-'|    \   |
        /   | \    _\  _\
        \__/'._;.  ==' ==\
                 \    \   |
                 /    /   /
                 /-._/-._/
                 \   `\  \
                  `-._/._/
"""

def get_temperature(city, api_key):
    """
    Получает текущую температуру в указанном городе через OpenWeatherMap API.
    :param city: название города (строка)
    :param api_key: API ключ OpenWeatherMap (строка)
    :return: температура в градусах Цельсия (float) или None при ошибке
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        # Проверяем, что ключ 'main' и 'temp' существуют в ответе
        if 'main' in data and 'temp' in data['main']:
            temp = data['main']['temp']
            return temp
        else:
            return None # Некорректный ответ API
    except requests.exceptions.RequestException as e:
        # Обработка ошибок сетевого запроса
        print(f"Ошибка при запросе к API: {e}")
        return None
    except Exception as e:
        # Обработка других возможных ошибок (например, парсинг JSON)
        print(f"Произошла ошибка: {e}")
        return None

def get_cpu_load():
    """
    Получает текущую загрузку CPU в процентах.
    :return: загрузка CPU (float)
    """
    return psutil.cpu_percent(interval=1)

def get_gpu_load():
    """
    Получает текущую загрузку всех доступных GPU в процентах.
    :return: список загрузок GPU (list of float) или None, если GPU не обнаружены
    """
    gpus = GPUtil.getGPUs()
    if not gpus:
        return None
    gpu_loads = [gpu.load * 100 for gpu in gpus]
    return gpu_loads

def main():
    # Ваш API ключ OpenWeatherMap — замените на свой ключ
    # Получить ключ можно на сайте: https://openweathermap.org/api
    API_KEY = "ВАШ_API_КЛЮЧ"

    # Очистка консоли для операционных систем Windows ('cls') или Linux/macOS ('clear')
    os.system('cls' if os.name == 'nt' else 'clear')

    # Вывод ASCII-арта космонавта
    print(ASCII_ART)

    # Запрос города у пользователя. Метод .strip() удаляет пробелы в начале и конце строки.
    # Если пользователь ничего не введет, используется город по умолчанию "Krasnodar".
    city = input("Введите название города для получения температуры (по умолчанию Краснодар): ").strip()
    if not city:
        city = "Krasnodar"

    print(f"\nДобро пожаловать в открытый космос!\n")

    # Получение и вывод температуры для выбранного города
    temp = get_temperature(city, API_KEY)
    if temp is not None:
        # .title() делает первую букву каждого слова заглавной (например, "moscow" -> "Moscow")
        print(f"Температура за бортом ({city.title()}): {temp:.1f} °C")
    else:
        print(f"Не удалось получить температуру для города {city.title()}. Проверьте название города или API-ключ.")

    # Получение и вывод загрузки CPU
    cpu_load = get_cpu_load()
    print(f"Нагрузка CPU: {cpu_load:.1f}%")

    # Получение и вывод загрузки GPU
    gpu_loads = get_gpu_load()
    if gpu_loads is None:
        print("GPU не обнаружен или данные недоступны.")
    else:
        # Выводим нагрузку для каждой обнаруженной GPU
        for i, load in enumerate(gpu_loads):
            print(f"Нагрузка GPU #{i+1}: {load:.1f}%")

    # Ожидание нажатия Enter перед закрытием консоли, чтобы пользователь успел прочитать информацию
    print("\nНажмите Enter для выхода...")
    input()

# Точка входа в программу: убеждаемся, что main() вызывается только при прямом запуске скрипта
if __name__ == "__main__":
    main()
