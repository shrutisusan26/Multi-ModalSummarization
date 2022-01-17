import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import cv2

def report_gen(report_dic,ip,fr):
    doc = SimpleDocTemplate(ip.split("\\")[-1][:-3]+".pdf",pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    frames = report_dic.keys()
    cap = cv2.VideoCapture(ip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    scale = float(16*fps/fr)
    Story=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    for i in frames:
        try:
            cap.set(1, i*scale)
            ret, frame = cap.read()
            if not ret:
                print("ERR")
            fname=r'E:\Multi-Modal Summarization\Data\output_images\pic'+str(i)+".jpg"
            cv2.imwrite(fname, frame)
            im = Image(fname, 2*inch, 5*inch)
            Story.append(im)
            Story.append(Paragraph(report_dic[i], styles["Normal"]))
            Story.append(Spacer(1, 12))
        except:
            print("no")
    doc.build(Story)