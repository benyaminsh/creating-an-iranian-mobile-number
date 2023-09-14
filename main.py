from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random


count = int(input('Number of numbers required : '))

print('\nStart...')

file = open('numbers.txt', 'w+')


def generate_iranian_phone_numbers(num):
    valid_prefixes = ['0912', '0930', '0901', '0902', '0918', '0910', '0933', '0990']
    phone_numbers = []

    for _ in range(num):
        is_valid = False
        while not is_valid:
            prefix = random.choice(valid_prefixes)
            phone_number = prefix
            for _ in range(7):
                phone_number += str(random.randint(0, 9))

            is_valid = validate_iranian_phone_number(phone_number)

        phone_numbers.append(phone_number)

    return phone_numbers


def validate_iranian_phone_number(phone_number):
    if len(phone_number) != 11:
        return False

    if phone_number[:2] != '09':
        return False

    return True


def check_telegram_user(phone_number):
    driver = webdriver.Firefox()
    try:
        driver.get('https://web.telegram.org/k/')
        sleep(5)
        driver.find_element(By.CSS_SELECTOR,
                            '#auth-pages > div > div.tabs-container.auth-pages__container > div.tabs-tab.page-signQR.active > div > div.input-wrapper > button').send_keys(
            Keys.ENTER)
        sleep(2)
        number_input = driver.find_element(By.CSS_SELECTOR,
                                           '#auth-pages > div > div.tabs-container.auth-pages__container > div.tabs-tab.page-sign.active > div > div.input-wrapper > div.input-field.input-field-phone > div.input-field-input')
        number_input.clear()
        number_input.send_keys(f"+98{phone_number[1:]}")

        next_button = driver.find_element(By.CSS_SELECTOR,
                                          '#auth-pages > div > div.tabs-container.auth-pages__container > div.tabs-tab.page-sign.active > div > div.input-wrapper > button.btn-primary.btn-color-primary.rp').click()
        sleep(2)
        try:
            get_error = driver.find_element(By.CSS_SELECTOR,
                                            '#auth-pages > div > div.tabs-container.auth-pages__container > div.tabs-tab.page-sign.active > div > div.input-wrapper > div.input-field.input-field-phone > label > span').get_attribute(
                'textContent')
            if get_error == 'Phone Number Invalid':
                sleep(1)
                driver.close()
                return False
            elif get_error == 'Code':
                sleep(1)
                driver.close()
                return True
            else:
                driver.close()
                return True
        except:
            pass

        driver.close()
        return True
    except:
        driver.close()
        return False


numbers = []
flash_count = 0
random_phone_numbers = generate_iranian_phone_numbers(count)

for phone_number in random_phone_numbers:
    print(">" * flash_count)
    is_telegram_user = check_telegram_user(phone_number)
    sleep(2)
    if is_telegram_user:
        # print("Yes",phone_number)
        if phone_number not in numbers:
            flash_count += 1
            numbers.append(phone_number)
    else:
        if flash_count > 0:
            flash_count -= 1
        # print("No",phone_number)
        random_phone_numbers.extend(generate_iranian_phone_numbers(1))
        # random_phone_numbers.remove(phone_number)

for number in numbers:
    file.write(f"{number}\n")

print(f'\n{count} issues were successfully created.')
