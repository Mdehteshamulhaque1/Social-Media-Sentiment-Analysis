FROM node:20-alpine AS build

WORKDIR /app
COPY frontend/package.json ./frontend/package.json
RUN cd frontend && npm install
COPY frontend ./frontend
ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN cd frontend && npm run build

FROM nginx:1.27-alpine
COPY infra/nginx/frontend.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/frontend/dist /usr/share/nginx/html
EXPOSE 80
