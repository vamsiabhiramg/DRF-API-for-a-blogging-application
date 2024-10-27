from rest_framework.test import APITestCase,APIRequestFactory
from .views import PostListCreateView
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
#from rest_framework.test import force_authenticate

User=get_user_model()

class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        response = self.client.get(reverse('posts_home'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Hello World')
        
class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.url=reverse('list_posts')
        # self.factory = APIRequestFactory()
        # self.view = PostListCreateView.as_view()
        # self.url=reverse('list_posts')
        # self.user = User.objects.create(username='guru', email='guru@app.com',password='Admin@123')
        
    def authentiate(self):
        self.client.post(reverse('signup'), {
            "username":"guru",
            "email":"guru@app.com",
            "password":"Admin@123",
        })
        
        response=self.client.post(reverse('login'), {
            "email":"guru@app.com",
            "password":"Admin@123",
        })
        
        #print(response.data)
        
        token=response.data['tokens']['access']
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    
        
    def test_list_posts(self):
        response=self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_post_creation(self):
        self.authentiate()
        
        sample_data={
            "title":"sample post",
            "content":"sample content",
        }
        response=self.client.post(reverse('list_posts'), sample_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], sample_data['title'])
        self.assertEqual(response.data['content'], sample_data['content'])
    
        # self.factory = APIRequestFactory()
        # self.view = PostListCreateView.as_view()
        # sample_post={
        #     "title":"sample post",
        #     "content":"sample content",
        # }
        # request = self.factory.post(self.url, sample_post)
        # request.user = self.user
        # response = self.view(request)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)