import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://scholar.google.com/citations?view_op=view_org&org=10241031385301082500&hl=th&oi=io")

df = pd.DataFrame(
    {
        'title':['Real-time people tracking in a camera network'],
        'authors':['Wasit Limprasert, Andrew Wallace, Greg Michaelson'],
        'publication_date':['2013/4/24'],
        'description':['We present an approach to track several subjects from video sequences acquired by multiple cameras in real time. We address the key concerns of real time performance and continuity of tracking in overlapping and nonoverlapping fields of view. Each human subject is represented by a parametric ellipsoid having a state vector that encodes its position, velocity and height. We also encode visibility and persistence to tackle problems of distraction and short-period occlusion. To improve likelihood computation from different viewpoints, including the relocation of subjects after network blind spots, the colored and textured surface of each ellipsoid is learned progressively as the subject moves through the scene. This is combined with the information about subject position and velocity to perform camera handoff. For real time performance, the boundary of the ellipsoid can be projected several hundred times per frame for …'],
        'cite_by':['19']
    }
)

for i in range(30):
    profiles = driver.find_elements_by_class_name('gsc_1usr')
    profiles_id = []

    for profile in profiles:
        profiles_id.append(profile.find_element_by_tag_name('a').get_attribute('href').split('=')[2])
    for j in profiles_id:
        print(j)
        url2 = 'https://scholar.google.com/citations?hl=en&user=' + j
        driver.get(url2)
        time.sleep(1)
        while True:
            try:
                element = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.ID, 'gsc_bpf_more'))
                )
                element.click()
            except:
                break
                time.sleep(3)
        for k in driver.find_elements(By.CSS_SELECTOR, "td.gsc_a_t"):
            a = k.find_element_by_css_selector('a')
            k.find_element_by_css_selector('a').click()
            time.sleep(2)
            try:
                title = driver.find_elements_by_css_selector("a[class='gsc_vcd_title_link']")[0].text
            except:
                title = "-"
            try:
                authors = driver.find_elements_by_css_selector("div[class='gsc_vcd_value']")[0].text
            except:
                authors = "-"
            try:
                publication_date = driver.find_elements_by_css_selector('div.gsc_vcd_value')[1].text
            except:
                publication_date = "-"
            try:
                description = driver.find_element_by_css_selector('div.gsh_small').text
            except:
                description = "-"
            try:
                cite_by = \
                driver.find_element_by_css_selector("div[style='margin-bottom:1em']").find_element_by_css_selector('a').text.split(' ')[2]
            except:
                cite_by = "-"
            df = df.append(
                {
                    'title': title,
                    'authors': authors,
                    'publication_date': publication_date,
                    'description': description,
                    'cite_by': cite_by
                }, ignore_index=True
            )
            driver.back()
        driver.back()
    time.sleep(3)
    next_page = driver.find_element_by_css_selector('#gsc_authors_bottom_pag > div > button.gs_btnPR.gs_in_ib.gs_btn_half.gs_btn_lsb.gs_btn_srt.gsc_pgn_pnx')
    next_page.click()
df.to_csv('Paper_table.csv')