import imp
from Transcription.process_transcript import find_sentence_for_frame
import cv2
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.rl_config import defaultPageSize
from report_gen import  report_gen
def combine_summaries(sentences,chunks,fr,t_chunk):
    scale = (16/fr)
    chunk_summary = {}
    chunks = sorted(chunks)
    for i in range(len(chunks)-1):
        start_time = chunks[i]*scale
        end_time = (chunks[i+1])*scale
        #print(start_time, end_time)
        chunk_summary[chunks[i]] = find_sentence_for_frame(start_time,end_time,sentences)
        s = list(chunk_summary.keys())[0]
        e = list(chunk_summary.keys())[-1]
    if chunks[0]!=0:
        start_time = 0
        end_time = (chunks[0])*scale
        chunk_summary[s]= {**find_sentence_for_frame(start_time,end_time,sentences),**chunk_summary[s]}
    if chunks[-1]!=t_chunk:
        start_time = chunks[-1]*scale
        end_time = (t_chunk)*scale
        chunk_summary[e]= {**find_sentence_for_frame(start_time,end_time,sentences),**chunk_summary[e]}
    return chunk_summary

if __name__=="__main__":
    ip = r'E:\Multi-Modal Summarization\Data\videos\Keynesian economics _ Aggregate demand and aggregate supply _ Macroeconomics _ Khan Academy.mp4'
    PAGE_WIDTH = defaultPageSize[0]
    sentences ={
  "0.0": "What I want to do in this video is start introducing and we've already talked about him a little bit, so actually they've already been introduced, but maybe flesh out a little bit more Keynesian thinking, so this right here is a picture of John Maynard Keynes and I often mispronounce them eskine, because that's how it's spelled.",
  "15.0": " But it's John Maynard Keynes and he was an economist who did a lot of his most famous work during the Great Depression, because in his view, classical models did not seem to be of much use during the Great Depression and so to understand this a little bit better.",
  "30.0": "Let's compare kind of purely classical aggregate supply aggregate demand models to maybe more one that's more Keynesian and some of what we've talked about or Keynesian I should say.",
  "36.2": " I already did my first mispronunciation, one that's a little bit more Keynesian Keynesian, right over here and some of the conversations we've already begun to introduce a little bit of Keynesian thinking.",
  "42.400000000000006": " But in this video, we're going to try to show the difference between the two.",
  "48.60000000000001": " And it's not to say that one is right or one is wrong.",
  "54.80000000000001": " In fact, Keynesian felt that in the long run.",
  "61.0": "The classical model actually made sense, but he also famously said in the long run we are all dead, and I also want to emphasize that this isn't a defense of Keynesian economics.",
  "67.0": " There are some points to what he has to say, but there are other schools of thought.",
  "73.0": " Unfortunately, they often get very dogmatic, but they also have some reasons to be wary of Keynesian economics, and we hope to go over some of that in future videos.",
  "79.0": " But in this one we just want to understand what Keynesian economics is all about and how it really was a fundamental departure from classical economics.",
  "85.0": " So in classical economics.",
  "91.0": "So I'm going to use aggregate demand and aggregate supply in both.",
  "94.0": "So this is classical.",
  "99.0": " This is price this right over here is real GDP real GDP? And I'm going to do it for the Keynesian case as well.",
  "104.0": "So this is price and this right over here is real GDP.",
  "110.0": "GDP now in both in both views of reality or both models, you have a downward sloping aggregate demand curve for all the reasons that we've talked about in multiple videos, it's aggregate demand, that is aggregate demand right over there.",
  "133.5": " So we've seen the long run aggregate supply curve something like this.",
  "142.0": " This is the aggregate supply in the long run, or sometimes it's you'll have long run aggregate supply.",
  "150.5": " Sometimes it'll be referred to that and saying look all prices.",
  "159.0": "Prices and money.",
  "164.0": " They're just facilitating transactions and you go to work and you get paid and all that, but then you go and use that money to go buy other things that the economy produces, like food and shelter and transportation.",
  "169.0": " So all money is a way of facilitating the transactions.",
  "174.0": " But the economy in theory based on how many people it has, what kind of technology it has, what it's productive, what kind of factories it has, what kind of natural resources it has.",
  "179.0": " It's just going to produce what it's going to produce, and if you were to just change aggregate demand.",
  "184.0": " If the government, let's say.",
  "189.0": "Where to print money and aggregate demand were to and distribute it from helicopters in this classical model you would just have aggregate demand shift to the right, but you have this vertical long run aggregate supply curve, so the net effect is it didn't change the output in this classical model.",
  "197.0": " All that happens is that the price goes from this equilibrium price to this equilibrium price over here.",
  "205.0": " So you have the price would go up and you would just experience inflation with no increased output.",
  "213.0": " And there's multiple ways you could have shifted that aggregate demand curve to the right.",
  "221.0": "You could have fiscal policy where the government, maybe it holds, it's maybe it holds its tax revenue constant, but it increases spending or it goes the other way around.",
  "227.0": " It does not decrease, it doesn't change its spending, but it lowers tax revenue.",
  "233.0": " Either of those it kind of tries to pump money into the economy and pushes that aggregate demand curve to the right.",
  "239.0": " And in this purely classical view, it says in the long run that's not going to be any good, just will lead to inflation.",
  "245.0": " The only way that you can increase the output of economy is by making it more productive.",
  "251.0": "Maybe in making some investments in technology make the economy more efficient.",
  "256.3333333333333": " Maybe your population grows so they only way is to really shift this curve to the right on the supply side on the supply side, right over here.",
  "261.66666666666663": " And Keynes did not disagree with that, but he's sitting here in the middle of the Great Depression and saying, look all of a sudden people are poor.",
  "266.99999999999994": " In the 1930s factories did not get blown up.",
  "272.33333333333326": " People didn't disappear.",
  "277.6666666666666": " In fact there are factories that want to be run, but they're being shuttered down because no one is demanding goods from them.",
  "283.0": "There are people that want to work, but no one is asking them to work.",
  "293.6666666666667": " They could work and produce the wealth that could then be distributed to society, but it's no ones demanding for them to do it, so he suspected, well, something weird was happening with aggregate demand, especially in the short run.",
  "304.33333333333337": " So in a very pure, very very very short run model, I know we have talked about kind of a short run aggregate supply curve that is upward sloping, so something that might look something that might look something like that and that is actually starting to put some of the Keynesian ideas into practice.",
  "315.0": "And what I like to think of is kind of something in between, but if you think in the very very very very short term, Keynes would say well prices are going to be very sticky, so especially especially showing the short run.",
  "327.0": "In the short run and I'll call it the very short run, the very short run you have, especially if the economy is producing well below its capacity like it seemed to be doing during the Great Depression.",
  "330.3333333333333": " Prices are sticky.",
  "333.66666666666663": " Prices are sticky, and that makes intuitive sense.",
  "336.99999999999994": " If the economy is trying to get overheated, people are being overworked.",
  "340.33333333333326": " You want them to work more.",
  "343.6666666666666": " Hey, I want overtime.",
  "346.9999999999999": " You want factories to operate faster.",
  "350.3333333333332": " People are going to start, and the utilization is high.",
  "353.6666666666665": " People are going to start charging and more and more.",
  "357.0": "But if I'm unemployed and I'm desperate to work, I'm not going to ask for a pay raise.",
  "361.0": " If my factory is at 30% utilization and someone wants to buy a little bit more, that's not that I'm that I'm going to say, hey, I'm going to raise prices on you.",
  "365.0": " I'll say yeah, this exact same price.",
  "369.0": " Yeah, you want another 5% of my factory to be utilized.",
  "373.0": " Sure, that sounds great.",
  "377.0": " So in the very short run it kind of has the opposite view of the aggregate supply curve.",
  "381.0": " Then the classical model it says at any level of GDP in the short run, prices won't be affected.",
  "385.0": "It won't be affected, and so in this model, right over here.",
  "389.42857142857144": " So this is aggregate supply and I'll call it in the very short run.",
  "393.8571428571429": " Very short run and you can debate what short run or very short run means.",
  "398.28571428571433": " Whether we're talking about days, weeks, months, or even a few years here.",
  "402.7142857142858": " But once you start looking at the world this way, then something interesting happens in this model, right? Over here.",
  "407.1428571428572": " The only way to increase product, the only way to increase GDP was on the supply side.",
  "411.57142857142867": " In this model, right? Over here, the only way to increase GDP is on the demand side.",
  "416.0": "To actually, either through monetary policy, print more money or through fiscal policy, lower taxes while holding spending constant.",
  "423.5": " Or maybe do both.",
  "431.0": " You essentially deficit spending some way without maybe holding taxes constant, but the government spending more whatever shift the curve to the right and that might be a way that might be a way to increase the overall output and canes.",
  "438.5": " Real realization was that look.",
  "446.0": "The classical economists would tell you if you have a free and unfettered market.",
  "451.1666666666667": " The economy will just get to its natural, very efficient state.",
  "456.33333333333337": " And Kane says yes, that is sometimes true, but that's sometimes not true, and we'll talk about different cases and by no means do I think the Keynesian model is the ideal.",
  "461.50000000000006": " And I don't think even Keynes would have thought the Keynesian model describes everything depends on the circumstance.",
  "466.66666666666674": " But Keynes would say look, let's think about very simple, very simple idea.",
  "471.8333333333334": " Let's say you have a person a, person B, person C and person D.",
  "477.0": "And let's say person a cells to person B, person B, cells to person C, person C cells to person B and person D cells to person A and let's say that they are all selling 2 units of whatever good in service that they offer and for whatever reason, let's say C is getting a little bit.",
  "484.5": " See is just all of a sudden got a little bit pessimistic, had a bad dream, woke up on the wrong side of the bed, and said you know what? I'm not feeling so good about the economy.",
  "492.0": " I'm going to hold off for my purchase from B instead of two units.",
  "499.5": " I'm going to purchase one unit.",
  "507.0": "Well bizwell GI my business is bad now I'm only going to produce purchase one unit and a does the same thing for the same reason D does the same thing.",
  "514.75": " Well now it all came back to see and now CC is wow.",
  "522.5": " I was right that dream was predictive but it was a self fulfilling prophecy and now they're going to operate in this state and there might not be any natural way to get them bumped up to that state where they're all buying 2 units from each other without maybe some outside especially some government actor.",
  "530.25": " Maybe all of a sudden saying hey be OK if he doesn't want to buy 2.",
  "543.5": " But then someone else, let's say the government tries to shift the aggregate demand curve through fiscal policy, and they say, hey, well, I'll buy one from you.",
  "549.0": " I'll buy one from you, be, and so then be says, OK, Now I can buy 2 again and daikon by two again and then we can buy 2 again and then see could buy 2 again and then an ideal world.",
  "554.5": " And this is the danger of the government.",
  "560.0": " The government would step back and say OK everything is fine again.",
  "565.5": " I don't have to buy this, but as we know it's very hard once the government starts spending money in some way to actually cut.",
  "571.0": "This spending right over here, but this was the general idea behind the Keynesian versus a classical.",
  "576.6": " He says look there are circumstances like the Great Depression where the economy is operating well below its potential and in those circumstances you need to have a stimulus on the demand side, not just the supply side.",
  "582.2": " Now the correct answer is with all things, it's probably something in between.",
  "587.8000000000001": " It probably a more accurate model is something like this.",
  "593.4000000000001": " So let's draw.",
  "599.0": "So this is price.",
  "603.4285714285714": " This is real GDP right? Over here and we'll still draw our downward sloping aggregate demand curve, aggregate demand curve, and the more accurate thing might look something like this.",
  "607.8571428571429": " Let's say that this is the absolute theoretical maximum output.",
  "612.2857142857143": " If everyone in the country isn't sleeping, the factories are just being run to the ground.",
  "616.7142857142858": " That's the absolute theoretical output.",
  "621.1428571428572": " And let's say that this is it's potential, just a healthy state where the economy might be operating.",
  "625.5714285714287": " The real kind of.",
  "630.0": "Medium run supply curve or short run supply aggregate supply curve, so this is aggregate supply in the very long run.",
  "634.0": " So this is in the long run aggregate supply.",
  "638.0": " The best model would be something that's in between.",
  "642.0": " It might look something like this.",
  "646.0": " So our aggregate supply curve might look something like I wanted a different color.",
  "650.0": "Let me do it in magenta so it might look something like this might look something like this, so if whatever reason, maybe someone has a bad dream or a bunch of people have a bad dream or something scary happens.",
  "656.2": " Aggregate demand gets the stock market, crash is something happens, aggregate demand shifts over there, so when we're out here now, all of a sudden our output is well below potential.",
  "662.4000000000001": " We have a lot of excess capacity, and now the Keynesian ideas seem.",
  "668.6000000000001": " Maybe they'll make sense.",
  "674.8000000000002": " Maybe there should be out some outside stimulus happening.",
  "681.0": "Now on the other side, if we're performing well at potential and then all of a sudden the government wants to do Keynesian policies, and we'll see in future videos, the government will always want to do Keynesian policies, even if they're not justified.",
  "687.2": " It might do.",
  "693.4000000000001": " It will push aggregate demand out here and then the net effect is especially the more vertical.",
  "699.6000000000001": " This is, the more this net effect will be true that you really just get more inflation and you don't really get a lot of increase in output.",
  "705.8000000000002": " So it really depends on the circumstance, but an aggregate supply curve that starts flat at low levels of output."
}
    chunks =  [
    14,
    23,
    67,
    48,
    5,
    107,
    123,
    144,
    194,
    214,
    372,
    291,
    305,
    299,
    429,
    319,
    388,
    461,
    462,
    466,
    480,
    581,
    587
  ]
    
    fr= 4
    t_chunk = 589
    report_dic = combine_summaries(sentences,chunks,fr,t_chunk)
    report_gen(report_dic,ip,fr)