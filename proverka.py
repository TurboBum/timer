import subprocess
import psutil
import time

def monitor_process(process_name):
    while True:
        # Поиск процесса по имени
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                print(f"{process_name} работает.")
                break
        else:
            print(f"{process_name} завершился. Перезапускаем...")
            # Перезапуск вашего приложения
            subprocess.Popen(['python', 'main.py'])
        
        time.sleep(5)  # Проверка каждые 5 секунд

if __name__ == "__main__":
    monitor_process('Python')  # Укажите здесь имя вашего приложения
