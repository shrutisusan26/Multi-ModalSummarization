def summaryEntity(item)->dict:
    """
    A function to make summary entities database compliant.

    Args:
        item (dict): A dictionary containing original and summary sentences.

    Returns:
        dict: Containing database compliant dictionary with the original and 
        summary sentences.
    """
    return {
        "article": item['article'],
        'order': item['order']
    }

def vsummaryEntity(item)->dict:
    """
    A function to make video summary entities database compliant.

    Args:
        item (dict): A dictionary containing file path, list of keyframe, frame rate 
        at which video was processed and number of chunks of 16 frames in the entire video.

    Returns:
        dict: Containing database compliant dictionary with file path, list of keyframe, 
        frame rate at which video was processed and number of chunks of 16 frames in the 
        entire video.
    """
    return {
        "path": item['path'],
        'order': item['order'],
        'fr': item['fr'],
        't_chunks': item['t_chunks']

    }
def transEntity(item)->dict:
    """
    A function to make transcription entities database compliant.

    Args:
        item (dict): A dictionary containing transcription ID and the name with which 
        the blob has been uploaded to azure.

    Returns:
        dict: Containing database compliant dictionary with the transcription ID and 
        the name of the blob.
    """
    return {
        "transcription_id": item['transcription_id'],
        'blob_name': item['blob_name']
    }