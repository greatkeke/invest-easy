# Stage 1: Build the Angular application
FROM node:18-alpine AS build

WORKDIR /app

# Copy only necessary files for npm install
COPY package.json package-lock.json ./

# Install dependencies and clean cache
RUN npm ci && \
    npm cache clean --force

# Copy only necessary source files
COPY src/ src/
COPY angular.json tsconfig.* ./

# Build both client and server
RUN npm run build && \
    rm -rf node_modules

# Stage 2: Serve the application
FROM node:18-alpine

WORKDIR /app

# Copy only necessary built files
COPY --from=build /app/dist/invest-easy/browser ./dist/invest-easy/browser
COPY --from=build /app/dist/invest-easy/server ./dist/invest-easy/server

# Install production dependencies
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && \
    npm cache clean --force

# Expose port
EXPOSE 4000

VOLUME /app/dist/invest-easy/browser/assets 

# Start the SSR server
CMD ["npm", "run", "serve:ssr:invest-easy"]
