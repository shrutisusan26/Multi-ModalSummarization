import fitz
import os

def gettext(odir,sdir):
    os.makedirs(sdir)
    for k,i in enumerate(os.listdir(odir)):
        pdf_file = fitz.open(os.path.join(odir,i))
        text = ''
        for page in pdf_file:
            text+= page.get_text()
        fname = i[:-4]
        with open(f"{sdir}{fname}.txt", "w",encoding='utf-8') as fil:
            #print(text)
            fil.write(text)

    
if __name__ =="__main__":
    gettext(r"../../reports/Nptel/",r'./Generated_Text/')
    gettext(r"../Dataset/pdfs",r'./Actual_Text/')