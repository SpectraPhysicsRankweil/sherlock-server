# build stage
FROM node:lts-alpine as build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# production stage
FROM python:3.9-slim

EXPOSE 80

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY server.py /app/
COPY --from=build-stage /app/dist /app/static

WORKDIR /app

CMD ["python3", "-u", "server.py"]