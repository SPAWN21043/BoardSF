from celery import shared_task
import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)
email_send = settings.EMAIL_FROM


@shared_task
def send_create_post(post_id, post_header, post_preview, post_mail):

    subject = 'В категориях, на которые вы подписаны появилась новая статья:'
    text_content = f'Появилась новая статья: {post_header}\n' \
                   f'Ссылка на новость: http://127.0.0.1:8000/posts/{post_id}\n' \
                   f'Краткое содержание: {post_preview}'

    html_save = render_to_string('send_post.html', {'subject': subject, 'heading': post_header, 'preview': post_preview,
                                                    'post_id': post_id})

    msg = EmailMultiAlternatives(subject, text_content, email_send, to=post_mail)

    msg.attach_alternative(html_save, "text/html")
    msg.send()


@shared_task
def send_update_post(post_id, post_header, post_preview, post_mail):

    subject = 'В категориях, на которые вы подписаны была изменена статья'
    text_content = f'В категориях, на которые вы подписаны была изменена статья: \n\n' \
                   f'Ссылка: http://127.0.0.1:8000/posts/{post_id}/\n\n' \
                   f'Заголовок: {post_header}\n' \
                   f'Превью: {post_preview}\n'

    html_save = render_to_string('send_post.html', {'subject': subject, 'heading': post_header, 'preview': post_preview,
                                                    'post_id': post_id})

    msg = EmailMultiAlternatives(subject, text_content, email_send, to=post_mail)

    msg.attach_alternative(html_save, "text/html")
    msg.send()


@shared_task
def send_create_responses(post_id, post_preview, post_mail):
    post_header = 'В вашей статье появился новый отклик'
    subject = 'В вашей статье появился новый отклик:'
    text_content = f'Появилась новая статья: {post_preview}\n' \
                   f'Ссылка на новость: http://127.0.0.1:8000/posts/{post_id}\n' \

    html_save = render_to_string('send_post.html', {'subject': subject, 'heading': post_header, 'preview': post_preview,
                                                    'post_id': post_id})

    msg = EmailMultiAlternatives(subject, text_content, email_send, to=post_mail)

    msg.attach_alternative(html_save, "text/html")
    msg.send()


@shared_task
def send_update_responses(post_id, post_preview, post_mail):
    post_header = 'Ваш комментарий добавлен'
    subject = 'Ваш комментарий добавлен'
    text_content = f'Ваш комментарий для статьи {post_header} добавлен : \n\n' \
                   f'Ссылка: http://127.0.0.1:8000/posts/{post_id}/\n\n' \
                   f'Заголовок: {post_header}\n' \
                   f'Превью: {post_preview}\n'

    html_save = render_to_string('send_post.html', {'subject': subject, 'heading': post_header, 'preview': post_preview,
                                                    'post_id': post_id})

    msg = EmailMultiAlternatives(subject, text_content, email_send, to=post_mail)

    msg.attach_alternative(html_save, "text/html")
    msg.send()
