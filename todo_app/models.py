from django.db import models

class Category(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField('name', max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Category'
        
    def __str__(self):
        return "Nome da categoria: " + self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', models.CASCADE, db_column='User_id')  # Field name made lowercase.
    todo = models.ForeignKey('Todo', models.CASCADE, db_column='Todo_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comment'


class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', models.CASCADE, db_column='User_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Todo'
        
    def __str__(self):
        return "Título do Todo: " + self.title

class Todocategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, models.CASCADE, db_column='Category_id')  # Field name made lowercase.
    todo = models.ForeignKey(Todo, models.CASCADE, db_column='Todo_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TodoCategory'


class Todohistory(models.Model):
    id = models.AutoField(primary_key=True)
    old_title = models.CharField(max_length=100)
    new_title = models.CharField(max_length=100)
    changed_at = models.DateTimeField(auto_now_add=True)
    todo = models.ForeignKey(Todo, models.CASCADE, db_column='Todo_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TodoHistory'


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(unique=True, max_length=255)
    sms = models.CharField(max_length=16, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'User'
        
    def __str__(self):
        return "Nome do usuário: " + self.name + " - Email: " + self.email


class Usercategory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column='User_id')  # Field name made lowercase.
    category = models.ForeignKey(Category, models.CASCADE, db_column='Category_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserCategory'


class Timestamps(models.Model):
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timestamps'
