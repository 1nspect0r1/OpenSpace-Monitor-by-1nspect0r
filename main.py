import os
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
    # Очистка консоли для операционных систем Windows ('cls') или Linux/macOS ('clear')
    os.system('cls' if os.name == 'nt' else 'clear')

    # Вывод ASCII-арта космонавта
    print(ASCII_ART)

    print(f"\nДобро пожаловать в открытый космос!\n")

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

if __name__ == "__main__":
    main()
