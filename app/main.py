from fastapi import FastAPI
from app.api.routes import router
import logging

logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    app.include_router(router.routes)


# response_content = """### 1. **Found Files**:
# - **UsernameView in an unspecified file**: This file includes the UsernameView class that extends Django REST Framework's GenericAPIView and uses UsernameSerializ
# er for input validation and serialization. It interacts with helper functions parse_instagram and generate_message for processing Instagram data and generating a personalized message, respectively.
#
# ### 2. **Downsides/Comments**:
# - **Error Handling**: The implementation of error handling seems minimal. While serializer.is_valid(raise_exception=True) will raise exception on serializer errors, th
# ere is no clear handling or logging for issues that might occur during the execution of parse_instagram or generate_message. Issues like network errors, API limitations, or unexpected data formats are not addressed.
# - **Logging**: There is no indication of any logging mechanism. In a production environment, logging is crucial for debugging and tracking the flow of data and errors.
# - **Documentation**: Code comments and method descriptions are lacking. Adding docstrings to the class and methods would improve maintainability and understandability, especially for other developers or future maintenance.
# - **Security**: The code directly uses request.data['username'] without additional checks. This can be potentially risky as it assumes the username exists in the data payload without fail. In situations where the key might be missing, the code could raise a KeyError.
# - **Performance Considerations**: The current setup does not display any optimizations like caching which could be beneficial, especially if the parse_instagram function is hitting external services or APIs. Caching could seriously improve response times and reduce server load.
# - **Test Coverage**: There is no mention of tests. Proper unit and integration tests are necessary to ensure the functionality and robustness of the API endpoints.
#
# ### 3. **Rating**: 3/5
# - The code displays a basic but functional handling of the task using Django REST Framework appropriately with a clean, straightforward approach. However, due to the lack of error handling, security checks, and optimizations, there is a significant room for improvement.
#
# ### 4. **Conclusion**:
# The Junior developer shows promising skills in utilizing Django REST Framework and building RESTful APIs but lacks in-depth handling of potential runtime errors, security concerns, and documentation. With guidance and experience, these areas can be greatly improved. It is recommended that the developer:
# - Implement error handling for external function calls.
# - Add detailed logging for debugging and operational visibility.
# - Secure and validate all inputs to avoid unexpected errors or potential security risks.
# - Enhance the application performance with techniques like caching.
# - Include comprehensive comments and documentation.
# - Develop tests to ensure code reliability and ease future modifications.
#
# Overall, the developer has made a good start but should focus on robustness and security to advance further in backend development. With continued learning and attention to best practices, the developer has the potential to grow significantly in their role."""
# # Структура для зберігання результатів
# response_blocks = {
#     'found_files': '',
#     'downsides_comments': '',
#     'rating': '',
#     'conclusion': ''
# }
#
# # Використовуємо ключі для ідентифікації поточного блоку
# current_key = None
#
# # Розділяємо текст на рядки
# for line in response_content.split('\n'):
#     line = line.strip()  # Прибираємо пробіли на початку та в кінці
#
#     # Перевіряємо, до якого блоку належить рядок
#     if line.startswith('### 1. **Found Files**:'):
#         current_key = 'found_files'
#         response_blocks[current_key] = line.replace('### 1. **Found Files**:', '').strip()
#     elif line.startswith('### 2. **Downsides/Comments**:'):
#         current_key = 'downsides_comments'
#         response_blocks[current_key] = line.replace('### 2. **Downsides/Comments**:', '').strip()
#     elif line.startswith('### 3. **Rating**:'):
#         current_key = 'rating'
#         response_blocks[current_key] = line.replace('### 3. **Rating**:', '').strip()
#     elif line.startswith('### 4. **Conclusion**:'):
#         current_key = 'conclusion'
#         response_blocks[current_key] = line.replace('### 4. **Conclusion**:', '').strip()
#     elif current_key:
#         # Додаємо рядки до відповідного блоку
#         response_blocks[current_key] += ' ' + line
#
# # Виводимо отримані блоки
# pprint(response_blocks)
