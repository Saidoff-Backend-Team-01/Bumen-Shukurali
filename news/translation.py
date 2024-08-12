from modeltranslation.translator import translator, TranslationOptions

from news.models import News


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(News, NewsTranslationOptions)