from modeltranslation.translator import TranslationOptions, translator

from .models import FAQ


class FAQTranslationOptions(TranslationOptions):
    fields = ("question", "answer")


translator.register(FAQ, FAQTranslationOptions)
