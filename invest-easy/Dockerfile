# Stage 1: Build the Angular application
FROM node:18-alpine AS build
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy all files
COPY . .

# Build both client and server
RUN npm run build
RUN npm run build:ssr

# Stage 2: Serve the application
FROM node:18-alpine
WORKDIR /app

# Copy built files from build stage
COPY --from=build /app/dist/invest-easy/browser ./browser
COPY --from=build /app/dist/invest-easy/server ./server

# Install production dependencies
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Copy nginx config
COPY nginx.conf ./

# Install nginx and supervisord
RUN apk add --no-cache nginx supervisor

# Configure supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80 4000

# Start services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
