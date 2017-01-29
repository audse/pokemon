from django.template import Library

from forum.models import Post, Category

register = Library()

@register.simple_tag
def get_posts():
	post_category = Category.objects.get(name="Announcements")
	posts_header = Post.objects.filter(category=post_category).order_by("-post_time")[:6]
	for post in posts_header:
		post.body_length = 64 - len(post.title)
	return posts_header