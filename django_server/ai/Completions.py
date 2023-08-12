from django_server.models import Comment
from openai import ChatCompletion


def generate_chat_history(comment):
    messages_list = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
    previous_comments = [
        *Comment.objects.filter(id__lte=comment.id, post_id=comment.post_id).values_list('text', 'author')]
    for comment in previous_comments:
        if comment[1] is None:
            messages_list.append({"role": "assistant", "content": comment[0]})
        else:
            messages_list.append({"role": "user", "content": comment[0]})
    return messages_list


def create_ai_comment(message_history):
    # response = ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=message_history,
    #     max_tokens=512,
    # )
    # comment_text = response.choices[0].message['content']
    return "Dummy ai comment"  # comment_text


def ai_comment(comment):
    message_history = generate_chat_history(comment)
    comment_text = create_ai_comment(message_history)
    Comment.objects.create(text=comment_text, post_id=comment.post_id, author=None)