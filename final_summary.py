from Transcription.process_transcript import find_sentence_for_frame
import cv2
def combine_summaries(sentences,chunks,fr,t_chunk):
    scale = (16/fr)
    chunk_summary = {}
    chunks = sorted(chunks)
    for i in range(len(chunks)-1):
        start_time = chunks[i]*scale
        end_time = (chunks[i+1])*scale
        #print(start_time, end_time)
        chunk_summary[chunks[i]] = find_sentence_for_frame(start_time,end_time,sentences)
    if chunks[0]!=0:
        start_time = 0
        end_time = (chunks[0])*scale
        chunk_summary[chunks[0]]= {**find_sentence_for_frame(start_time,end_time,sentences),**chunk_summary[chunks[0]]}
    if chunks[-1]!=t_chunk:
        start_time = chunks[-1]*scale
        end_time = (t_chunk)*scale
        chunk_summary[chunks[0]]= {**find_sentence_for_frame(start_time,end_time,sentences),**chunk_summary[chunks[0]]}
    return chunk_summary

if __name__=="__main__":
    ip = r'E:\Multi-Modal Summarization\Data\videos\input.mp4'
    sentences = {
    "5.5": " Today we will discuss how to write a function, rotate that rotates an array of size north by D elements.",
    "11.0": "Let's look at this example.",
    "14.333333333333334": " We have this array with elements 123456 and seven.",
    "80.0": "That is, the last two elements six and seven are replaced by the D elements in the temporary array.",
    "84.5": " That is one and two.",
    "89.0": "Clearly the output array has been rotated to the left by a factor of 2.",
    "95.0": "The 2nd way is by rotating it one by one we store the first elements of the array that is the element at index zero in a temporary variable temp.",
    "106.0": "Then we move the element at index one to index zero, index two to index one, and so on until we finally move temp to index N 1.",
    "182.0": "And let D be three.",
    "185.0": " That means we wish to rotate this array by three.",
    "188.0": "So N is 12 and D is 3.",
    "229.0": "Next we move the elements in the second set.",
    "233.0": "And then in the third set we finally get this array.",
    "239.0": "We can see that all the elements in this array are shifted by three elements to the left.",
    "245.0": "Here is the simple implementation of the juggling algorithm.",
    "249.0": "We run a loop from index 0, tagd of D and warg is a separate function used to find the greatest common divisor of two numbers."
    }
    chunks = [
    7,
    27,
    53,
    91,
    189,
    163,
    212,
    250,
    261,
    417,
    334,
    312,
    366,
    382
    ]
    fr= 24
    t_chunk = 432
    report_dic = combine_summaries(sentences,chunks,fr,t_chunk)
    frames = report_dic.keys()
    cap = cv2.VideoCapture(ip)
    fps = cap.get(cv2.CAP_PROP_FPS)
    #print(fps)
    scale = float(16*fps/fr)
    for i in frames:
        try:
            #print(i*scale)
            cap.set(1, i*scale)
            ret, frame = cap.read()
            if not ret:
                print("ERR")
            fname=r'E:\Multi-Modal Summarization\Data\output_images\pic'+str(i)+".jpg"
            cv2.imwrite(fname, frame)
        except:
            print("no")

    for key,val in report_dic.items():
        summ=''
        #print(val)
        if val!={}:
            summ = ''
            for time,sent in val.items():
                #print(sent)
                summ+=sent
            print(str(key)+' : '+ summ)
        else:
            print(str(key))
