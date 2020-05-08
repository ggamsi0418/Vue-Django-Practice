from django.db import models

class Todo(models.Model):
    name = models.CharField('NAME', max_length=5, blank=True)
    todo = models.CharField('TODO', max_length=50)

    def __str__(self):
        return self.todo
    
    def save(self, force_insert=False, forece_updatge=False, using=None, update_fields=None):
        if not self.name:
            self.name = '홍길동'
        super().save() # 상위(슈퍼) 클래스의 save 메소드 호출 ==> 실제로 저장이 완료된다.