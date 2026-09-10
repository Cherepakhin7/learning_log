from django.shortcuts import render,redirect
from .models import Topic,Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
    """Главная страница приложения 'Журнал обучения'"""
    return render(request,"learning_logs/index.html")

@login_required
def topics(request):
    """Выводит список всех тем"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics" : topics}
    return render(request,"learning_logs/topics.html",context)

@login_required
def topic(request,topic_id):
    """Выводит отдельную тему и все ее записи"""
    topic = Topic.objects.get(id= topic_id)
    #Проверка того, что тема принадлежит текущему пользователю
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {"topic" : topic, "entries" : entries}
    return render(request,"learning_logs/topic.html", context)

@login_required
def new_topic(request):
    """Добавляет новую тему"""
    if request.method != "POST":
        #Данные еще не отправлялись, создается пустая форма
        form = TopicForm()
    else:
        #Отправлены данные POST, нужно обработать данные
        form = TopicForm(data = request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")
    #вывести пустую или недействительную форму
    context = {"form" : form}
    return render(request,"learning_logs/new_topic.html", context)

@login_required
def new_entry(request,topic_id):
    """Добавляет новую запись для конкретной темы"""
    topic = Topic.objects.get(id = topic_id)
    if request.method != "POST":
        #Данные еще не отправлялись,создается новая(пустая) форма
        form = EntryForm()
    else:
        #Отправлены данные POST,нужно обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic",topic_id = topic_id)
    #Вывести пустую или недействидельную форму
    context = {"topic" : topic,"form" : form}
    return render(request,"learning_logs/new_entry.html",context)

@login_required
def edit_entry(request,entry_id):
    """Редактирует уже существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic =  entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != "POST":
        #Исходный запрос, форма заполняется прошлыми записями
        form = EntryForm(instance=entry)
    else:
        #Отправлены данные POST,обработка данных
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic",topic_id = topic.id)
    context = {"topic" : topic,"entry" : entry,"form" : form}
    return render(request,"learning_logs/edit_entry.html",context)