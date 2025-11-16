# Social API (Learning Project)

This project is a personal learning project built with **Django**, **Django REST Framework**, and **SimpleJWT**.
It’s not a production-ready system — I built it to understand how real APIs work and to practice authentication flows, testing, and basic social features.

---

## Features
- Custom User model (email/phone login)
- Register / Login (JWT)
- Forgot password with OTP (simple hard-coded OTP flow for learning)
- Reset password
- Change password (with old password check)
- User profile: get + partial update
- Username change with conflict validation
- Create posts & comments
- Swagger documentation  
- Postman collection included  
- Docker support  
- API tests using `APITestCase`

---

##  What I Learned
I used this project to get comfortable with:
- Django REST Framework routing, serializers, and APIView/GenericView usage  
- Handling PATCH requests and partial updates  
- JWT authentication flow with SimpleJWT  
- Writing API tests (`APITestCase`, `force_authenticate`, etc.)  
- Building simple OTP-based password reset logic (in this case, hard-coded because the goal was  learning the flow, not production security)  
- Working with Swagger for auto-generated API docs  
- Creating and organizing a Postman collection  
- Containerizing a Django project using a minimal Dockerfile  
- Managing environment variables and project structure for a real API  
- Understanding how to write cleaner, more maintainable view logic  

---

## API Documentation
- Postman collection:
 **[docs/postman_collection.json](docs/Django_Social_Backend.postman_collection.json)**
- Sawgger :
    --
