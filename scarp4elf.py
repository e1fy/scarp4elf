from sys import argv as arguments
from sys import exit
import requests
import re
import os
alphacoders_regex_recon = r"center title'>(.*)<\/h1>"
alphacoders_regex_images = r"boxgrid.>\n*.*a href=.(.*).title"
alphacoders_regex_get_image_url = r"main-content.*(https.*)."
alphacoders_regex_name = r"https:.*\/(.+)"
alphacoders_regex_determine = r"(\d+).*Wallpapers"
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
def download(file_name,file_url):
    try:
        with open(file_name,"wb") as f:
            f.write(requests.get(file_url,headers=headers).content)
            print(f"[+] downloaded - {file_name}")
    except KeyboardInterrupt:
            os.remove(file_name)
            print("[!]keyboard interrupt")
            exit()
def alpha_coders_download_single_page(url):
    request = requests.get(url,headers=headers)
    source_code = request.text
    regex_resault_images_match = re.findall(alphacoders_regex_images,source_code)
    for ids in regex_resault_images_match:
        alpha_coders_get_by_id(ids)
def alpha_coders_fix_key(key):
    if(" " in key):
        key = key.replace(" ","+")
    return key
def alpha_coders_recon(key):
    key = alpha_coders_fix_key(key)
    url = f"https://wall.alphacoders.com/search.php?search={key}"
    recon = requests.get(url,headers=headers)
    recon_source = recon.text
    recon_source = recon_source.replace("\n","")
    recon_resault_images = re.findall(alphacoders_regex_recon,recon_source)
    recon_resault_fixed_images = re.findall(alphacoders_regex_determine,recon_resault_images[0])
    number_of_images = recon_resault_fixed_images[0]
    pages_check = int(number_of_images) % 30
    return number_of_images,pages_check
def scarp_alpha_coders(key,number_of_images,pages_check):
    key = alpha_coders_fix_key(key)
    def go_brr():
        for i in range(1,int(pages)):
            alpha_coders_download_single_page(f"https://wall.alphacoders.com/search.php?search={key}&page={str(i)}")
    if(pages_check==0):
        pages = int(number_of_images) / 30
        go_brr()
    elif(int(number_of_images) <= 30):
        alpha_coders_download_single_page(f"https://wall.alphacoders.com/search.php?search={key}&page=1")
    else:
        pages = int(number_of_images) / 30 + 1
        go_brr()
    return 0
def alpha_coders_get_by_id(ids):
    get_id_page = requests.get(f"https://wall.alphacoders.com/{ids}",headers=headers)
    source_code_id_page = get_id_page.text
    match_image = re.findall(alphacoders_regex_get_image_url,source_code_id_page)
    name = match_image[0]
    file_name = re.findall(alphacoders_regex_name,name)
    download(file_name[0],name)
def main():
    if(len(arguments)==1):
        exit()
    else:
        keyword = " ".join(arguments[1:])
    number_of_images,pages_check = alpha_coders_recon(keyword)
    print(f"{str(number_of_images)} - {str(pages_check)} ")
    scarp_alpha_coders(keyword,number_of_images,pages_check)
if __name__ == "__main__":
    main()
