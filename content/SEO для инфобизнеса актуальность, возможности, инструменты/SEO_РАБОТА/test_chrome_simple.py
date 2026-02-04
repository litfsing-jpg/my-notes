import undetected_chromedriver as uc

print("1. Создание опций...")
options = uc.ChromeOptions()

print("2. Инициализация драйвера...")
driver = uc.Chrome(options=options)

print("3. Открытие Google...")
driver.get("https://google.com")

import time
time.sleep(3)

print(f"4. Заголовок: {driver.title}")

print("5. Закрытие...")
driver.quit()

print("✅ Тест пройден!")
