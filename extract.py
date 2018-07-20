from selenium import webdriver

url = 'http://mbopn.kuratorium.waw.pl/'

labels = [" Typ: ", " Rodzaj placówki: ", "nazwa szkoły/placówki:", " miejscowość:", "ulica:", "nr domu:",
          "kod pocztowy:", "telefon:", "email:", "Przedmiot:", "Liczba godzin w tygodniu:",
          "Wymiar zatrudnienia:", "Data dodania:", "Termin składania dokumentów:"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

offers_driver = webdriver.Chrome(chrome_options=chrome_options)
offers_driver.implicitly_wait(5)

details_driver = webdriver.Chrome(chrome_options=chrome_options)
details_driver.implicitly_wait(5)
i = 1

sql_inserts = open('sql_inserts.sql', 'w')

while True:
    print(i)
    offers_driver.get(url + '#/page/' + str(i))
    table = offers_driver.find_element_by_id('all')
    offers = table.find_elements_by_xpath('//td[a="szczegóły "]/a')
    if not offers:
        break
    for offer in offers:
        details_driver.get(offer.get_attribute('href'))
        details = details_driver.find_element_by_id('detalis')
        print('INSERT INTO offer VALUES (', file=sql_inserts)
        while details.find_element_by_xpath('//fieldset/p').text == "(numer oferty: )":
            pass
        print('\t\'' + details.find_element_by_xpath('//fieldset/p').text + '\',', file=sql_inserts)
        for label in labels:
            if label == "Liczba godzin w tygodniu:":
                print('\t' + details.find_element_by_xpath('//tr[td=\"' + label + '\"]/td[@class="ng-binding"]').text
                      + ',', file=sql_inserts)
            else:
                print('\t\'' + details.find_element_by_xpath('//tr[td=\"' + label + '\"]/td[@class="ng-binding"]').text
                      + '\',', file=sql_inserts)
        print('\t\'' + details.find_element_by_xpath('//td/p').text + '\'', file=sql_inserts)
        print(');', file=sql_inserts)
    i += 1

offers_driver.quit()
details_driver.quit()
