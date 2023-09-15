def generate_chat_history(comment):
    from django_server.models import Comment

    messages_list = [
        {"role": "system", "content": comment.post.chat_role},
    ]
    previous_comments = []
    previous_comments = [
        *Comment.objects.filter(id__lte=comment.id, post=comment.post).values_list(
            "text", "author"
        )
    ]
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
    # return comment_text
    return "Dummy ai comment"


def generate_completion_prompt(comment):
    from django_server.models import Comment

    message_history = generate_chat_history(comment)
    comment_text = create_ai_comment(message_history)
    Comment.objects.create(text=comment_text, post=comment.post, author=None)
