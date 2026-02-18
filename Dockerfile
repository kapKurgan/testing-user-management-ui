FROM python:3.10

LABEL maintainer="kkaapp@yandex.ru" \
      description="AQA Python: UI-тесты на Playwright + pytest + Allure"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright

RUN apt-get update && apt-get install -y

RUN pip install playwright

RUN playwright install --with-deps chromium

COPY . .
RUN mkdir -p reports/allure-results reports/allure-report

RUN pip install --no-cache-dir -r requirements.txt

# CMD ["pytest", "-s", "-v", "--alluredir=reports/allure-results", "--html=reports/pytest_report.html", "--capture=tee-sys", "--self-contained-html", "tests/test_page_login.py"]

# Системные зависимости для Allure
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jre-headless curl
ARG ALLURE_VERSION=2.23.1
RUN curl -L -o /tmp/allure.tgz \
    "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz" \
    && tar -xzf /tmp/allure.tgz -C /opt \
    && ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/local/bin/allure \
    && rm /tmp/allure.tgz

# Порты, которые будем пробрасывать наружу
EXPOSE 8080 5252

# Скрипт-обёртка
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Переключаемся на скрипт
ENTRYPOINT ["/entrypoint.sh"]
