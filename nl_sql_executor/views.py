from django.shortcuts import render
from django.http import JsonResponse
#from .utils_sql import create_sql_chain
#from .utils_vector import create_vector_chain
from .utils.nl_sql import sql_chain
from .utils.vector import vector_chain
from .utils.query_routing import router

'''
def nl_sql_executor(request):
    #graph = create_sql_chain()
    #graph = vector_chain()
    if request.method == "POST":
        nl = request.POST.get("nl", "")
        nl = nl.lower()
        route = router.invoke({"question": nl})
        result = vector_chain.invoke({"question": nl})
        return JsonResponse({"message": result['answer']})
    return render(request, "nl_executor.html")

'''

def nl_sql_executor(request):
    #graph = create_sql_chain()
    #graph = vector_chain()
    if request.method == "POST":
        nl = request.POST.get("nl", "")
        nl = nl.lower()
        route = router.invoke({"question": nl})
        result = {}
        #result = vector_chain.invoke({"question": nl})
        
        if route["datasource"] == "POSTGRESQL":
            result = sql_chain.invoke({"question": nl})
            for k,v in result.items():
                print(k,v)
        elif route["datasource"] == "FAISS":
            result = vector_chain.invoke({"question": nl})
        else:
            result['answer'] = "Request cannot be processed."
        return JsonResponse({"message": [result['answer'], route['datasource'],]})
        #return JsonResponse({"message": route['datasource']})
    return render(request, "nl_executor.html")
# Create your views here.
