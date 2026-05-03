FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DEPLOY_API_KEY=ng-deploy-key-7a3f92b1
EXPOSE 5000
CMD ["python", "app.py"]
