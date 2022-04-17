from app import db
from app.models import User, Post

# добавим нескольких пользователей
u = User(username='john', email='john@example.com')
db.session.add(u)
db.session.commit()

u = User(username='susan', email='susan@example.com')
db.session.add(u)
db.session.commit()

# получим всех пользователей
users = User.query.all()
print(users)

# получим пользователя с id = 1
u = User.query.get(1)
print(u)

# сделаем публикацию
p = Post(body='my first post!', author=u)
db.session.add(p)
db.session.commit()

# получим все публикации, которые сделал один пользователь с id = 1
u = User.query.get(1)
posts = u.posts.all()
print(posts)

# распечатаем id публикаций, имена авторов и содержание
posts = Post.query.all()
for p in posts:
    print(p.id, p.author.username, p.body)

# пользователи по алфавиту в обратном порядке
User.query.order_by(User.username.desc()).all()

# удалим всех пользователей
users = User.query.all()
for u in users:
    db.session.delete(u)

# удалим все публикации
posts = Post.query.all()
for p in posts:
    db.session.delete(p)
    
# зафиксируем изменения в базе
db.session.commit()
