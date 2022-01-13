def summaryEntity(item)->dict:
        return {
            "article": item['article'],
            'order': item['order']
        }

def vsummaryEntity(item)->dict:
        return {
            "path": item['path'],
            'order': item['order'],
            'fr': item['fr']
    
        }