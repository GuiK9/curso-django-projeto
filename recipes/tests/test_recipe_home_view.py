from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTeste(RecipeTestBase):
    def test_recipe_home_view_is_correct(self):
        view = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_view_return_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_contex_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_contex_recipes), 1)

    def test_recipe_category_template_loads_recipes(self):
        title = 'this is a category test'

        self.make_recipe(title=title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(title, content)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<H1 class="center m-y">No recipes found here</H1>',
            response.content.decode('utf-8')
        )

    def test_recipe_detail_template_loads_correct_recipe(self):
        needed_title = 'this is a detail page - It load one recipe'

        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'id': 1,
                }
            )
        )
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published false don't show"""

        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('No recipes found here', content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published false don't show"""

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', args=(recipe.category.id,)))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published false don't show"""

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', args=(recipe.id,)))

        self.assertEqual(response.status_code, 404)
