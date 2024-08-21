from modeltranslation.translator import TranslationOptions, translator

from news.models import News


class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "description")


translator.register(News, NewsTranslationOptions)
