def summaryEntity(item)->dict:
        return {
            "article": item['article'],
            'order': item['order']
        }

def vsummaryEntity(item)->dict:
        return {
            "path": item['path'],
            'order': item['order'],
            'fr': item['fr'],
            't_chunks': item['t_chunks']
    
        }
def transEntity(item)->dict:
        return {
            "transcription_id": item['transcription_id'],
            'blob_name': item['blob_name']
        }