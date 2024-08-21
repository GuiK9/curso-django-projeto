from django.core.exceptions import ValidationError

from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name="teste_default_category"),
            author=self.make_author(username="newusername"),
            title='Recipe Title',
            description='Recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe preparation steps',
            )
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_time_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.is_published)
    
    def test_recipe_str_representation(self):
        self.recipe.title = 'Testing representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing representation')
