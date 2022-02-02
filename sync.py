def find_sentence_for_frame(start_time,end_time,sentences):
    """
    Filter all those sentences in the key sentences that lie within the 
    start and end time (interval between to key frames)
    Args:
        start_time ([int]):  offset to the start of the current key frame  
        end_time ([int]):    offset to the start of the next keyframe 
        sentences ([Dict]):  all summary sentences

    Returns:
        res[Dict]: Filtered dictionary with correponding sentences for the frame
    """
    res = {key: val for key, val in filter(lambda sub: int(float(sub[0])) >= start_time and
                                   int(float(sub[0])) <= end_time, sentences.items())}
    return res

def combine_summaries(sentences,chunks,fr,t_chunk):
    """
    Combines text and video summaries based on timestamps
    Args:
        sentences ([Dict]): Sentences with timestamps
        chunks ([list]): Ordering of key frames selected
        fr ([int]): Frame rate of the desired video
        t_chunk ([list]): Ordering of key sentences selected

    Returns:
       chunk_summary[Dict]: Combined summariers wrt to the timestamps 
       with frames as keys and summary sents as vals
    """
    scale = (16/fr)
    chunk_summary = {}
    chunks = sorted(chunks)
    for i in range(len(chunks)-1):
        start_time = chunks[i]*scale
        end_time = (chunks[i+1])*scale
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
