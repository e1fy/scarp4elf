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
def download_single_page(url):
    request = requests.get(url,headers=headers)
    source_code = request.text
    regex_resault_images_match = re.findall(alphacoders_regex_images,source_code)
    for ids in regex_resault_images_match:
        get_by_id(ids)
def scarp_alpha_coders(key):
    if(" " in key):
        key = key.replace(" ","+")
    url = f"https://wall.alphacoders.com/search.php?search={key}"
    recon = requests.get(url,headers=headers)
    recon_source = recon.text
    recon_source = recon_source.replace("\n","")
    recon_resault_images = re.findall(alphacoders_regex_recon,recon_source)
    recon_resault_fixed_images = re.findall(alphacoders_regex_determine,recon_resault_images[0])
    number_of_images = recon_resault_fixed_images[0]
    pages_check = int(number_of_images) % 30
    if(pages_check==0):
        pages = int(number_of_images) / 30
    else:
        pages = int(number_of_images) / 30 + 1
    for i in range(1,int(pages)):
        download_single_page(f"https://wall.alphacoders.com/search.php?search={key}&page={str(i)}")
    return 0
def get_by_id(ids):
    get_id_page = requests.get(f"https://wall.alphacoders.com/{ids}",headers=headers)
    source_code_id_page = get_id_page.text
    match_image = re.findall(alphacoders_regex_get_image_url,source_code_id_page)
    name = match_image[0]
    file_name = re.findall(alphacoders_regex_name,name)
    download(file_name[0],name)
def download(file_name,file_url):
    try:
        with open(file_name,"wb") as f:
            f.write(requests.get(file_url,headers=headers).content)
            print(f"[+] downloaded - {file_name}")
    except KeyboardInterrupt:
            os.remove(file_name)
            print("[!]keyboard interrupt")
            exit()
def main():
    if(len(arguments)==1):
        exit()
    else:
        keyword = " ".join(arguments[1:])
    scarp_alpha_coders(keyword)
if __name__ == "__main__":
    main()
