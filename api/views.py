import json

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic import DeleteView, ListView
from django.views.generic.edit import BaseCreateView, BaseDeleteView
from django.views.generic.list import BaseListView

from todo.models import Todo


# ensure_csrf_cookie 데코레이터는
# cookie에 csrf Token을 담아서 클라이언트게 전해준다. (클라이언트의 첫 진입 시점에 발급)
# 보통의 경우 '{% csrf_token %}'을 사용하면 django에서 위 과정을 알아서 처리해준다.
# 하지만 본 예제의 경우, csrf_token 탬플릿 태그를 사용하지 않기 때문에
# 이와 같은 데코레이터 기능이 필요한 것이다.
@method_decorator(ensure_csrf_cookie, name='dispatch')
class ApiTodoLV(BaseListView):
    model = Todo

    def render_to_response(self, context, **response_kwargs):
        # values 메소드는 테이블에서 가져온 각각의 레코드들을 딕셔너리로 풀어준다
        todoList = list(context['object_list'].values())
        return JsonResponse(data=todoList, safe=False, status=200)


# csrf 임시로 꺼놓기
# 클래스에 데코레이터 설정하기
# @method_decorator(csrf_exempt, name='dispatch')
class ApiTodoDelV(BaseDeleteView):
    model = Todo
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return JsonResponse(data={}, status=204)


# @method_decorator(csrf_exempt, name='dispatch')
class ApiTodoCV(BaseCreateView):
    model = Todo
    fields = '__all__' # createview는 내부에서 form을 만들기 때문에 fields 속성은 필수

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # form 형식으로 받을 때는 request.POST
        # form 형식이 아닌 경우에는 request.body
        # 그런데 request.body는 Json(str) 형태이기 때문에 이를 딕셔너리로 바꿔줄 수 있는 json 모듈을 사용해야 한다.
        kwargs['data'] = json.loads(self.request.body) 
        return kwargs


    def form_valid(self, form):
        print('form_valid()', form)
        self.object = form.save()
        newTodo = model_to_dict(self.object) # self.object가 모델 타입이기 때문에 딕셔너리로 변환
        print(f'newTodo: {newTodo}')
        return JsonResponse(data=newTodo, status=201)

    def form_invalid(self, form):
        print('form_invalid()', form)
        # form.errors의 데이터 타입은 딕셔너리!
        return JsonResponse(data=form.errors, status=400)


"""
BaseDeleteView와 DeleteView의 차이
(ListView도 마찬가지)

DeleteView는 template 처리에 대한 로직도 포함되어 있다.
하지만 현재 로직에서는 JsonResponse로 응답을 하기 때문에
template 처리는 필요없는 기능이다.
그러므로 BaseDeleteView를 사용하는 것이 좀 더 간결한 코드라고 할 수 있다.

"""

# class ApiTodoLV(ListView):
#     model = Todo

#     # def get(self, request, *args, **kwargs):
#     #     tmpList = [
#     #         {'id': 1, 'name': 'd박정빈', 'todo': '풋살하기'},
#     #         {'id': 2, 'name': 'd박정빈', 'todo': '인프런 강의듣기'},
#     #         {'id': 3, 'name': 'd홍길동', 'todo': '장작패기'},
#     #         {'id': 4, 'name': 'd홍길동', 'todo': '순찰돌기'},
#     #     ]
#     #     return JsonResponse(data=tmpList, safe=False)

#     def render_to_response(self, context, **response_kwargs):
#         # values 메소드는 테이블에서 가져온 각각의 레코드들을 딕셔너리로 풀어준다
#         todoList = list(context['object_list'].values())
#         return JsonResponse(data=todoList, safe=False, status=200)


# # csrf 임시로 꺼놓기
# # 클래스에 데코레이터 설정하기
# @method_decorator(csrf_exempt, name='dispatch')
# class ApiTodoDelV(DeleteView):
#     model = Todo
    
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.delete()

#         return JsonResponse(data={}, status=204)
