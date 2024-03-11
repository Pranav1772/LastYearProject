from django.shortcuts import render
from django.http import JsonResponse
from .models import Chat_Details
import uuid
from django.shortcuts import get_object_or_404

from django.conf import settings
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(dotenv_path=os.path.join(settings.BASE_DIR, '.env'))
client = OpenAI()




# Create your views here.
def homepage(request):
   # Query all records from PDF_Details model
    file_details_list = Chat_Details.objects.all()

    # Prepare a list of dictionaries with 'id' and 'title'
    my_data_list = [
        {'id': file_detail._id, 'title': file_detail.file_name}
        for file_detail in file_details_list
    ]
    context = {'my_data_list': my_data_list}
    return render(request,'pdfchat/index.html',context)

def newChat(request):
    
    # my_assistant = client.beta.assistants.create(
    #     instructions="You are an teacher assistant bot, and you have access to files to answer questions about it.",
    #     name="File handler",
    #     tools=[{"type": "retrieval"}],
    #     model="gpt-3.5-turbo-1106",
    # )
    # print(my_assistant)
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            try:
                thread = client.beta.threads.create()
                chat_id = uuid.uuid4()
                chat_details = Chat_Details(file_name=file.name)
                chat_details._id = chat_id
                chat_details.thread_id = thread.id
                chat_details.file.save(file.name, file)
                new_chat = {'id': chat_details._id, 'title': chat_details.file_name}
                return JsonResponse(new_chat)

            except Exception as e:
                return JsonResponse({'error': f'Error saving the file: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'No file provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def loadChat(request,id):
    chat_details = get_object_or_404(Chat_Details,_id=id)
    thread_id = chat_details.thread_id
    messages = client.beta.threads.messages.list(thread_id=thread_id,order="asc")

    message_list=[]
    
    for message in messages.data:
        # print(message)
        print(message.content[0].text.value)
        message_list.append({
            'role':message.role,
            'content':message.content[0].text.value
        })
    
    # my_data_list = [
    #     {'role': 'user', 'content': 'Hello'},
    #     {'role': 'assistant', 'content': 'How can I assist you today'},
    #     {'role': 'user', 'content': 'what is the timing right now'},
    #     {'role': 'assistant', 'content': "It's 10:30 PM"},
    # ]
    print(id)
    response_data = {'id': id, 'messages': message_list}
    return JsonResponse(response_data,safe=False)

def getResponse(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chatId')
        message_text = request.POST.get('messageText')
        chat_details = get_object_or_404(Chat_Details,_id=chat_id)
        thread_id = chat_details.thread_id
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_text
        )
        runs = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id='asst_3hgzIUaQ2i03TSme0FRAUVAh'
        )
        while True:
            runs = client.beta.threads.runs.retrieve(
                run_id=runs.id,
                thread_id=thread_id
            )
            if runs.status in ["queued","in_progress","cancelling"]:
                break
        
        message = client.beta.threads.messages.list(thread_id=thread_id,order="desc",limit=1)
        print(message)
        # conversation = Conversation.objects.create(
        #     file_details_id=id,
        #     role='user',
        #     content=message_text
        # )
        print(chat_id,message_text)
        
        return JsonResponse({'status': message.data[0].content[0].text.value})
    return JsonResponse({'error': 'Invalid request method'})