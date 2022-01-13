from Transcription.process_transcript import find_sentence_for_frame

def combine_summaries(sentences,chunks,fr,fps):
    scale = (16/fr)
    chunk_summary = {}
    for i in range(len(chunks)-1):
        start_time = i*scale
        end_time = (i+1)*scale
        chunk_summary[i] = find_sentence_for_frame(start_time,end_time,sentences).values()
    return chunk_summary