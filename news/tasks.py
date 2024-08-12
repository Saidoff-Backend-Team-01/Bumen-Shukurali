from celery import shared_task
from news.models import News, NewsView



@shared_task
def add_in_views(ip, news_id):
    news_views, created = NewsView.objects.get_or_create(ip=ip)
    
    news = News.published.get(pk=int(news_id))
    news.views.add(news_views)



