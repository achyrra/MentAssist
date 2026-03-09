# -------------------------------------------------------
# Stage 1: Build
# Frontend team: fill in your build steps here.
# This stub assumes a Node-based framework (React, Vue, etc.)
# -------------------------------------------------------
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies first (layer caching)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build
# Output is expected at /app/dist — update below if your
# framework outputs elsewhere (e.g. /app/build for CRA)

# -------------------------------------------------------
# Stage 2: Serve
# Copies only the built static files into a minimal nginx image.
# No Node runtime in the final image.
# -------------------------------------------------------
FROM nginx:1.27-alpine AS serve

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy built assets from Stage 1
# Update the source path if your build output dir differs
COPY --from=build /app/dist /usr/share/nginx/html

# Simple nginx config to serve the SPA with fallback routing
RUN printf 'server {\n\
    listen 80;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
