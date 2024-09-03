from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchlTest(RecipeTestBase):

    def test_recipe_search_load_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_scaped(self):
        url = reverse('recipes:search') + '?q=<teste>'
        response = self.client.get(url)
        self.assertIn(
            'search for &quot;&lt;teste&gt;&quot;',
            response.content.decode('utf-8')
            )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'this is recipe one'
        title2 = 'this is recipe two'

        self.make_recipe(slug='one', title=title1, author_data={'username': 'one'})

        self.make_recipe(slug='two', title=title2, author_data={'username': 'two'})

        url = reverse('recipes:search')

        response1 = self.client.get(url + f'?q={title1}')
        response2 = self.client.get(url + f'?q={title2}')
        response_both = self.client.get(url + '?q=this')

        self.assertIn(title1, response1.content.decode('utf-8'))
        self.assertNotIn(title2, response1.content.decode('utf-8'))

        self.assertIn(title2, response2.content.decode('utf-8'))
        self.assertNotIn(title1, response2.content.decode('utf-8'))

        self.assertIn(title1, response_both.content.decode('utf-8'))
        self.assertIn(title2, response_both.content.decode('utf-8'))
