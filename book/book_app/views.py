from django.views.generic import TemplateView
from googleapiclient.discovery import build
from django.conf import settings


from datetime import datetime
import time

# Create your views here.
class DashboardView(TemplateView):
    template_name = "book.html"
    
    def get_context_data(self, **kwargs):
        
        max_results = 10
        start_index = 0
    
        start_time = time.time()
        
        api_key = settings.GOOGLE_API_KEY        
        service = build('books', 'v1', developerKey=api_key)
        response = service.volumes().list(q="''", startIndex=start_index, maxResults=max_results).execute()

        end_time = time.time()
        
        total_results = response['totalItems']
        items = response.get('items', [])
        book_list = []

        common_author = ''
        earliest_date = datetime.now().strftime('%Y-%m-%d')
        latest_date = '0000-00-00'

        for item in items:
            id = item.get('id')
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', '')
            authors = volume_info.get('authors', [])
            description = volume_info.get('description', '')
            published_date = volume_info.get('publishedDate', '')

            formatted_authors = ', '.join(authors) if authors else 'Unknown Author'

            if authors and authors[0]:
                if authors.count(authors[0]) > authors.count(common_author):
                    common_author = authors[0]

            if published_date:
                if published_date < earliest_date:
                    earliest_date = published_date
                if published_date > latest_date:
                    latest_date = published_date

            book_list.append({
                'id':id,
                'title': title,
                'authors': formatted_authors,
                'description': description,
                'published_date': published_date,
            })
            
        context = {
        'total_results': total_results,
        'common_author': common_author,
        'earliest_date': earliest_date,
        'latest_date': latest_date,
        'response_time': end_time - start_time,
        'books': book_list,
        'next_start_index': start_index + max_results,
        'prev_start_index': max(0, start_index - max_results),
        }

        return context