"""
This module collects helper functions and classes that "span" multiple levels
of MVC. In other words, these functions/classes introduce controlled coupling
for convenience's sake.
"""
# from в моем понимании, это "штука", которая дает понять откуда брать тот или иной class или def(я не знаю , что такое класс, но через контрл я прокликал loader в django/template )
# функции , в свою очередь, это готовые куски кода, которые , чтобы не переписывать каждый раз,наверно, и в пользу читаемости, а так же вызова когда угодно(пока не представляю как может пригодиться это когда угодно) выносят отдельно


from django.http import (
    Http404,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.template import loader
from django.urls import NoReverseMatch, reverse
from django.utils.functional import Promise

# def это функция, а то, что в скобках, это параметры, сказать, что такое параметр я не смогу
def render(
    request, template_name, context=None, content_type=None, status=None, using=None
):
    """
    Return an HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    #content это переменная, которая переводит непонятное мне в скобках render() , через функцию render_to_string , которые находятся в loader, в строчный вид
    content = loader.render_to_string(template_name, context, request, using=using)
    # return это выход из функции и возвращение ответа (в данном случае-классом функции которого конвертируют данные в http(могу ошибаться))
    return HttpResponse(content, content_type, status)

#снова функция в которой задаются параметры
def redirect(to, *args, permanent=False, preserve_request=False, **kwargs):
    """
    Return an HttpResponseRedirect to the appropriate URL for the arguments
    passed.

    The arguments could be:

        * A model: the model's `get_absolute_url()` function will be called.

        * A view name, possibly with arguments: `urls.reverse()` will be used
          to reverse-resolve the name.

        * A URL, which will be used as-is for the redirect location.

    Issues a temporary redirect by default. Set permanent=True to issue a
    permanent redirect. Set preserve_request=True to instruct the user agent
    to preserve the original HTTP method and body when following the redirect.
    """
    #переменная в которой задаются параметры (if-если, esle иначе)
    redirect_class = (
        HttpResponsePermanentRedirect if permanent else HttpResponseRedirect
    )
    #возвращает переменную и это все , что я могу сказать, дальше не понимаю что именно
    return redirect_class(
        resolve_url(to, *args, **kwargs),
        preserve_request=preserve_request,
    )

#создание функции c параметром
def _get_queryset(klass):
    """
    Return a QuerySet or a Manager.
    Duck typing in action: any class with a `get()` method (for
    get_object_or_404) or a `filter()` method (for get_list_or_404) might do
    the job.
    """
    # If it is a model class or anything else with ._default_manager
    #тут смогу только написать, что if, это если
    if hasattr(klass, "_default_manager"):
        #возвращает что-то
        return klass._default_manager.all()
    #возвращает параметр
    return klass

#создание функции с параметрами
def get_object_or_404(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise an Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    #переменная с функцией _get_queryset
    queryset = _get_queryset(klass)
    #если не , а дальше не могу написать
    if not hasattr(queryset, "get"):
        #создание переменной
        klass__name = (
            #тут я знаю только if и else
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        # не знаю что такое raise
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            #не знаю что такое процент
            "or QuerySet, not '%s'." % klass__name
        )
    # try:если нет, то попробовать то , что входит ниже 
    try:
        #вернуть 
        return queryset.get(*args, **kwargs)
    # вернуть исключая queryset.model.DoesNotExist 
    except queryset.model.DoesNotExist:
    #не знаю что такое raise и то что ниже
        raise Http404(
            "No %s matches the given query." % queryset.model._meta.object_name
        )

#  что такое async не знаю , но снова идет вызов функции с параметрами
async def aget_object_or_404(klass, *args, **kwargs):
    """See get_object_or_404()."""
    #переменная значением которой будет функция с параметром klass
    queryset = _get_queryset(klass)
    #если функция hasarrt не с параметром aget, то 
    if not hasattr(queryset, "aget"):
        #переменной klass__name присвоить и дальше две операции с если и иначе, но я не могу их понять 
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        #не знаю что такое raise и дальше не понимаю
        raise ValueError(
            "First argument to aget_object_or_404() must be a Model, Manager, or "
            f"QuerySet, not '{klass__name}'."
        )
    #попробовать вернуть и дальше ничего не могу понять 
    try:
        return await queryset.aget(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404(f"No {queryset.model._meta.object_name} matches the given query.")

#снова функция
def get_list_or_404(klass, *args, **kwargs):
    """
    Use filter() to return a list of objects, or raise an Http404 exception if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    # создается переменаня c параметром
    queryset = _get_queryset(klass)
    #если функция hasattr не с параметром filter, то 
    if not hasattr(queryset, "filter"):
        #создание переменной а что внутри не понимаю
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        # здесь тоже непонятно
        raise ValueError(
            "First argument to get_list_or_404() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
        #создается переменная и дальше непонятно что 
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        raise Http404(
            "No %s matches the given query." % queryset.model._meta.object_name
        )
    return obj_list

#создание функции с параметрами 
async def aget_list_or_404(klass, *args, **kwargs):
    """See get_list_or_404()."""
    #создание переменной с параметром
    queryset = _get_queryset(klass)
    #если hasattr без параметра фильтр , то 
    if not hasattr(queryset, "filter"):
        # задается переменная и дальне не знаю что 
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to aget_list_or_404() must be a Model, Manager, or "
            f"QuerySet, not '{klass__name}'."
        )
    obj_list = [obj async for obj in queryset.filter(*args, **kwargs)]
    if not obj_list:
        raise Http404(f"No {queryset.model._meta.object_name} matches the given query.")
    return obj_list


#  создание функции с непонятными параметрами
def resolve_url(to, *args, **kwargs):
    """
    Return a URL appropriate for the arguments passed.

    The arguments could be:

        * A model: the model's `get_absolute_url()` function will be called.

        * A view name, possibly with arguments: `urls.reverse()` will be used
          to reverse-resolve the name.

        * A URL, which will be returned as-is.
    """
    # If it's a model, use get_absolute_url()
    # если функция hasattr с параметром get_absolute_url, то 
    if hasattr(to, "get_absolute_url"):
        # возвращает оба параметра 
        return to.get_absolute_url()
    # если функция isisnstance с параметрами to и классом Promise, то 
    if isinstance(to, Promise):
        # Expand the lazy instance, as it can cause issues when it is passed
        # further to some Python functions like urlparse.
        # перевести параметр в строчный вид
        to = str(to)

    # Handle relative URLs
    # если функция isinstance с параметром to строчного вида (то что после and ы ничего не понял)
    if isinstance(to, str) and to.startswith(("./", "../")):
        # вернуть to
        return to

    # Next try a reverse URL resolution.
    #  не знаю что такое трай
    try:
        # вернуть функцию reverse, которая , на мой взгляд, делает все параметры строчного вида
        return reverse(to, args=args, kwargs=kwargs)
    # не знаю знаю что будет делаться ниже, но с конце возвращают параметр to
    except NoReverseMatch:
        # If this is a callable, re-raise.
        if callable(to):
            raise
        # If this doesn't "feel" like a URL, re-raise.
        if "/" not in to and "." not in to:
            raise

    # Finally, fall back and assume it's a URL
    return to