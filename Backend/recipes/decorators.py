from shared.serializers import JsonResponse


def object_exists(model, slug_or_pk):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                if slug_or_pk == 'pk':
                    model.objects.get(pk=kwargs.get(slug_or_pk))
                else:
                    model.objects.get(slug=kwargs.get(slug_or_pk))
            except model.DoesNotExist:
                return JsonResponse({'error': f'{model._meta.object_name} not found'}, status=404)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

