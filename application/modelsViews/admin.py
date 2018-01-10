from django.contrib import admin
from modelsViews.models import *

class ingredientsAdmin(admin.ModelAdmin):
    model = ingredientsModel
    filter_horizontal = ('functions','warnings')

class skinTypesAdmin(admin.ModelAdmin):
    model = SkinTypeModel
    filter_horizontal = ('suggested','notSuggested')

admin.site.register(Brand)
admin.site.register(ProductsModel)
admin.site.register(CommentsModel)
admin.site.register(RankingModel)
admin.site.register(SuggestedReasonsConfig)
admin.site.register(SkinTypeModel, skinTypesAdmin)

#substances and ingredients
admin.site.register(ingredientsModel, ingredientsAdmin)
admin.site.register(warningsModel)
admin.site.register(ingredientFunctionsModel)
admin.site.register(banedSubstancesModel)
admin.site.register(restrictedSubstancesModel)
admin.site.register(colorantsModel)
admin.site.register(preservativesModel)
admin.site.register(uvFiltersModel)
