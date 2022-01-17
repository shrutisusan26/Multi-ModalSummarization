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
    ip = r'E:\Multi-Modal Summarization\Data\videos\Keynesian economics _ Aggregate demand and aggregate supply _ Macroeconomics _ Khan Academy.mp4s'
    sentences ={
    "91.0": "So I'm going to use aggregate demand and aggregate supply in both.",
    "94.0": "So this is classical.",
    "99.0": " This is price this right over here is real GDP real GDP? And I'm going to do it for the Keynesian case as well.",
    "150.5": " Sometimes it'll be referred to that and saying look all prices.",
    "159.0": "Prices and money.",
    "164.0": " They're just facilitating transactions and you go to work and you get paid and all that, but then you go and use that money to go buy other things that the economy produces, like food and shelter and transportation.",
    "174.0": " But the economy in theory based on how many people it has, what kind of technology it has, what it's productive, what kind of factories it has, what kind of natural resources it has.",
    "179.0": " It's just going to produce what it's going to produce, and if you were to just change aggregate demand.",
    "184.0": " If the government, let's say.",
    "213.0": " And there's multiple ways you could have shifted that aggregate demand curve to the right.",
    "221.0": "You could have fiscal policy where the government, maybe it holds, it's maybe it holds its tax revenue constant, but it increases spending or it goes the other way around.",
    "227.0": " It does not decrease, it doesn't change its spending, but it lowers tax revenue.",
    "261.66666666666663": " And Keynes did not disagree with that, but he's sitting here in the middle of the Great Depression and saying, look all of a sudden people are poor.",
    "266.99999999999994": " In the 1930s factories did not get blown up.",
    "272.33333333333326": " People didn't disappear.",
    "293.6666666666667": " They could work and produce the wealth that could then be distributed to society, but it's no ones demanding for them to do it, so he suspected, well, something weird was happening with aggregate demand, especially in the short run.",
    "304.33333333333337": " So in a very pure, very very very short run model, I know we have talked about kind of a short run aggregate supply curve that is upward sloping, so something that might look something that might look something like that and that is actually starting to put some of the Keynesian ideas into practice.",
    "315.0": "And what I like to think of is kind of something in between, but if you think in the very very very very short term, Keynes would say well prices are going to be very sticky, so especially especially showing the short run.",
    "346.9999999999999": " You want factories to operate faster.",
    "350.3333333333332": " People are going to start, and the utilization is high.",
    "353.6666666666665": " People are going to start charging and more and more.",
    "361.0": " If my factory is at 30% utilization and someone wants to buy a little bit more, that's not that I'm that I'm going to say, hey, I'm going to raise prices on you.",
    "365.0": " I'll say yeah, this exact same price.",
    "369.0": " Yeah, you want another 5% of my factory to be utilized.",
    "377.0": " So in the very short run it kind of has the opposite view of the aggregate supply curve.",
    "381.0": " Then the classical model it says at any level of GDP in the short run, prices won't be affected.",
    "385.0": "It won't be affected, and so in this model, right over here.",
    "431.0": " You essentially deficit spending some way without maybe holding taxes constant, but the government spending more whatever shift the curve to the right and that might be a way that might be a way to increase the overall output and canes.",
    "438.5": " Real realization was that look.",
    "446.0": "The classical economists would tell you if you have a free and unfettered market.",
    "451.1666666666667": " The economy will just get to its natural, very efficient state.",
    "456.33333333333337": " And Kane says yes, that is sometimes true, but that's sometimes not true, and we'll talk about different cases and by no means do I think the Keynesian model is the ideal.",
    "461.50000000000006": " And I don't think even Keynes would have thought the Keynesian model describes everything depends on the circumstance.",
    "484.5": " See is just all of a sudden got a little bit pessimistic, had a bad dream, woke up on the wrong side of the bed, and said you know what? I'm not feeling so good about the economy.",
    "492.0": " I'm going to hold off for my purchase from B instead of two units.",
    "499.5": " I'm going to purchase one unit.",
    "607.8571428571429": " Let's say that this is the absolute theoretical maximum output.",
    "612.2857142857143": " If everyone in the country isn't sleeping, the factories are just being run to the ground.",
    "616.7142857142858": " That's the absolute theoretical output.",
    "621.1428571428572": " And let's say that this is it's potential, just a healthy state where the economy might be operating.",
    "625.5714285714287": " The real kind of.",
    "630.0": "Medium run supply curve or short run supply aggregate supply curve, so this is aggregate supply in the very long run.",
    "634.0": " So this is in the long run aggregate supply.",
    "638.0": " The best model would be something that's in between.",
    "662.4000000000001": " We have a lot of excess capacity, and now the Keynesian ideas seem.",
    "668.6000000000001": " Maybe they'll make sense.",
    "674.8000000000002": " Maybe there should be out some outside stimulus happening."
    }
    chunks =  [
    4,
    29,
    78,
    55,
    65,
    97,
    119,
    138,
    238,
    277,
    343,
    429,
    449,
    495,
    564,
    592,
    603,
    593,
    606,
    618,
    662,
    678,
    687,
    704
  ]
    fr= 16
    t_chunk = 724
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
