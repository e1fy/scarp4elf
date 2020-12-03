import requests
import re
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
def scarp_alpha_coders(key):
    #regexes and setup
    url = f"https://wall.alphacoders.com/search.php?search={key}"
    regex_recon = r"center title'>(.*)<\/h1>"
    regex_recon_pages = r"<input type=.text. class=.form-control. placeholder=.Page # \/ (\d+).>"
    regex_images = r"boxgrid.>\n*.*a href=.(.*).title"
    regex_get_image_url = r"main-content.*(https.*)."
    regex_name = r"https:.*\/(.+)"
    #recon
    recon = requests.get(url,headers=headers)
    recon_source = recon.text
    recon_source=recon_source.replace("\n","")
    #results
    recon_resault_images = re.findall(regex_recon,recon_source)
    recon_resault_pages = re.findall(regex_recon_pages,recon_source)
    pages = recon_resault_pages[0]
    print(f"{recon_resault_images[0]} {pages} pages - alphacoders")
    #fixing
    if(" " in key):
        key = key.replace(" ","+")
    #scarping
    for i in range(1,int(pages)+1):
        request = requests.get(f"https://wall.alphacoders.com/search.php?search={key}&page={str(i)}",headers=headers)
        source_code = request.text
        regex_resault_images_match = re.findall(regex_images,source_code)
        for ids in regex_resault_images_match:
            get_id_page = requests.get(f"https://wall.alphacoders.com/{ids}",headers=headers)
            source_code_id_page = get_id_page.text
            match_image = re.findall(regex_get_image_url,source_code_id_page)
            name = match_image[0]
            file_name = re.findall(regex_name,name)
            with open(file_name[0],"wb") as f:
                f.write(requests.get(name,headers=headers).content)
            print(f"[+] downloaded - {name}")
def main():
    keyword = "zero two" #character goes here
    scarp_alpha_coders(keyword)
if __name__ == "__main__":
    main()
