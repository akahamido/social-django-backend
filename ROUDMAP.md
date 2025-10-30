شرح مرحله اول پروژه
سیستم Backend برای شبکه اجتماعی شامل:
سیستم Auth:

ثبت‌نام (با ایمیل، شماره‌تلفن یا یوزرنیم)

ورود (Login)

با ایمیل، یوزرنیم یا شماره تلفن

احراز هویت با JWT

فراموشی رمز عبور (Forget password)

با تأیید OTP (فعلاً هاردکد مثل 123456)

تغییر رمز عبور (Change password)

تأیید شماره تلفن با OTP (در ثبت‌نام یا تغییر رمز)

تغییر یوزرنیم

سیستمی برای ذخیره و تطبیق mentionها (وقتی یوزرنیم تغییر کرد، لینک‌ها همچنان کار کنند)

آپدیت پروفایل (partial update)

فقط فیلدهای ارسالی بروزرسانی شوند (مثلاً فقط اسم بدون ارسال کل دیتا)

ورود/ثبت‌نام با گوگل

با استفاده از Google OAuth و JWT

نکات:

کاربر باید بتواند با یوزرنیم، ایمیل یا شماره تلفن وارد شود.

این سه فیلد باید unique باشند ولی در عین حال nullable، چون ممکن است کاربر فقط یکی از آن‌ها را داشته باشد.

اگر با گوگل ثبت‌نام کند و یوزرنیم نداشته باشد، یک یوزرنیم رندوم ساخته شود.

اطلاعات کاربر شامل:

id (از نوع UUID و یونیک)

first_name, last_name, username, email, phone, password

created_at, updated_at

تمام فرآیندهای ورود و ثبت‌نام با JWT انجام شود (از پکیج djangorestframework-simplejwt).

اطلاعات حساس (مثل SECRET_KEY، JWT_SECRET، تنظیمات DB و Google API keys) باید در فایل .env ذخیره شود (با پکیج django-environ).

تمام ID ها در هر مدل باید از نوع UUID باشند.

Tech Stack:

Django + Django REST Framework (DRF)

PostgreSQL

Docker + docker-compose

JWT Auth (SimpleJWT)

Swagger Docs (drf-spectacular یا drf-yasg)

Google OAuth (django-allauth + dj-rest-auth)

Postman collection برای تست

نکته نهایی:

فرانت لازم نیست.
فقط با Postman تست شود و APIها با Swagger مستند شوند..
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
روز 1 — اسکلت پروژه و Custom User (تخمین: 5–7 ساعت)

هدف: راه‌اندازی پروژه Django و ساخت مدل کاربر با UUID.
کارها:

scaffold پروژه (django-admin startproject backend) و app users

نصب requirements حداقلی (Django, djangorestframework, psycopg2-binary, django-environ, djangorestframework-simplejwt)

پیاده‌سازی Custom User (AbstractBaseUser) با فیلدهای خواسته‌شده (email, username, phone, uuid, timestamps)

تنظیم AUTH_USER_MODEL در settings

ساخت migrations و اجرای python manage.py migrate
خروجی: Git commit با پیام واضح + README اولیه (چگونگی اجرای dev)
.
.
.
.
.
.
روز 2 — Auth پایه: register / login (identifier) + JWT (تخمین: 6–8 ساعت)

هدف: پیاده‌سازی ثبت‌نام و ورود با JWT
کارها:

پیاده‌سازی authentication backend برای login با username|email|phone

serializers و views برای register و login (استفاده از SimpleJWT برای توکن)

endpointها و مستندات ساده در Swagger (scaffold)

نوشتن یک یا دو تست برای register/login
خروجی: endpoints قابل تست در Postman + commit با توضیح
.
.
.
.
.
.
روز 3 — OTP (هاردکد)، تغییر/ریست پسورد، آپدیت پروفایل (تخمین: 6–8 ساعت)

هدف: flows مربوط به پروفایل و پسورد
کارها:

endpoint برای request/reset password با OTP هاردکد (123456)

endpoint change-password وقتی کاربر login است

PATCH /users/me/ partial update serializer

اعتبارسنجی که فقط فیلدهای ارسال‌شده آپدیت شوند
خروجی: مجموعه request های Postman برای این flows + commit
.
.
.
.
.
.
.
.
.

روز 4 — Change username + Mention design + Social login (Google) (تخمین: 7–9 ساعت)

هدف: mentions پایدار و راه‌اندازی Google OAuth
کارها:

طراحی و پیاده‌سازی مدل Mention و ذخیره‌سازی مرجع (وقتی comment ساخته می‌شود)

endpoint یا کاربری برای تغییر username که mentions را حفظ کند (در واقع چون mention به User ارجاع می‌دهد نیازی به جایگزینی متن نیست)

تنظیم django-allauth + dj-rest-auth برای Google OAuth و متصل کردن به SimpleJWT

تست دستی: ثبت‌نام با Google (در Postman یا ساده شده)
خروجی: commit و مستندات مختصر درباره‌ی mention و Google flow
.
.
.
.
.
.
.
..
روز 5 — Posts/comments ساده + Swagger + Docker + Postman collection + README نهایی (تخمین: 8 ساعت)

هدف: تکمیل بخش social basics، dockerize و مستندسازی
کارها:

مدل Post و Comment با extraction ساده‌ی mentions در save

مستندسازی کامل‌تر با drf-spectacular یا drf-yasg و تهیه صفحه Swagger /api/docs/

فایل Dockerfile و docker-compose.yml برای web + postgres

ساخت postman_collection.json با نمونه requestها (register, login, profile, post, comment, password reset)

تکمیل README و اضافه کردن ROADMAP.md که بالاتر دادم
خروجی: لینک repo با امکانات دمو و کامیت‌های معنی‌دار
