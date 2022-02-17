from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import cv2
import os
from helper import dirgetcheck

def report_gen(report_dic,ip,fr):
    """
    Generates a .pdf out of  aligned key sentences & frames

    Args:
        report_dic ([Dict]): Combined summariers wrt to the timestamps with frames as keys and summary sents as vals
        ip ([string]): path of the original video location on the server
        fr ([int]): frame rate of the video
    """
    dir = dirgetcheck('Data','output_images')
    doc = SimpleDocTemplate(os.path.join(os.getcwd(),r'reports\Nptel',ip.split("\\")[-1].split('.')[0]+".pdf"),pagesize=A4,
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
            fname=os.path.join(dir,'pic'+str(i)+".jpg")
            cv2.imwrite(fname, frame)
            im = Image(fname, 5*inch, 2*inch)
            Story.append(im)
            Story.append(Spacer(1, 12))
            val = report_dic[i]
            if val!={}:
                summ = ''
                for time,sent in val.items():
                    summ+=sent
            else:
                summ = ''
            Story.append(Paragraph(summ, styles["Normal"]))
            Story.append(Spacer(1, 12))
        except:
            print("no")
    doc.build(Story)