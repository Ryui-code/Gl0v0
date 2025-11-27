from modeltranslation.translator import TranslationOptions, register
from .models import Store, StoreRating, Order, CourierRating

@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(StoreRating)
class StoreRatingTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(CourierRating)
class CourierRatingTranslationOptions(TranslationOptions):
    fields = ('description',)