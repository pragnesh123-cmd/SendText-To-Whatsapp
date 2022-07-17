from urllib import request
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from SendTextToWhatsapp.settings import BASE_DIR
from webdriver_manager.chrome import ChromeDriverManager
import time as t
from .models import FileForms
import os

def webwhatsapp(request):
        if request.method == "POST":
                msg = request.POST['msg']
                filename = request.FILES['file']
                form = FileForms(request.POST, request.FILES)
                if form.is_valid:
                        form.save()
                message = msg
                numbers = []

                with open(f"{BASE_DIR}/media/media/{filename}" ,"r") as f: 
                        for line in f.read().splitlines():
                                print(line)
                                if line != "":
                                        numbers.append(int(line))
                os.remove(f"{BASE_DIR}/media/media/{filename}")                        
                numbers = list(set(numbers))
                total_number=len(numbers)
                delay = 30
                time = 5
                driver = webdriver.Chrome(ChromeDriverManager().install())
                driver.get('https://web.whatsapp.com')
                msgcount = 0
                failed = 0
                result = input("press yes only after logging in whatsapp.")
                if result == 'yes':
                        for number in numbers:
                                number = number.strip()
                                if number == "":
                                        continue
                                url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
                                driver.get(url)
                                try:
                                        click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CLASS_NAME , '_4sWnG')))
                                        print(click_btn)
                                        t.sleep(1)
                                        click_btn.click()
                                        t.sleep(time)
                                        msgcount+=1
                                        print(msgcount)
                                        print(total_number-(failed+msgcount))
                                except Exception as e:
                                        failed+=1
                                        print(failed)
                                        print(total_number-(failed+msgcount))
        form = FileForms()                            
        return render(request,"form.html",{"form":form})                                

