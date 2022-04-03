from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Posts, User, Category, Responses
from .tasks import send_create_post, send_update_post, send_create_responses, send_update_responses


@receiver(post_save, sender=Posts)
def post_save_post(created, **kwargs):
    instance = kwargs['instance']
    cat_id = Category.objects.get(pk=instance.category.id_category)
    to_mail = [user.email for user in cat_id.subscribed.all()]
    if created:
        post_id = instance.id_Post
        post_header = instance.header
        post_preview = instance.content

        if isinstance(to_mail, str):
            post_mail = [to_mail, ]
        else:
            post_mail = to_mail

        send_create_post.delay(post_id, post_header, post_preview, post_mail)

    else:
        post_id = instance.id_Post
        post_header = instance.header
        post_preview = instance.content

        if isinstance(to_mail, str):
            post_mail = [to_mail, ]
        else:
            post_mail = to_mail

        send_update_post.delay(post_id, post_header, post_preview, post_mail)


@receiver(post_save, sender=Responses)
def post_save_responses(created, **kwargs):
    instance = kwargs['instance']
    post_user = Posts.objects.get(pk=instance.post.id_Post)
    to_mail = [post_user.author.email]
    if created:
        post_id = post_user.id_Post
        post_preview = instance.text

        if isinstance(to_mail, str):
            post_mail = [to_mail, ]
        else:
            post_mail = to_mail

        send_create_responses.delay(post_id, post_preview, post_mail)

    else:
        post_id = post_user.id_Post

        post_preview = instance.text

        if isinstance(to_mail, str):
            post_mail = [to_mail, ]
        else:
            post_mail = to_mail

        send_update_responses.delay(post_id, post_preview, post_mail)


