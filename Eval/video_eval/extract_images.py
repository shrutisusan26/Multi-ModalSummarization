import fitz
import io
from PIL import Image
import os

def getimages(odir,sdir):
    os.makedirs(sdir)
    for k,i in enumerate(os.listdir(odir)):
        pdf_file = fitz.open(os.path.join(odir,i))
        os.mkdir(os.path.join(sdir,i))
        # STEP 3
        # iterate over PDF pages
        for page_index in range(len(pdf_file)):
            
            # get the page itself
            page = pdf_file[page_index]
            image_list = page.get_images()
            
            # printing number of images found in this page
            # if image_list:
            #     print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            # else:
            #     print("[!] No images found on page", page_index)
            for image_index, img in enumerate(page.get_images(), start=1):
                
                # get the XREF of the image
                xref = img[0]
                
                # extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                
                # get the image extension
                image_ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))
                # save it to local disk
                image.save(open(f"{sdir}{i}/{page_index+1}_{image_index}.{image_ext}", "wb"))
    
if __name__ =="__main__":
    getimages(r"../../reports/Nptel/",r'./Generated_Keyframes/')
    #getimages(r"../Dataset/pdfs",r'./Actual_Images/')
    #getimages(r"../../reports/",r'./Everything/')