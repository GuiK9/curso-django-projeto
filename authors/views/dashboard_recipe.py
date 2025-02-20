from django.views import View
from django.http import Http404
from django.shortcuts import redirect, render

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe
from django.contrib import messages
from django.urls import reverse


class DashboardRecipe(View):
    def get(self, request, id):
        print('estou aqui na classe cbv')
        recipe = Recipe.objects.filter(
            is_published=False,
            author=request.user,
            pk=id
        ).first()

        if not recipe:
            raise Http404()

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()
            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

        return render(
            request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form,
            }
        )
